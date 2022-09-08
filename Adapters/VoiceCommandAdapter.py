import sys, os
import Levenshtein
import speake3

MAX_LEVENSHTEIN_DISTANCE_ERROR = 3

class VoiceCommandAdapter:
    def __init__(self, voice_cmds) -> None:
        self.voice_cmds = voice_cmds    
        self.engine = speake3.Speake()

        self.espeake_configure()

    def espeake_configure(self):
        self.engine.set('voice', 'en')
        self.engine.set('speed', '190')
        self.engine.set('pitch', '40')

    # Return a function based on the voice command.
    def interpret(self, command: str, fallback: object) -> object: 
        cmds_dict = {cmd_text:[Levenshtein.distance(command, cmd_voice[0]), cmd_voice[1]] for cmd_text, cmd_voice in self.voice_cmds}

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
    def speak(self, text: str) -> bool:
        self.engine.say(text)
        self.engine.talkback()
