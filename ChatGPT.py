'''
ChatGPT chatbot

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


class ChatGPT:
    def __init__(self, logger):
        # fetch API key from environment
        load_dotenv()
        self.secret_key = os.getenv('SECRET_KEY')

        # get configuration
        with open('chat_config.json', 'r') as FP:
            self.config = json.load(FP)

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

        self.context = Context(self.pretext, num_response_tokens=self.config['max_tokens'])

        # start log
        self.logger = logger
        self.logger.info("*Begin log*\n")

        self.prompt_tokens_used = 0
        self.completion_tokens_used = 0

    def loop(self):
        '''
        The main loop

        Loops until the user says simply "goodbye" and model has responded
        to that prompt.
        '''
        text = 'hello'
        while True:
            # update context and get prompt
            self.logger.info(f'[Human] {text}')
            self.context.add(role='user', text=text)

            # send prompt to GPT-3.5
            prompt = self.context.get_prompt()
            ai_text, n_tokens = self.__prompt_gpt(prompt)
    
            # speak and log response
            self.tts.speak(ai_text)
            self.logger.info(f'[AI] {ai_text}')

            # update context. If first two iterations, store as pretext
            # (pinned messages). 
            self.context.add(role='assistant',
                            text=ai_text,
                            n_tokens=n_tokens)

            # See if user said goodbye
            if text == 'goodbye':
                break

            # Listen for user input
            text = self.recog.speech_to_text()

        self.logger.info('\n*End log*')

        # finishing up
        print('\rExiting...')

        if self.config['model'] == 'gpt-3.5-turbo':
            cost = (self.prompt_tokens_used + self.completion_tokens_used)/\
                   1000 * .002
        else:
            cost = self.prompt_tokens_used / 1000 * .03 + \
                   self.completion_tokens_used / 1000 * .06
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
        openai.api_key = self.secret_key
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
        n_tokens = response.usage.completion_tokens
        self.prompt_tokens_used += response.usage.prompt_tokens
        self.completion_tokens_used += n_tokens
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

    # Inistantiate GPTChat and run loop
    print('Initializing...', end='')
    gpt_chat = ChatGPT(logger)
    gpt_chat.loop()


if __name__ == '__main__':
    main()
