from flask import Flask, render_template, Response, redirect, url_for
from video_feed import generate_frames
from realtime_feed import generate_realtime_frames

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/realtime')
def realtime():
    return render_template('realtime.html')

@app.route('/realtime_feed')
def realtime_feed():
    return Response(generate_realtime_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
