# OpenAI API Experiements

This is a repo with some basic experiments using the OpenAI API.

## Getting Started

Clone the repo to your local machine then run the following.

```
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Now you should be able to run the experiments.

## Experiments

### Chat Bypass

A simple program to access GPT directly through the API which helps when the web version of GPT is down or glitchy.

### Voice Chat

Uses a number of libraries to enable voice chat with GPT. Also logs out the text version (important as speech synthesis and transcription is *slow*). Uses push-to-talk bound to CTRL.
* OpenAI speech transcription
* GPT
* ElevenLabs speech synthesis to provide the voice for GPT.