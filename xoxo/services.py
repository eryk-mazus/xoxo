from typing import List, Dict

from xoxo import models


def extract_result_from_bing(resp: dict) -> List[models.SearchResult]:
    return [
            models.SearchResult(x["name"], x["url"], x["snippet"])
            for x in json_response["webPages"]["value"]
            ]


def extract_result_from_ddg(result: List[Dict[str, str]]):
    assert len(result), "Empty result"
    res = result[0]
    assert res["title"] and res["body"] and res["href"], "Response object is not compatible"


    return [
            models.SearchResult(name=x["title"], url=x["href"], snippet=x["body"])
            for x in result
            ]



