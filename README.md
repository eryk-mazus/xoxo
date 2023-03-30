# xoxo

tiny, exploitable chatbot that can use tools

something between chatgpt and perplexity.ai with a toolformer flavour, but in your terminal 

demo:

https://user-images.githubusercontent.com/21311210/228931234-1a2abb4d-53a1-414b-8455-13152261dc6e.mp4

## Setup

1. Add OpenAI API key to the environment variables:
```
set OPENAI_API_KEY=XXX
```

2. Install and Run 
```
poetry install
poetry run python ./xoxo/main.py --user_name YOUR_NAME
```

## Ideas for near-term development:
- docker
- support llama/alpaca.cpp
- add yaml with config
- publish to pypi

Contributions welcome !
