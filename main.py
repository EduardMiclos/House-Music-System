import multiprocessing
from ctypes import c_wchar_p
import os

from BluetoothManager.BluetoothManager import BluetoothManager
from MusicManager.MusicManager import MusicManager

class MusicSystem:
    def __init__(self) -> None:
        
        # The MAC address of the bluetooth speaker.
        self.bluetooth_device = "2C:FD:B4:38:5D:CA"

        self.music_manager = MusicManager()

        self.SYSTEM_ON = False
        self.input_command = None

    def turn_on(self) -> None:
        self.SYSTEM_ON = True 
        self.input_command = multiprocessing.Manager().Value(c_wchar_p, '')

        # This signal is used for communication between the current thread and voice_listener thread.
        interrupt_signal = multiprocessing.Event()

        # This process takes input commands from the user.

        # This process executes all the commands. It can be interrupted at any time.
        command_executer = None

        while self.SYSTEM_ON:
            interrupt_signal.wait()

            if command_executer is not None and command_executer.is_alive():
                self.interrupt()
                command_executer.terminate()


ms = MusicSystem()
# ms.turn_on()

bluetooth_manager = BluetoothManager(ms.bluetooth_device)
is_connected = bluetooth_manager.connect()

if is_connected:
    music_manager = MusicManager()

    while True:
        x = int(input('Enter 1 [play] or 2 [stop]'))
        
        if x == 1:
            music_manager.play(genre='romantic')
        if x == 2:
            music_manager.stop()


