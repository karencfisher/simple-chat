import os
import openai
from dotenv import dotenv_values
import speech_recognition as sr
from TTS.api import TTS
import simpleaudio as sa


class GPTChat:
    def __init__(self):
        self.secret_key = os.getenv('SECRET_KEY')
        self.recog = sr.Recognizer()
        model_name = TTS.list_models()[0]
        self.tts = TTS(model_name)

    def loop(self):
        text = ''
        while text != 'goodbye':
            text = self.__listen()
            response = self.__prompt_gpt(text)
            self.__respond(response)

        print('Exiting')

    def __prompt_gpt(self, prompt):
        openai.api_key = self.secret_key
        response = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = prompt,
            temperature = 0.6,
            max_tokens = 150
        )
        return response.choices[0].text

    def __listen(self):
        while 1:
            try:
                # use the microphone as source for input.
                with sr.Microphone() as source2:
                    self.recog.adjust_for_ambient_noise(source2, duration=0.2)
                    
                    #listens for the user's input
                    print('listening...')
                    audio2 = self.recog.record(source2, duration=5)

                    # Using google to recognize audio
                    MyText = self.recog.recognize_google(audio2)

                    if MyText != '':
                        return MyText

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
         
            except sr.UnknownValueError:
                continue

    def __respond(self, text):
        out_path = os.path.join(os.getcwd(), 'output.wav')
        self.tts.tts_to_file(text=text, 
                    speaker=self.tts.speakers[0], 
                    language=self.tts.languages[0], 
                    file_path=out_path)
    
        wave_obj = sa.WaveObject.from_wave_file(out_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()

        os.remove(out_path)


def main():
    gpt_chat = GPTChat()
    gpt_chat.loop()


if __name__ == '__main__':
    main()
