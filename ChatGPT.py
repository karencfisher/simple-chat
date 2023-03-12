'''
GPT Chat

The loop is basically

speech -> text -> prompt -> completion by GPT-3 -> response -> speech

Until the user says simply "goodbye", at which point the model is allowed
to reply, and then the program exits.

'''
import os
import json
import logging
from datetime import datetime
import openai
from dotenv import load_dotenv

from ChatGPTContext import Context
from vosk_recognizer import SpeechRecognize
from tts import Text2Speech


class ChatGPT:
    def __init__(self, logger, pretext=''):
        # fetch API key from environment
        load_dotenv()
        self.secret_key = os.getenv('SECRET_KEY')

        # intialize speech recognition
        self.recog = SpeechRecognize()

        # Initialize TTS
        self.tts = Text2Speech()

        # get configuration
        with open('chatgpt_config.json', 'r') as FP:
            self.config = json.load(FP)

        # set up context
        self.context = Context(response_tokens=self.config['max_tokens'], 
                               pretext=pretext)

        self.logger = logger
        self.logger.info("*Begin log*\n")

    def loop(self):
        '''
        The main loop

        Loops until the user says simply "goodbye" and model has responded
        to that prompt.
        '''
        text = 'hello'
        while True:
            # update context and get prompt
            self.logger.info(f'["Human"] {text}')
            self.context.add(role='user', text=text)

            # send prompt to GPT-3
            prompt = self.context.get_prompt()
            ai_text, n_tokens = self.__prompt_gpt(prompt)

            # speak and log response
            self.tts.speak(ai_text)
            self.logger.info(f'["AI"] {ai_text.strip()}')
            self.context.add(role='assistant',
                             text=ai_text, 
                             n_tokens=n_tokens)

            # See if user said goodbye
            if text == 'goodbye':
                break

            # Listen for user input
            text = self.recog.speech_to_text()

        self.logger.info('\n*End log*')
        print('\rExiting...')

    def __prompt_gpt(self, prompt):
        '''
        Prompt GPT-3

        Input: prompt - string
        Returns: text from the model
        '''
        print('\rWaiting...     ', end='')
        openai.api_key = self.secret_key
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=prompt,
            max_tokens=self.config['max_tokens'],
            temperature=self.config['temperature'],
            top_p=self.config['top_p'],
            n=self.config['n'],
            presence_penalty=self.config['presence_penalty'],
            frequency_penalty=self.config['frequency_penalty']
        )
        text = response.choices[0].message.content
        n_tokens = response.usage.completion_tokens
        return text, n_tokens


def main():
    # initialize logging
    now = datetime.now()
    logfile = f'chatgptlog-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
    logpath = os.path.join('logs', logfile)
    logging.basicConfig(filename=logpath, 
                        level=logging.INFO, 
                        format='%(message)s')
    logger = logging.getLogger()

    # If pretext file exists, load it
    pretext = ''
    if os.path.exists('chat_pretext.txt'):
        with open('chat_pretext.txt', 'r') as PRETEXT:
            pretext = PRETEXT.read()

    # set up profile (if exists) and concatenate to pretext
    if os.path.exists("chat_user_profile.txt"):
        with open('chat_user_profile.txt', 'r') as FP:
            profile = FP.read()
        pretext += f'\n\nUser profile:\n{profile}'

    # Inistantiate GPTChat and run loop
    print('Initializing...', end='')
    gpt_chat = ChatGPT(logger, pretext=pretext)
    gpt_chat.loop()


if __name__ == '__main__':
    main()
