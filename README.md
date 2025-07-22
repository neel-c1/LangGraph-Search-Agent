# LangGraph Search Agent

This is an agentic AI program that generates reports based on a provided query. Think of this as an alternative to Google search. This is also just a sample program that isn't anything too crazy.

## Requirements

1. Python 3.12
2. OpenAI API Key
3. SerpAPI API Key

## Set up

```
git clone https://www.github.com/neel-c1/LangGraph-Search-Agent.git
cd LangGraph-Search-Agent
cp -r .env.example .env
```
Copy paste your API keys accordingly.
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -U pip
pip3 install -r requirements.txt
python3 main.py
```
Alternatively, you can run `python3 main.py gui` if you'd like a GUI based program.

## Done?

Press `^C` on your keyboard.
```
deactivate
rm -rf .venv
```