import multiprocessing
from ctypes import c_wchar_p
import signal
import os

from Adapters.VoiceCommandAdapter import VoiceCommandAdapter
from MusicManager.MusicManager import MusicManager
from VoiceRecognition.VoiceListener import VoiceListener
from VoiceRecognition.VoiceCommand import VoiceCommand

class MusicSystem:
    def __init__(self) -> None:
        # List of the UUIDs of all the available Bluetooth Devices.
        self.bluetooth_devices =  {
            "JBL_GO3_1": '2C:FD:B4:38:5D:CA',
            "JBL_GO3_2": '', # Need to buy it first.
            "MICROPHONE_UUID": '' # Need to but it first.
        }

        # List of all the voice commands along with the corresponding function pointers.
        self.voice_cmds = {
            "PLAY_GENRE": VoiceCommand(text = 'play genre', callback = self.play_genre, audio_path = 'Database/dialogue_answers/play_genre.mp3'),
            "PLAY_SONG": VoiceCommand(text = 'play song', callback = self.play_song, audio_path = 'Database/dialogue_answers/play_song.mp3'),
            "FULL_REFRESH": VoiceCommand(text = 'full refresh', callback = self.full_refresh, audio_path = 'Database/dialogue_answers/full_refresh.mp3'),
            "HITS_REFRESH": VoiceCommand(text = 'refresh hits', callback = self.refresh_hits, audio_path = 'Database/dialogue_answers/hits_refresh.mp3'),
            "DOWNLOAD": VoiceCommand(text = 'download new songs', callback = self.download, audio_path = 'Database/dialogue_answers/download.mp3'),
            "PAUSE": VoiceCommand(text = 'pause', callback = self.pause, audio_path = 'Database/dialogue_answers/pause.mp3'),
            "STOP": VoiceCommand(text = 'stop', callback = self.stop, audio_path = 'Database/dialogue_answers/stop.mp3'),
            "TURN_OFF": VoiceCommand(text = 'turn off', callback = self.turn_off, audio_path = 'Database/dialogue_answers/turn_off.mp3') 
        }
        self.fallback_cmd = VoiceCommand(callback = self.unknown_command, audio_path = 'Database/dialogue_answers/unknown_command.mp3')

        self.music_manager = MusicManager()
        self.voice_adapter = VoiceCommandAdapter(voice_cmds = self.voice_cmds.items())

        self.SYSTEM_ON = False
        self.input_command = None

    def turn_on(self) -> None:
        self.SYSTEM_ON = True 
        self.input_command = multiprocessing.Manager().Value(c_wchar_p, '')

        # This signal is used for communication between the current thread and voice_listener thread.
        interrupt_signal = multiprocessing.Event()

        # This process takes input commands from the user.
        voice_listener = multiprocessing.Process(target = VoiceListener.listen, args = (interrupt_signal, self.input_command)) 
        voice_listener.start()

        # This process executes all the commands. It can be interrupted at any time.
        command_executer = None

        while self.SYSTEM_ON:
            interrupt_signal.wait()

            if command_executer is not None and command_executer.is_alive():
                self.interrupt()
                command_executer.terminate()

            voice_command = self.voice_adapter.interpret(command = self.input_command.value, fallback = self.fallback_cmd) 
            print(voice_command.audio_path)
            command_executer = multiprocessing.Process(target = voice_command.callback, args = (voice_command.audio_path,), daemon = False)
            command_executer.start()

            interrupt_signal.clear()
    
    def interrupt(self) -> None:
        # Killing the mp123 process instantly.
        os.system('pkill mpg123')

    def turn_off(self) -> None:
        self.SYSTEM_ON = False

    def play_genre(self, path) -> None:
        self.voice_adapter.speak(path)

    def play_song(self, path) -> None:
        self.voice_adapter.speak(path)

    def full_refresh(self, path) -> None:
        self.voice_adapter.speak(path)

    def refresh_hits(self, path) -> None:
        self.voice_adapter.speak(path)

    def download(self, path) -> None:
        self.voice_adapter.speak(path) 

    def pause(self, path) -> None:
        self.voice_adapter.speak(path)

    def stop(self, path) -> None:
        self.voice_adapter.speak(path)

    def unknown_command(self, path) -> None:
        self.voice_adapter.speak(path)


ms = MusicSystem()
ms.turn_on()
