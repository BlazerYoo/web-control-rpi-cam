import os
from time import sleep
from flask import Flask, request, render_template
from markupsafe import escape
from gpiozero import Servo
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
    panServoAngle = -1
    tiltServoAngle = -1
    panServo.value = panServoAngle
    tiltServo.value = tiltServoAngle


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    global panServo
    global tiltServo
    global panServoAngle
    global tiltServoAngle
    interval = 0.08
    if request.method == "POST":
        direction = escape(request.form.get("direction"))
        print(direction)
        if 'up' in direction.lower():
            if (tiltServoAngle + interval) >= 1:
                tiltServoAngle = 1
            else:
                tiltServoAngle += interval
            tiltServo.value = tiltServoAngle
        elif 'down' in direction.lower():
            if (tiltServoAngle - interval) <= -1:
                tiltServoAngle = -1
            else:
                tiltServoAngle -= interval
            tiltServo.value = tiltServoAngle
        elif 'left' in direction.lower():
            if (panServoAngle + interval) >= 1:
                panServoAngle = 1
            else:
                panServoAngle += interval
            panServo.value = panServoAngle
        else:
            if (panServoAngle - interval) <= -1:
                panServoAngle = -1
            else:
                panServoAngle -= interval
            panServo.value = panServoAngle
            
        print("PAN:", panServoAngle, "TILT:", tiltServoAngle)

    return render_template('home.html')


if __name__ == '__main__':
    init()
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)