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

from context import Context
from vosk_recognizer import SpeechRecognize
from tts import Text2Speech


class GPTChat:
    def __init__(self, logger, pretext=''):
        # fetch API key from environment
        load_dotenv()
        self.secret_key = os.getenv('SECRET_KEY')

        # intialize speech recognition
        self.recog = SpeechRecognize()

        # Initialize TTS
        self.tts = Text2Speech()

        # fetch gpt-3 config
        with open('gpt3_config.json', 'r') as FP:
            self.gpt3_config = json.load(FP)

        # set up context
        self.context = Context(pretext=pretext)

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
            self.logger.info(f'[human] {text}')
            self.context + text
            prompt = self.context.get_prompt()

            # send prompt to GPT-3
            response = self.__prompt_gpt(prompt)

            # speak and log response
            self.tts.speak(response)
            self.logger.info(f'[AI] {response.strip()}')
            self.context + response

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
        response = openai.Completion.create(
            engine = self.gpt3_config['engine'],
            prompt = prompt,
            temperature = self.gpt3_config['temperature'],
            max_tokens = self.gpt3_config['max_tokens']
        )
        return response.choices[0].text


def main():
    # initialize logging
    now = datetime.now()
    logfile = f'chatlog-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
    logpath = os.path.join('logs', logfile)
    logging.basicConfig(filename=logpath, 
                        level=logging.INFO, 
                        format='%(message)s')
    logger = logging.getLogger()

    # If pretext file exists, load it
    pretext = ''
    if os.path.exists('pretext.txt'):
        with open('pretext.txt', 'r') as PRETEXT:
            pretext = PRETEXT.read()
            pretext = pretext.replace('\n', ' ')

    # Inistantiate GPTChat and run loop
    print('Initializing...', end='')
    gpt_chat = GPTChat(logger, pretext=pretext)
    gpt_chat.loop()


if __name__ == '__main__':
    main()
