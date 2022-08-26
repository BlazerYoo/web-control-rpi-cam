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
    global led5
    global led6
    global led7
    global led8
    global led9
    global led10
    global powerLed

    led1 = PWMLED(22)
    led1.value = 0
    led2 = PWMLED(10)
    led2.value = 0
    led3 = PWMLED(9)
    led3.value = 0
    led4 = PWMLED(11)
    led4.value = 0
    led5 = PWMLED(5)
    led5.value = 0
    led6 = PWMLED(6)
    led6.value = 0
    led7 = PWMLED(13)
    led7.value = 0
    led8 = PWMLED(19)
    led8.value = 0
    led9 = PWMLED(26)
    led9.value = 0
    led10 = PWMLED(16)
    led10.value = 0
    powerLed = PWMLED(21)
    powerLed.value = 1


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
        global led5
        global led6
        global led7
        global led8
        global led9
        global led10
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
            led5.value = 0
            led6.value = 0
            led7.value = 0
            led8.value = 0
            led9.value = 0
            led10.value = 0
        elif 'lumin' in message.lower():
            lumin = int(message.split(" ")[1]) / 100
            led1.value = lumin
            led2.value = lumin
            led3.value = lumin
            led4.value = lumin
            led5.value = lumin
            led6.value = lumin
            led7.value = lumin
            led8.value = lumin
            led9.value = lumin
            led10.value = lumin
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
