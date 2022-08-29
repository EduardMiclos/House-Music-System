import subprocess
from subprocess import CalledProcessError

class BluetoothManager:
    def __init__(self, target_uuid) -> None:
        self.target_uuid = target_uuid
        self.device_name = None

    def connect(self, target_uuid = self.target_uuid) -> bool:
        try:
            subprocess.run(['bluetoothctl', 'connect', target_uuid], check = True)
            process = subprocess.run(['bluetoothctl', 'info', self.target_uuid], check = True, capture_output = True)

            self.device_name = str(process.stdout).split('\\n\\t')[1]
            self.device_name = device_name.split(':')[1].strip()

            print(f'Successfully connected to device: {self.device_name}')
            return True
        except CalledProcessError as cpe:
            print(f'Failure: Couldn\' connect to device. Process return code: {cpe.returncode}')
            print(f'Process output: {cpe.output}')

            return False

    def disconnect(self) -> bool:
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



bm = BluetoothManager(target_uuid = '2C:FD:B4:38:5D:CA')
bm.connect()


