'''
GPT Chat

The loop is basically

speech -> text -> prompt -> completion by GPT-3 -> response -> speech

Until the user says simply "goodbye", at which point the model is allowed
to reply, and then the program exits.

'''
import os
import logging
from datetime import datetime
import openai
from dotenv import load_dotenv
import speech_recognition as sr
from TTS.api import TTS
import simpleaudio as sa

from context import Context


class GPTChat:
    def __init__(self, logger, pretext=''):
        # fetch API key from environment
        load_dotenv()
        self.secret_key = os.getenv('SECRET_KEY')

        # intialize speech recognition and TTS
        self.recog = sr.Recognizer()
        model_name = TTS.list_models()[0]
        self.tts = TTS(model_name)

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
        text = ''
        while text != 'goodbye':
            # Listen for user input
            try:
                text = self.__listen()
            except ConnectionError:
                break
            self.logger.info(f'[human] {text}')

            # update context and get prompt
            self.context + text
            prompt = self.context.get_prompt()

            # send prompt to GPT-3
            response = self.__prompt_gpt(prompt)

            # speak and log response
            self.__respond(response)
            self.logger.info(f'[AI] {response.strip()}')
            self.context + response

        self.logger.info('\n*End log*')
        print('Exiting')

    def __prompt_gpt(self, prompt):
        '''
        Prompt GPT-3

        Input: prompt - string
        Returns: text from the model
        '''
        print('Calling GPT-3...')
        openai.api_key = self.secret_key
        response = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = prompt,
            temperature = 0.6,
            max_tokens = 150
        )
        return response.choices[0].text

    def __listen(self):
        '''
        Listen for user input

        Returns: transcription of the user's spoken input
        THrows 
        '''
        while 1:
            try:
                with sr.Microphone() as source:
                    # Adjust for ambient noise
                    self.recog.adjust_for_ambient_noise(source, duration=1)

                    # Listen
                    print('listening...')
                    audio = self.recog.listen(source)

                    # speech to text
                    MyText = self.recog.recognize_google(audio)
                    return MyText

            except sr.RequestError as e:
                # Error such as exhausting quota for requests
                msg = f'Could not request results due to error: {e}'
                print(msg)
                self.logger.error(msg)
                raise ConnectionError
         
            except sr.UnknownValueError:
                # Silence
                continue

    def __respond(self, text):
        '''
        Text to speech

        Uses TTS to translate text to speech stored in a temporary wav file.
        Then play wav file, and delete.

        Input: text, string

        '''
        print('Speaking...')
        out_path = os.path.join(os.getcwd(), 'output.wav')

        # Generate wav file
        self.tts.tts_to_file(text=text, 
                    speaker=self.tts.speakers[0], 
                    language=self.tts.languages[0], 
                    file_path=out_path)
    
        # play and delete
        wave_obj = sa.WaveObject.from_wave_file(out_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        os.remove(out_path)


def main():
    # initialize logging
    now = datetime.now()
    logfile = f'chatlog-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
    logpath = os.path.join('logs', logfile)
    logging.basicConfig(filename=logpath, 
                        level=logging.INFO, 
                        format='%(message)s')
    logger = logging.getLogger()

    # If prestext file exists, load it
    if os.path.exists('pretext.txt'):
        with open('pretext.txt', 'r') as PRETEXT:
            pretext = PRETEXT.read()
            pretext = pretext.replace('\n', ' ')

    # Inistantiate GPTChat and run loop
    gpt_chat = GPTChat(logger, pretext=pretext)
    gpt_chat.loop()


if __name__ == '__main__':
    main()
