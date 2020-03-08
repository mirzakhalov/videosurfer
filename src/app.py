from flask import Flask, request, render_template, send_from_directory
from pytube import YouTube
import sys
sys.path.append('../')

import process
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

videos = []

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/other", methods=['PUT', 'POST'])
def other():
    if request.method == 'POST':
        yt = YouTube(request.data.decode("utf-8"))
        videos.append(yt.streams.filter(resolution='720p', file_extension='mp4')[0].download())
        print(videos)
    else:
        filename = request.files['video'].filename
        request.files['video'].save(filename)
        process.video_to_frames(filename, f"{filename.split('.')[0]}/")
        os.remove(filename)
        # videos.append(request.files['video'])

    return "Success"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='./static/favicon.icon')
                               

if __name__ == '__main__':
    app.run()