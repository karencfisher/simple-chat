'''
ChatGPT chatbot

The loop is basically

speech -> text -> prompt -> completion by GPT-3 -> response -> speech

Until the user says simply "goodbye", at which point the model is allowed
to reply, and then the program exits.

'''
import os
import sys
import json
import logging
from datetime import datetime
import openai
# import gpt4all
import google.generativeai as palm
from dotenv import load_dotenv

from context import Context
from vosk_recognizer import SpeechRecognize
from tts import Text2Speech
from ui import STDIO


class ChatGPT:
    def __init__(self, logger, ui=STDIO):
        self.ui = ui()

        # fetch API key from environment
        load_dotenv()
        
        # get configuration
        with open('chat_config.json', 'r') as FP:
            self.config = json.load(FP)
        
        if self.config['provider'] == 'openai':
            secret_key = os.getenv('OPENAI_SECRET_KEY')
            openai.api_key = secret_key
        elif self.config['provider'] == 'gpt4all':
            self.gpt4all = gpt4all.GPT4All(self.config['model'])
        elif self.config['provider'] == 'PaLM':
            secret_key = os.getenv('PALM_SECRET_KEY')
            palm.configure(api_key=secret_key)
        else:
            raise ValueError('Invalid provider choice')

        # intialize speech recognition
        self.recog = SpeechRecognize()

        # Initialize TTS
        self.tts = Text2Speech()

        # get system prompt
        with open('chat_system_prompt.txt', 'r') as PRETEXT:
            self.pretext = PRETEXT.read()
        
        with open('chat_user_profile.txt', 'r') as PROFILE:
           profile = PROFILE.read()
        self.pretext += 'User profile:\n\n' + profile

        self.context = Context(self.pretext, 
                               num_response_tokens=self.config['max_tokens'],
                               max_context_tokens=self.config['max_context'])

        # start log
        self.logger = logger
        self.logger.info("*Begin log*\n")

        self.prompt_tokens_used = 0
        self.completion_tokens_used = 0

    def loop(self, voice=True):
        '''
        The main loop

        Loops until the user says simply "goodbye" and model has responded
        to that prompt.
        '''
        text = 'hello'
        while True:
            # update context and get prompt
            self.logger.info(f'[Human] {text}')
            self.context.add(role='user', 
                             text=text, 
                             provider=self.config['provider'])

            # send prompt to GPT-3.5
            prompt = self.context.get_prompt()
            ai_text, n_tokens = self.__prompt_gpt(prompt)
    
            # speak and log response
            if voice:
                self.tts.speak(ai_text)
            else:
                self.ui.output(ai_text)


            self.logger.info(f'[AI] {ai_text}')

            # update context. If first two iterations, store as pretext
            # (pinned messages). 
            self.context.add(role='assistant',
                            text=ai_text,
                            provider=self.config['provider'],
                            n_tokens=n_tokens)

            # See if user said goodbye
            if text == 'goodbye':
                break

            # Listen for user input
            if voice:
                text = self.recog.speech_to_text()
            else:
                text = self.ui.input()

        self.logger.info('\n*End log*')

        # finishing up
        print('\rExiting...')

        if self.config['model'] == 'gpt-3.5-turbo':
            cost = (self.prompt_tokens_used + self.completion_tokens_used)/\
                   1000 * .002
        elif self.config['model'] == "gpt-4":
            cost = self.prompt_tokens_used / 1000 * .03 + \
                   self.completion_tokens_used / 1000 * .06
        else:
            cost = 0.0
        print(f'Prompt tokens used: {self.prompt_tokens_used}')
        print(f'Completion tokens used: {self.completion_tokens_used}')
        print(f'Total price: ${cost: .3f}')

    def __prompt_gpt(self, prompt):
        '''
        Prompt GPT-3

        Input: prompt - string
        Returns: text from the model
        '''
        print('\rWaiting...     ', end='')

        if self.config['provider'] == 'openai':
            response = openai.ChatCompletion.create(
                model=self.config['model'],
                messages=prompt,
                max_tokens=self.config['max_tokens'],
                temperature=self.config['temperature'],
                top_p=self.config['top_p'],
                n=self.config['n'],
                presence_penalty=self.config['presence_penalty'],
                frequency_penalty=self.config['frequency_penalty']
            )
            text = response.choices[0].message.content
            completion_tokens = response.usage.completion_tokens
            prompt_tokens = response.usage.prompt_tokens

        elif self.config['provider'] == 'gpt4all':
            response = self.provider.chat_completion(
                messages=prompt,
                verbose=False,
                streaming=False
            )
            text = response['choices'][0]['message']['content']
            completion_tokens = response['usage']['completion_tokens']
            prompt_tokens = response['usage']['prompt_tokens']

        elif self.config['provider'] == 'PaLM':
            response = palm.chat(
                model=self.config['model'],
                context=self.pretext,
                messages=prompt[1:],
                temperature=self.config['temperature'],
                top_p=self.config['top_p'],
                top_k=self.config['top_k'],
            )
            text = response.last
            completion_tokens = 0
            prompt_tokens = 0

        else:
            raise ValueError('Invalid provider')
        
        self.prompt_tokens_used += prompt_tokens
        self.completion_tokens_used += completion_tokens
        return text, completion_tokens


def main():
    voice = True
    if len(sys.argv) > 1:
        if sys.argv[1] == 'novoice':
            voice=False
        else:
            print(f'Unrecognized argument {sys.argv[1]}')
            return

    # initialize logging
    now = datetime.now()
    logfile = f'chatgptlog-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
    logpath = os.path.join('logs', logfile)
    logging.basicConfig(filename=logpath, 
                        level=logging.INFO, 
                        format='%(message)s')
    logger = logging.getLogger()

    # Inistantiate GPTChat and run loop
    print('Initializing...', end='')
    gpt_chat = ChatGPT(logger)
    gpt_chat.loop(voice=voice)


if __name__ == '__main__':
    main()
