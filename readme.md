<span style="color: gray">
<h1>Simple voice chat with GPT-3</h1>
</span>

Maybe the simplest voice chat with GPT-3 one can build? Using SpeechRecognition to convert speech to text (using the Google speech recongition engine), passing the text to GPT-3 via the OpenAI API, and then converting the resulting text to speech using Coqui TTS and simple audio. 


<span style="color: gray">
<h2>Installation</h2>
</span>

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

<span style="color: gray">
<h2>Maintaining context</h2>
</span>

In order to maintain some degree of conitnuity, we will prompt the model with a
rolling conversation, in this form:

<span style="color: gray">
PRETEXT:
</span>

"The following is a conversation with an AI assistant. The assistant is helpful, creative, 
clever, and very friendly. The assistant's name is Susan." 

<span style="color: gray">
CONTEXT:
</span>

[human] Hello Susan.  

[AI] Hello, what can I do for you today?  

[human] Why don't you tell us who you are?  

[AI] I am Susan, an AI virtual assistant, so I'm always here to help you. No matter where you are, I'm here to answer your questions.  

[human] okay what is the meaning of life?  

[AI] The meaning of life is a complex question that has no single answer. Everyone has their own opinion on what life is all about. Some believe that life is about finding purpose and creating a life of meaning, while others believe that life is simply about experiencing joy and living in the moment. Ultimately, it's up to you to decide what the meaning of life is for you.

[human] Tell me more about it?

The <span style="color: gray">PRETEXT</span> defines a role or character for the conversational agent, or other
wise define it's purpose. It is defined in a text file in the working directory that woth the file name of 'pretext.txt.' If one want to omit a pretext, the file can be omitted.

The <span style="color: gray">CONTEXT</span> then is the rolling, recent conversation. 

The total length of this altogether, which becomes the next prompt to the model.
<b>The total combination of pretext and context cannot exceed 2048 tokens, which is the input limit for
GPT-3</b>. When that limit is reached, the earlier portions of the context is truncated.<br>

<span style="color: gray">
<h2>Different tasks</h2>
</span>

You can also define different use cases aside as an AI assistant or chat bot by defining a different
pretext. For example, to use as an English to French translator, create a pretext.txt file containing
simply:

```
Translate English to French
```

For example, a transcription of a translation session then:

```
[human] good morning
[AI] Bonjour
[human] what are we doing today
[AI] Qu'est-ce que nous faisons aujourd'hui ?
[human] maybe we can prove on your accent
[AI] Peut-�tre que nous pouvons travailler sur ton accent
[human] goodbye
[AI] Au revoir
```

Though the accent could be better, to say the least.

         
<span style="color: gray">
<h2>Use</h2>
</span>

Run

```
>>> python gpt_chat.py
```

The program will initialize the TTS and SpeechRecognition modules, and then display "listen..." Talk with GPT-3. Say "goodbye" to exit.


<span style="color: gray">
<h2>Logs</h2>
</span>

The program also records transcriptions of the conversation in a log file. It is named by the date and time
of the ocnversation, and is stored in the logs directory.
