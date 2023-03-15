# xoxo.ai

tiny, exploitable chatbot that can use tools

something between chatgpt and perplexity.ai with a toolformer flavour

<p align="center">
  <img src="https://raw.githubusercontent.com/eryk-mazus/xoxo/main/docs/example.png">
</p>

## Setup

1. Add OpenAI API and Bing Web Search API keys to the environment variables:
```
set OPENAI_API_KEY=XXX
set BING_SUBSCRIPTION_KEY=XXX
```

If you don't have Azure account, you can set it up [here](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api). Free tier gives you 1k calls per month.


2. Installation 
```
poetry install 
```

3. Run
```
poetry run python ./xoxo/main.py --user_name YOUR_NAME
```

## Ideas for near-term development:
- flushing conversation history when the max context length is close to being overflown
- add the local memory ~ cashing and retrieving information from previous conversations
- ui
- support other LLMs besides gpt

Contributions welcome !