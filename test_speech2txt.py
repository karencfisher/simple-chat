import speech_recognition as sr

r = sr.Recognizer()

while 1:
    try:
         
        # use the microphone as source for input.
        with sr.Microphone() as source2:
             
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=1)
             
            #listens for the user's input
            print('listening...')
            audio2 = r.listen(source2)
            print('heard...')
             
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            print(f'I said: {MyText}')

            if MyText != '':
                break
             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        continue