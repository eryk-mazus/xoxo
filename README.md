# xoxo.ai

tiny, exploitable chatbot that can use tools

something between chatgpt and perplexity.ai with a toolformer flavour

<p align="center">
  <img src="https://raw.githubusercontent.com/eryk-mazus/xoxo/main/docs/example.png">
</p>

## Setup

1. Add OpenAI API key to the environment variables:
```
set OPENAI_API_KEY=XXX
```

2. Installation 
```
poetry install 
```

3. Run
```
poetry run python ./xoxo/main.py --user_name YOUR_NAME
```

## Ideas for near-term development:
- docker
- support LLaMA/Alpaca besides gpt
- ui

Contributions welcome !