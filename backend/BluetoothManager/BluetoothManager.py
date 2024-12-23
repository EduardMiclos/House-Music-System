import subprocess
from subprocess import CalledProcessError
from typing import List
from threading import Timer

class BluetoothManager:
    def __init__(self, target_uuid) -> None:
        self.target_uuid = target_uuid
        self.device_name = None
        self.is_connected = False

    def get_device_name(self):
        if self.device_name is None:
            device_info = self.get_device_info()
            self.device_name = device_info[1]
            self.device_name = self.device_name.split(':')[1].strip()
        return self.device_name

    def try_connect(self, target_uuid = None) -> bool:
        if self.is_connected():
            print('The device is already connected!')
            return True
        
        if target_uuid is not None:
            self.target_uuid = target_uuid

        try:
            # Restarting pulse audio s.t. we are able to connect to the device.
            pulseaudio_status = subprocess.run(['pulseaudio', '--check'], stdout=subprocess.DEVNULL) 

            if pulseaudio_status.returncode == 0:
                subprocess.run(['pulseaudio', '--kill'], check = True)

            subprocess.run(['pulseaudio', '--start'], check = True)
            
            subprocess.run(['bluetoothctl', 'connect', self.target_uuid], check = True)
            device_info = self.get_device_info()
            
            self.device_name = device_info[1]
            self.device_name = self.device_name.split(':')[1].strip()

            print(f'Successfully connected to device: {self.device_name}')
            return True
        except CalledProcessError as cpe:
            print(f'Failure: Couldn\' connect to device. Process return code: {cpe.returncode}')
            print(f'Process output: {cpe.output}')

            return False

    def disconnect(self) -> bool:
        if not self.is_connected():
            print('The device is not connected!')
            return True

        try:
            subprocess.run(['bluetoothctl', 'disconnect', self.target_uuid], check = True)
            print(f'Successfully disconnected from device: {self.device_name}')

            self.target_uuid = None
            self.device_name = None

            return True
        except CalledProcessError as cpe:
            print(f'Failure: Couldn\' disconnect from device. Process return code: {cpe.returncode}')
            print(f'Process output: {cpe.output}')

            return False

    def get_device_info(self) -> List[str]:
        process = subprocess.run(['bluetoothctl', 'info', self.target_uuid], capture_output = True)
        str_process = str(process.stdout)

        if "not available" in str_process:
            return None

        return str_process.split('\\n\\t')

    def check_if_connected(self) -> bool:
        device_info = self.get_device_info()
        is_connected = ""

        if device_info is not None:
            is_connected = device_info[8]
        
        self.is_connected = True if 'yes' in is_connected else False
        return self.is_connected
