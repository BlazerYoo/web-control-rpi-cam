# web control rpi cam

Websockets for low pan-and-tilt servo latency with Raspberry Pi camera streaming

## Usage

Run `git clone https://github.com/BlazerYoo/file2img.git` or [download](https://github.com/BlazerYoo/web-control-rpi-cam/archive/refs/heads/main.zip) repo.

Run `pip install -r requirements.txt` to install dependencies.

Run `sudo python appV2.py`

Run `python app_move.py`

Or edit `/home/pi/.bashrc` and add `sudo python appV2.py & python app_move.py`

Open `client.html` on a browser on device in same local network as your Raspberry Pi

## Credits

`camera_pi.py` from https://medium.com/@rovai/raspberry-pi-cam-pan-tilt-controlled-over-local-internet-49ecad3a5ee8

Setting up servo in `app_move.py` adapted from https://github.com/garyexplains/examples/blob/master/servo/sweep0.py

Python websocket in `app_move.py` and `client.html` adapted from https://websockets.readthedocs.io/en/stable/intro/tutorial1.html and https://www.piesocket.com/blog/python-websocket