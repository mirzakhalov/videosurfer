from flask import Flask, request, render_template, send_from_directory
from pytube import YouTube
import requests as req
import os
import math
from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup
import base64

import sys
sys.path.append('../')
import process

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
ID_APP = 'AhsanWah-MyApp-PRD-e69e8f5f8-f5a417a4'
empty_url_b64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAYEBAQFBAYFBQYJBgUGCQsIBgYICwwKCgsKCgwQDAwMDAwMEAwODxAPDgwTExQUExMcGxsbHCAgICAgICAgICD/2wBDAQcHBw0MDRgQEBgaFREVGiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICD/wAARCABQAFADAREAAhEBAxEB/8QAHAABAAEFAQEAAAAAAAAAAAAAAAUBAgQGBwMI/8QAPBAAAQMDAQQFBwoHAAAAAAAAAQIDBAAFERIGEyExByIykaE0QUJRYXGBFBUXQ1JidZOisSMzNVNUcpL/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8A+qaBQKBQKBQKBQKBQKBQa7eNoEWuO9MmPSNyJXyZtEdLJPY1jtj2Hz0EN9Jdl+3cfy4tA+kuy/buP5cWgyYm3EWYQIzd0czwBDUXHeeFBLSrk/GgqmuialhsanApMcLHDzJxxNBAfSXZft3H8uLQbRbJq5LjS0urXHkRW5LYdCAobzlnQB5qCToFAoNH2xhSLlbFxISd9INw3ugc93uinV7smg1hexka3Nh7aG6R7c2eIStaQpQ+6DxJ9mmgjZO3PRtZ8i3w3r1ITycUNyzkefK8rHwTQQF06ZNrJIU3bgxaWDwxGQC4R95xeo59oxQXdGO0s53bMM3OW5J+dmlxFOPrK+ueu0etn00gfGgz7lEMSc/HIxu1EAHnjmPCg7Ds35PbvwuN+1BPUHhOcebiOuM/zEpyM8eXPwoOcdIHSS1s1OTAVCeuMlxpL7brzgaj6VZAKUoyVciOOKDmd36WdtLgktNSk22OfqYKdz+vi5+qg1F5555xTry1OOr4qWslSifaTQWUCg9Ykl6JKZlMK0vMLS60r1KQdQPeKDsO2G5lrhXuOMR7owh8D1FY1cT68kj4UHR9m/J7d+Fxv2oJ6goQCMHiDzFBx3ptsZcsMK5JGXbW+qG8fOWnOs2fcMDvoOL0CgUCgUHVdkZXzx0cPRCcybE8dPH6h3LiSfjvAKDrGzfk9u/C437UE9QKDXNrrKm7W242oj+pRSGif8hnrNnvx3UHywpKkqKVDChwIPMGgpQKBQe0SHMmPBiIw5IfV2Wmklaj7kpyaDrnRRsLthbZst+4Q/ktumxlNLQ8oBesEKbVuxk8CMdbHOg6jZWkNKisoOpLUBlsE8+odPHuoJigUGJcwQwmQntR1BzgOOB2h8RQfNXSlZfmnba4NoTiPKV8rj45FL/WOPYF6hQQNsst3uru6tsN6W55wyhS8e8jgPjQb3ZOgna2bpXcXGbY0eYUd87/AMI6vesUG/2ToO2OgaVzd7c3hz3qtDefYhvHiTQb1b7XbbazuLfFaiM/22UJQPjpxQZVBGRGlN3iQn0d3lv3KVqP6iaCToFBRSUqSUq4pUMEe+g15eyezl3dZk3aA1MmW8GMhTuVJ0pOQCjsq4H0hQT0ePHjNJZjtIZZT2W20hKR7gOFB6UFCQBknAHM0GKq5xc6WtUhQ9FoavHs+NBQqujvZQiOnPNR1qx68Dq+NBfHh7t3fuOqeeKdBUcAYzngBQZNAoFBhKcRGuCy4oIakI1alEAa2+B7wRQVNybV5O2uR5soHVz/ALHAoGLo7zUiKn1J/iL7zhPhQVFsjE6ntT6gcguq1eHZ8KDKSlKRpSAlI5AUFaBQKBQKCxxlpzG8QleOWoA4oL6BQKBQKBQKD//Z"

videos = []

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/other", methods=['PUT', 'POST'])
def other():
    if request.method == 'POST':
        yt = YouTube(request.values['url'])
        videos.append(yt.streams.filter(resolution='720p', file_extension='mp4')[0].download(filename='you.mp4'))
        process.video_to_frames('you.mp4', f"you/")
        #print(videos)
        #description = request.values['description']
    else:
        filename = request.files['video'].filename
        request.files['video'].save(filename)
        process.video_to_frames(filename, f"{filename.split('.')[0]}/")

        # videos.append(request.files['video'])
        #description = request.values['description']
    return {} 

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='./static/favicon.icon')

@app.route("/get_ebay_products", methods=['POST'])
def get_ebay_products():
    def get_items(listOfItems):
        Keywords = listOfItems
        api = finding(appid=ID_APP, config_file=None)
        api_request = { 'keywords': Keywords }
        response = api.execute('findItemsByKeywords', api_request)
        soup = BeautifulSoup(response.content,'lxml')
        totalentries = int(soup.find('totalentries').text)
        items = soup.find_all('item')
        return items

    all_values = request.values['list'].split("-")
    display = []
    for value in all_values:    
        values = value.strip()
        if values == '':
            continue
        if values.find("size") > 0:
            values = values[0 : values.find("size") - 1]
        else:
            s = " "
            values = s.join(values.split(" ")[0 : math.ceil((len(values) + 1) / 2)])

        items = get_items(values)
        count = 0
        for item in items:
            if count == 3:
                break
            count += 1
            title = item.title.string
            price = int(round(float(item.currentprice.string)))
            url = item.galleryurl.string
            print(item)
            link = item.viewitemurl.string
            my_string = base64.b64encode(req.get(url).content)
            if my_string.decode("utf-8") == empty_url_b64:
                continue

            display.append({
                'title' : title,
                'url' : url,
                'price' : price,
                'link' : link
            })

    return {'list' : display}

if __name__ == '__main__':
    app.run()