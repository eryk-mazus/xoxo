import os
import json
import requests
import openai

from typing import List

from colorama import Fore, Back, Style

from xoxo import models, search

class Retriever:
    def __init__(
            self, 
            *,
            search_service: search.SearchServiceABC,
            openai_api_key: str,
            summary_prompt: str,
            k: int = 3
            ):

        self.k = k
        self._search_service = search_service
        self._openai_api_key = openai_api_key
        self._summary_prompt = summary_prompt

    def trigger(self, query: str, user_request: str = None):
        search_results = self._search_service.search(query)
        passages = "\n\n".join([x.get_passage() for x in search_results[: self.k]])
        request, state = (user_request, "XOXO") if user_request else (query, "RESULT")
        summary = self.summarize(request, passages)

        return models.Message(state, summary)


    def summarize(self, query: str, context: str) -> str:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self._summary_prompt.format(query=query, results=context),
            temperature=0.5,
            max_tokens=350,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].text.strip()

    @staticmethod
    def format_boring_msg(s: str) -> str:
        prefix = f"{Fore.CYAN} ~~ response:{Style.RESET_ALL}"
        return prefix + "\n" + f"{Fore.CYAN}{s}{Style.RESET_ALL}" + "\n" + f"{Fore.CYAN} {'~'*30}"

