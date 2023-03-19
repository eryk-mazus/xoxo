from typing import List
from abc import ABC, abstractmethod

import requests
from duckduckgo_search import ddg

from xoxo import services, models

class SearchServiceABC(ABC):

    @abstractmethod
    def search(self, query: str) -> List[models.SearchResult]:
        pass


class BingSearchService(SearchServiceABC):
    locale = "en-US"
    bing_api_endpoint = "https://api.bing.microsoft.com"

    def __init__(
            self, 
            *,
            bing_api_key: str, 
            requests_session: requests.Session = None
            ):

        self._bing_api_key = bing_api_key

        if requests_session is None:
            self._rsession = requests.Session()

        headers = {"Ocp-Apim-Subscription-Key": self._bing_api_key}
        self._rsession.headers.update(headers)

    def search(
            self, 
            query: str,
            ) -> List[models.SearchResult]:


        params = {"q": query, "mkt": self.locale}
        response = self._make_request(path="/v7.0/search", params=params)

        return services.extract_result_from_bing(response.json())

    def _make_request(self, *, path: str, params: dict):
        url = "{0}{1}".format(self.bing_api_endpoint, path)
        response = self._rsession.get(
                url,
                params=params
                )
        response.raise_for_status()

        return response




class DuckDuckGoSearchService(SearchServiceABC):
    locale = "en-US"

    def search(
            self, 
            query: str,
            ) -> List[models.SearchResult]:

        response = ddg(keywords=query, region=self.locale)
        return services.extract_result_from_ddg(response)

