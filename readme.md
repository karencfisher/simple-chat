## Simple voice chat with GPT-3

Maybe the simplest voice chat with GPT-3 one can build? Using SpeechRecognition to convert speech to text (using the Google speech recongition engine), passing to GPT-3 via the OpenAI API, and then converting the resulting text to speech using Coqui TTS and simple audio. 

Developed and test on Windows 10.

### Installation

It might be necessary to have installed eSpeak-ng. https://github.com/espeak-ng/espeak-ng/blob/master/docs/guide.md

1) Clone this repository
2) Create a Python virtual environment and activate it, e.g., 

```
>>> python -m venv .
>>> scripts\activate
```

3) Install dependencies using the requirements.txt file, e.g.,

```
>>> pip: -r requirements.txt
```

### Use

Run

```
>>> python gpt_chat.py
```

It will initialize the TTS and SpeechRecognition modules and then display "listen..." Talk with GPT-3. Say "goodbye" to exit.
