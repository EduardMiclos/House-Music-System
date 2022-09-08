import multiprocessing
from ctypes import c_wchar_p

from Adapters.VoiceCommandAdapter import VoiceCommandAdapter
from MusicManager.MusicManager import MusicManager
from VoiceRecognition.VoiceListener import VoiceListener

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
            "PLAY_GENRE": ['play genre', self.play_genre],
            "PLAY_SONG": ['play song', self.play_song],
            "FULL_REFRESH": ['make a full refresh', self.full_refresh],
            "HITS_REFRESH": ['refresh the hits', self.refresh_hits],
            "DOWNLOAD": ['download new songs', self.download],
            "PAUSE": ['pause', self.pause],
            "STOP": ['stop', self.stop],
            "TURN_OFF": ['turn off', self.turn_off]
        }

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
        voice_listener = multiprocessing.Process(target = VoiceListener.listen, args = (interrupt_signal, self.input_command), daemon = False) 
        voice_listener.start()

        # This process executes all the commands. It can be interrupted at any time.
        command_executer = multiprocessing.Process(daemon = False)

        while self.SYSTEM_ON:
            interrupt_signal.wait()

            if command_executer.is_alive():
                command_executer.kill()

            callback = self.voice_adapter.interpret(command = self.input_command.value, fallback = self.unknown_command)
            
            command_executer = multiprocessing.Process(target = callback, daemon = True)
            command_executer.start()

            interrupt_signal.clear()
        
    def play_genre(self) -> None:
        self.voice_adapter.speak('Please pick a genreaa asdf sdf wefsdf efsdf srdsd sd sd sdrsd fsdfsdfsdf sdr sd r')

    def play_song(self) -> None:
        self.voice_adapter.speak('Please pick a song')

    def full_refresh(self) -> None:
        self.voice_adapter.speak('Refreshing all songs')

    def refresh_hits(self) -> None:
        self.voice_adapter.speak('Refreshing all the hits')

    def download(self) -> None:
        self.voice_adapter.speak('Downloading new songs')

    def pause(self) -> None:
        self.voice_adapter.speak('Pausing')

    def stop(self) -> None:
        self.voice_adapter.speak('Stopping')

    def unknown_command(self) -> None:
        self.voice_adapter.speak('I\'m sorry. I don\'t understand what you\'re saying')

    def turn_off(self) -> None:
        self.voice_adapter.speak('Turning off. Goodbye!')

        self.SYSTEM_ON = False


ms = MusicSystem()
ms.turn_on()
