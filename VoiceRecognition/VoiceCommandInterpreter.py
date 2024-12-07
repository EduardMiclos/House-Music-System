import sys, os
import Levenshtein
import time

MAX_LEVENSHTEIN_DISTANCE_ERROR = 3

class VoiceCommandInterpreter:
    def __init__(self, voice_cmds) -> None:
        self.voice_cmds = voice_cmds

    # Return a function based on the voice command.
    def interpret(self, command: str, fallback: object) -> object: 
        cmds_dict = {cmd_text:[Levenshtein.distance(command, voice_command.text), voice_command] for cmd_text, voice_command in self.voice_cmds}

        min_key = None
        min_val = MAX_LEVENSHTEIN_DISTANCE_ERROR
        for key, val in cmds_dict.items():
            if val[0] < min_val:
                min_val = val[0]
                min_key = key

        if min_key is None:
            return fallback
        return cmds_dict[min_key][1]


    # This function represent the speaking mechanism of the Raspberry Pi.
    def speak(self, voice_path: str) -> bool:
        os.system(f'mpg123 {voice_path}')
