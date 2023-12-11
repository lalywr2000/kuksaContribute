# CAN Feeder
The purpose of this implementation is to input data received via CAN into a `KUKSA.val` databroker. By mapping incoming CAN data based on CAN IDs to their corresponding VSS representations, it is possible to provide data to the data broker via the kuksa_client.

## Usage
The feeder requires an installation of Python in version 3 and can be executed with the following commands:

```
pip install kuksa-client
pip install python-can

python3 can2val.py
```

This assumes a running `KUKSA.val` databroker at `127.0.0.1:55555`. Also the CAN communication in the device must be in a valid state.

This was successfully tested on Raspberry Pi 4B with Raspbian 11 (bullseye) and 2-CH CAN FD HAT