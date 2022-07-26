from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setServoAngle(servo, angle, a, b):
	pwm = GPIO.PWM(servo, 50)
	pwm.start(8)
	dutyCycle = angle * (b-a) / 180 + a
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.3)
	pwm.stop()

if __name__ == '__main__':
	import sys
	servo = int(sys.argv[1])
	GPIO.setup(servo, GPIO.OUT)
	setServoAngle(servo, int(sys.argv[2]), 1, 13)
	GPIO.cleanup()