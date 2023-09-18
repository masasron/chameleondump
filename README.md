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

Change the default PIN code of your ChameleonUltra device.

## Installation

### Prerequisites

- macOS (The tool is not supported on other operating systems)
- Python 3.6 or higher
- pip package manager

### Installing from PyPI

```bash
pip install chameleondump
```

## Usage

```bash
usage: chameleondump [-h] [--device {ChameleonUltra}] [--pin PIN] [--mask MASK]

ChameleonDump

optional arguments:
  -h, --help            show this help message and exit
  --device {ChameleonUltra}
                        The target device
  --pin PIN             The PIN to use for pairing, leave empty to use the default PIN
  --mask MASK           Mask the RFID tag IDs
```

### Building & Installing from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/masasron/chameleondump
   ```

2. Navigate to the project directory:
   ```bash
   cd chameleondump
   ```

3. Build & Install
   ```bash
   python3 setup.py sdist bdist_wheel
   pip3 install dist/chameleondump-0.1.5-py3-none-any.whl
   ```
   **Note:** The name of the wheel file may vary depending on the version of the
   tool.

### Supported Devices

- ChameleonUltra
