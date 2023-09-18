from setuptools import setup, find_packages

setup(
    name='chameleondump',
    version='0.1.5',
    description="Dump RFID tag IDs from ChameleonUltra devices",
    packages=find_packages(),
    author='Ron Masas',
    url='https://github.com/masasron/chameleondump',
    install_requires=[
        'bleak==0.21.0',
        'termcolor==2.3.0',
    ],
    entry_points={
        'console_scripts': [
            'chameleondump = chameleondump.chameleondump:cli',
        ],
    },
    license='GNU GPLv3',
    keywords = ['RFID', 'NFC', 'ChameleonUltra', 'ChameleonMini', 'BLE', 'Bluetooth'],
)