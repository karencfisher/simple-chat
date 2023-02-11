import json

import vosk
import pyaudio
import numpy as np

class SpeechRecognize:
    def __init__(self):
        with open('vosk_config.json', 'r') as FP:
            self.config = json.load(FP)
        vosk.SetLogLevel(-1)
        model = vosk.Model(self.config['model'])
        self.recognizer = vosk.KaldiRecognizer(model, 16000)

    def speech_to_text(self):
        print('\rListening...      ', end='')
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels = self.config['channels'],
                        rate=self.config['rate'],
                        input=True,
                        frames_per_buffer=self.config['chunk'])
        frames = []

        for i in range(0, int(self.config['rate'] / self.config['chunk'] * 5)):
            data = stream.read(self.config['chunk'])
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        audio = np.frombuffer(b''.join(frames), dtype=np.int16)
        self.recognizer.AcceptWaveform(audio.tobytes())
        result = json.loads(self.recognizer.Result())
        return result['text']
        
