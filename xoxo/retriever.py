import os
import json
import requests
import openai

from typing import List

from colorama import Fore, Back, Style

from xoxo import models

class Retriever:
    def __init__(
            self, 
            *,
            openai_api_key: str,
            bing_api_key: str,
            summary_prompt: str,
            bing_api_endpoint="https://api.bing.microsoft.com/v7.0/search"
            k: int = 3
            ):

        self.k = k
        self._openai_api_key = openai_api_key
        self._bing_api_key = bing_api_key
        self._bing_api_endpoint = bing_api_endpoint
        self._summary_prompt = summary_prompt

    def trigger(self, query: str, user_request: str = None):
        search_results = self.search(query)
        passages = "\n\n".join([x.get_passage() for x in search_results[: self.k]])
        request, state = (user_request, "XOXO") if user_request else (query, "RESULT")
        summary = self.summarize(request, passages)

        return models.Message(state, summary)

    def search(self, query: str) -> List[SearchResult]:
        mkt = "en-US"
        params = {"q": query, "mkt": mkt}
        headers = {"Ocp-Apim-Subscription-Key": self._bing_api_key}

        # todo:
        # check if there is a way to limit the number of search results

        # call to the search api:
        try:
            response = requests.get(
                    self._bing_api_endpoint, 
                    headers=headers, 
                    params=params
                    )
            response.raise_for_status()

            _ = response.headers
            json_response = response.json()

            return [
                models.SearchResult(x["name"], x["url"], x["snippet"])
                for x in json_response["webPages"]["value"]
            ]
        except Exception as e:
            print(e)
            return []

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
