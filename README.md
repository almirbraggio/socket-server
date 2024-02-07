# socket-server

Python socket server to decode message from telemetry devices like Suntech ST300 and VDO. This is an asynchronous socket TCP implementation with Python and Gevent.

# Requirements

Please check python version.
Tested with:

- Python 3.8
- Pip 20.0.2

To use this code, install `libevent-dev` with sudo:

```bash
apt update
apt install libevent-dev
```

Clone the project, ctivate virtual environment and install python requirements:

```bash
git clone git@github.com:almirbraggio/socket-server.git
cd socket-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

# Author

Almir A. Braggio
