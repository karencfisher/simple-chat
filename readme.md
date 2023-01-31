## Simple voice chat with GPT-3

Maybe the simplest voice chat with GPT-3 one can build? Using SpeechRecognition to convert speech to text (using the Google speech recongition engine), passing the text to GPT-3 via the OpenAI API, and then converting the resulting text to speech using Coqui TTS and simple audio. 

Developed and test on Windows 10.

### Installation

It might be necessary to have installed eSpeak-ng. https://github.com/espeak-ng/espeak-ng/blob/master/docs/guide.md

1) Clone this repository, and change to the new directory
2) Create a Python virtual environment and activate it, e.g., 

```
>>> python -m venv .
>>> scripts\activate
```

3) Install dependencies using the requirements.txt file, e.g.,

```
>>> pip -r requirements.txt
```

4) If you do not already have an account to use the OpenAI API, you will need to do so. 

https://openai.com/api/

5) Create a secret key to access the API, and copy it to paste in the next step

https://beta.openai.com/account/api-keys

6) Create an .env file in the same directory, and in it include the line:

```
SECRET_KEY = '<your secret key>'
```

Pasting your API key in place of the '<your secret key>'

### Establishing context

In order to make an interesting chatbot to have a conversation with, there is maintenance of a
rolling context. It includes a "pretext" prompting GPT-3 to take a particular role. For example,

"The following is a conversation with an AI assistant. The assistant is helpful, creative, 
clever, and very friendly."

If there is a pretext, it is stored in a text file which must be pretext.txt.

The ensuing interaction (the context) is then appended after the pretext (if there is any), up to 2048 tokens
(both pretext and the context). When the total number of tokens exceed 2048 (the input limit for GPT-3), 
the context is truncated from the earliest intereactions. This maintains at least a short memory of the
interaction.

### Use

Run

```
>>> python gpt_chat.py
```

It will initialize the TTS and SpeechRecognition modules and then display "listen..." Talk with GPT-3. Say "goodbye" to exit.
