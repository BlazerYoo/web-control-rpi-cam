import os
from time import sleep
from flask import Flask, render_template, request, Response
from markupsafe import escape
from camera_pi import Camera

app = Flask(__name__)

# Global variables definition and initialization
global panServoAngle
global tiltServoAngle
panServoAngle = 0
tiltServoAngle = 0

panPin = 27
tiltPin = 17


@app.route("/",methods=["POST","GET"])
def home():
	if request.method == "POST":
		direction = escape(request.form.get("direction"))
		print(direction)
		if 'up' in direction.lower():
			tiltServoAngle += 10
		elif 'down' in direction.lower():
			tiltServoAngle -= 10
		elif 'left' in direction.lower():
			panServoAngle -= 10
		else:
			panServoAngle += 10

		os.system("python angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))

		os.system("python angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))

	return render_template('home.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)