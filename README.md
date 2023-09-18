# ChameleonDump

## Overview

ChameleonDump is a user-friendly command-line tool developed exclusively for
macOS. Its primary function is to spotlight the security vulnerabilities that
arise from using hardcoded, default BLE (Bluetooth Low Energy) PIN codes.
Specifically, the tool attempts to connect to ChameleonUltra devices using their
default BLE PIN codes. Once connected, ChameleonDump mimics the actions of the
native app, extracting all stored RFID tag IDs from the device. As of now, the
tool supports only the ChameleonUltra device, but there are plans to extend its
capabilities to other devices in the future.

**⚠️ Note: This tool is designed for educational purposes only. Please use it
responsibly and only on devices you own or have explicit permission to test.**

## What Can You Do?

### For Developers

Multiple solutions exist for mitigating this security risk. The most
straightforward approach would be to require users to change the default PIN
when they first set up the device.

### For Users

If the system doesn't make changing the default PIN mandatory, it's strongly
recommended that you do so yourself to enhance your device's security.

## Installation

### Prerequisites

- macOS (The tool is not supported on other operating systems)
- Python 3.6 or higher
- pip package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/masasron/chameleondump
   ```

2. Navigate to the project directory:
   ```bash
   cd chameleondump
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use ChameleonDump, execute the following command:

```bash
python main.py --device <Device_Name> [--pin <PIN>]
```

### Options

- `--device`: An optional argument specifies the target device you wish to
  connect to.
- `--pin`: An optional argument specifying the PIN used for pairing. If not
  provided, the default PIN will be used.

### Supported Devices

- ChameleonUltra
