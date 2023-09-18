import asyncio
import subprocess
from bleak import BleakScanner

async def find_device(device_name):
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == device_name:
            return d.address
    return None

def pair_macos_bluetooth_device(device_name, pin):
    script  = """
    tell application "System Events"
        tell process "BluetoothUIServer"
            delay 1
            set value of text field 1 of window "Connection Request from: {}" to "{}"
            click button "Connect" of window "Connection Request from: {}"
        end tell
    end tell
    """
    subprocess.run(["osascript", "-e", script.format(device_name, pin, device_name)], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

async def is_macos_bluetooth_pairing_dialog_active(loop, timeout=4):
    end_time = loop.time() + timeout
    while True:
        try:
            result = subprocess.run(["pgrep", "BluetoothUIServer"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.stdout:
                return True
        except subprocess.CalledProcessError:
            pass

        if (loop.time() + 0.1) >= end_time:
            return False

        await asyncio.sleep(0.1)