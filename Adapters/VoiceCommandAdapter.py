import sys, os
import Levenshtein

class VoiceCommandAdapter:
    def __init__(self, voice_cmds) -> None:
        self.voice_cmds = voice_cmds

    def interpret(self, command: str) -> bool: 
        cmds_dict = {cmd_text:Levenshtein.distance(command, cmd_voice) for cmd_text, cmd_voice in self.voice_cmds}
        print(min(cmds_dict, key = cmds_dict.get))

