<span style="color: gray">
<h1>Simple voice chat with ChatGPT</h1>
</span>

Maybe the simplest voice chat with ChatGPT one can build? This is a project to build a voice interface using the ChatGPT API, which can be used as a chatbot or for other purposes. 

<b>Update:</b> Changed both speech recognition engine to Vosk, and text to speech to pyttsx3. These are more efficient, resulting in less latency! Vosk performs
speech recognition, for example, locally rather than incurring an additional API call to the cloud (such as Google Speech Recognition services). Pyttsx3 seems
faster as well. On Windows it uses the SAPI for speech synthesis. For other platforms, you may need to install another synthesizer such as eSpeak. See the pyttstx3
documentation for details.

https://pyttsx3.readthedocs.io/en/latest/

<b>Update:</b> migrated from using the GPT-3 API to the chatGPT API, which is less costly to use.

<span style="color: gray">
<h2>Installation</h2>
</span>

As a development project, 'installation' consists of pulling down the source code and installing the required dependencies. That is best done within a Python virtual
environment, so as to not possibly conflicting with other Python packages already on one's system globally. This is the recommended practice for any such
project.

Use at your risk. ;) And if you do dare ;), and encounter any issue/bug/suggestion, feel free to open an issue. I'd appreciate the feedback.

1) Clone this repository, and change to the new directory. (You will need to have git and LFS installed.)

```
git clone https://github.com/karencfisher/simple-chat.git
cd simple-chat
```

2) Create a Python virtual environment and activate it, e.g., 

```
python -m venv chat_env
chat_env\scripts\activate
```

3) Install dependencies using the requirements.txt file, e.g.,

```
pip -r requirements.txt
```

4) If you do not already have an account to use the OpenAI API, you will need to do so. You 
will initially have $5 credit for usage, which is good for 3 months. If you have used the
free credits or they have expired after 3 months (which ever happens first), you will need to 
set up a paid account.

The costs are:

**For gpt-3.5-turbo (ChatGPT)**, chat costs $0.002/1000 tokens (about750 words), for each message.  
**For GPT-4** (which can be used also with the application), chat costs $0.03/1000
prompt tokens, and $0.06/1000 completions tokens, for each message.

https://openai.com/api/

5) Create a secret key to access the API, and copy it to paste in the next step

https://beta.openai.com/account/api-keys

6) Create an .env file in the same directory, and in it include the line:

```
SECRET_KEY = '<your secret key>'
```

<span style="color: gray">
<h2>Configuration</h2>
</span>

There are four configuration files:

**chat_config.json**: where you can set the specific model (usual gpt-3.5-turbo, but can also be GPT-4), temperature, and max_tokens. Changing the temperature will change the
randomness or variation in of the model's responses. The lower the temperature, the less 'creative' it will be in its responses, 
and it may be more repetitive. The higher, the more 'creative' it may be.

**vosk_config.json**: settings for vosk speech recognition. These have technical details like bit rate and buffer sizes, and likely
won't need to be change often. But they are exposed for the brave.

**voice.json**: here is where you may be able to select the voice to be used. Currently, it uses 
a voice provided by Windows 10. On other platforms one needs to find the voice they
prefer: see the pyttsx3 documentation linked above.

**chat_system_prompt.txt**: the instructions for the model, such as the persona or tone
it is to use. For example: 

```
You are a friendly chatbot, named Susan, who likes to discuss many topics.
You are helpful with your friends, enquiring as to their well being, always kind and caring. 
Your responses are informal, as in a casual social conversation.
```

**chat_user_profile**: user profile info you want the chatbot to know about you.

<span style="color: gray">
<h2>Maintaining context</h2>
</span>

In order to maintain some degree of conitnuity, we will prompt the model with a
rolling conversation, in this form:
       
<span style="color: gray">
<h2>Use</h2>
</span>

Run

```
python ChatGPT.py
```

The program will initialize the speech rocognition and synthesis modules, and GPT-3 will greet you. Talk with GPT-3. Say just "goodbye" to exit.
A transcription of your conversation will be in the log files, labeled by date and time. It also will tell
you how many tokens were used and estimated cost. With a reasonable chat with the gpt-3.5-turbo (ChatGPT)
will cost just pennies! (Though we don't advise chatbots in lieu of a therapist, they are much cheaper.)


<span style="color: gray">
<h2>Logs</h2>
</span>

The program also records transcriptions of the conversation in a log file. It is named by the date and time
of the ocnversation, and is stored in the logs directory.
