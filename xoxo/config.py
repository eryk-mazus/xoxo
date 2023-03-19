import os

XOXO_SUMMARY_PROMPT = """
You are given a query and retrieved search results. Summarize the given search results keeping the user request in mind. 
If you enumerate things, list them from bullets in new lines with urls in parethesies so that the user could click on them.

RESULTS:
{results}

QUERY: {query}

ANSWER:

"""



BING_SUBSCRIPTION_KEY = os.environ["BING_SUBSCRIPTION_KEY"]
BING_ENDPOINT_URL = "https://api.bing.microsoft.com/v7.0/search"

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

