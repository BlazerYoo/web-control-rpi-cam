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
    panServo = Servo(27, min_pulse_width=0.6/1000,
                     max_pulse_width=2.7/1000, pin_factory=factory)
    tiltServo = Servo(17, min_pulse_width=0.5/1000,
                      max_pulse_width=2.4/1000, pin_factory=factory)
    panServoAngle = 0
    tiltServoAngle = -1
    panServo.value = panServoAngle
    tiltServo.value = tiltServoAngle

    global led1
    global led2
    global led3
    global led4
    led1 = PWMLED(22)
    led1.value = 0
    led2 = PWMLED(10)
    led2.value = 0
    led3 = PWMLED(9)
    led3.value = 0
    led4 = PWMLED(11)
    led4.value = 0


async def handler(websocket):
    async for message in websocket:
        # print(message)
        global panServo
        global tiltServo
        global panServoAngle
        global tiltServoAngle
        global led1
        global led2
        global led3
        global led4
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
        elif 'ledoff' in message.lower():
            led1.value = 0
            led2.value = 0
            led3.value = 0
            led4.value = 0
        elif 'lumin' in message.lower():
            led1.value = int(message.split(" ")[1]) / 100
            led2.value = int(message.split(" ")[1]) / 100
            led3.value = int(message.split(" ")[1]) / 100
            led4.value = int(message.split(" ")[1]) / 100
        elif 'power' in message.lower():
            await websocket.send("POWERING OFF...")
            os.system("sudo shutdown -h now")

        # print("PAN:", panServoAngle, "TILT:", tiltServoAngle)


async def main():
    async with websockets.serve(handler, "", 8000):
        await asyncio.Future()

if __name__ == "__main__":
    init()
    asyncio.run(main())
