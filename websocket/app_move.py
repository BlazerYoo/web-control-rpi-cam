import asyncio
import websockets
import os
from gpiozero import Servo
from gpiozero import PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory

def init():
    os.system("sudo pigpiod")
    factory = PiGPIOFactory()
    global panServo
    global tiltServo
    global panServoAngle
    global tiltServoAngle
    panServo = Servo(27, min_pulse_width=0.6/1000, max_pulse_width=2.7/1000, pin_factory=factory)
    tiltServo = Servo(17, min_pulse_width=0.5/1000, max_pulse_width=2.4/1000, pin_factory=factory)
    panServoAngle = 0
    tiltServoAngle = -1
    panServo.value = panServoAngle
    tiltServo.value = tiltServoAngle

    global led
    led = PWMLED(22)
    led.value = 0

async def handler(websocket):
    async for message in websocket:
        #print(message)
        global panServo
        global tiltServo
        global panServoAngle
        global tiltServoAngle
        #global led
        interval = 0.01
        if 'up' in message.lower():
            if (tiltServoAngle + interval) >= 1:
                tiltServoAngle = 1
            else:
                tiltServoAngle += interval
            tiltServo.value = tiltServoAngle
        elif 'down' in message.lower():
            if (tiltServoAngle - interval) <= -1:
                tiltServoAngle = -1
            else:
                tiltServoAngle -= interval
            tiltServo.value = tiltServoAngle
        elif 'left' in message.lower():
            if (panServoAngle + interval) >= 1:
                panServoAngle = 1
            else:
                panServoAngle += interval
            panServo.value = panServoAngle
        elif 'right' in message.lower():
            if (panServoAngle - interval) <= -1:
                panServoAngle = -1
            else:
                panServoAngle -= interval
            panServo.value = panServoAngle
        elif 'ledon' in message.lower():
            led.value = 0.75
        elif 'ledoff' in message.lower():
            led.value = 0
        elif 'power' in message.lower():
            await websocket.send("POWERING OFF...")
            os.system("sudo shutdown -h now")
            
        #print("PAN:", panServoAngle, "TILT:", tiltServoAngle)
        

async def main():
    async with websockets.serve(handler, "", 8000):
        await asyncio.Future()

if __name__ == "__main__":
    init()
    asyncio.run(main())
