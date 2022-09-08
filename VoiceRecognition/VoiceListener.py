import multiprocessing
import time
import random

texts = ['play genre', 'play song', 'wrongcmd', 'ackabacka', 'play', 'pasadaseas', 'download']

class VoiceListener:

    @staticmethod
    def listen(event: multiprocessing.Event, input_command: multiprocessing.Array) -> None:
        while True:
            time.sleep(2)
            print('Waiting for command...')
            input_command.value = random.choice(texts)
            print(f'Command is: {input_command.value}')
            event.set()

