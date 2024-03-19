
from flask import Flask, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture("rtsp://admin:instar@192.168.1.32:554/12")

def genFrames():
  while True:
    success, frame = camera.read()

    if not success:
      break
    else:
      ret, buffer = cv2.imencode('.jpg', frame)
      frame = buffer.tobytes()
      yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/videoFeed')
def videoFeed():
  return Response(genFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
  app.run(threaded=False, processes=3, host='192.168.1.10', port='1111')