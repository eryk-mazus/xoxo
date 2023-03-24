from typing import List
import  os
import json
import requests
import openai
from colorama import Fore, Back, Style
from xoxo import Message, SearchResult

openai.api_key = os.environ["OPENAI_API_KEY"]

# Bing web search API credentials
subscription_key = os.environ["BING_SUBSCRIPTION_KEY"]
endpoint = "https://api.bing.microsoft.com/v7.0/search"

summary_prompt = """
You are given a query and retrieved search results. Summarize the given search results keeping the user request in mind. 
If you enumerate things, list them from bullets in new lines with urls in parethesies so that the user could click on them.

RESULTS:
{results}

QUERY: {query}

ANSWER:

"""

class Retriever:
    def __init__(self, k: int = 3) -> None:
        self.k = k

    def trigger(self, query: str, user_request: str = None):
        search_results = self.search(query)
        passages = "\n\n".join([x.get_passage() for x in search_results[: self.k]])
        request, state = (query + "\nUSER QUESTION: " + user_request + "\n", "XOXO") if user_request else (query, "RESULT")

        summary = self.summarize(request, passages)
        return Message(state, summary)

    def search(self, query: str) -> List[SearchResult]:
        mkt = "en-US"
        params = {"q": query, "mkt": mkt}
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}

        # todo:
        # check if there is a way to limit the number of search results

        # call to the search api:
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()

            _ = response.headers
            json_response = response.json()

            return [
                SearchResult(x["name"], x["url"], x["snippet"])
                for x in json_response["webPages"]["value"]
            ]
        except Exception as e:
            print(e)
            return []

    def summarize(self, query: str, context: str) -> str:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=summary_prompt.format(query=query, results=context),
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