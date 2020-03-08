
from fuzzywuzzy import fuzz
import json
import pyrebase
import cv2
import imutils
import requests
import base64


config = json.loads(open('secret/config.json').read())
firebase = pyrebase.initialize_app(config)

# # build paths
db = firebase.database()
stg = firebase.storage()

API_ENDPOINT = "https://api.imgur.com/3/image"
  
# your API key here 
headers = {'Authorization': 'Bearer 120517490a8a9e9aa415106ce3694339da0c90c9'}

def back_track(times, curr_ind, curr_val, prev_chain=[]):
    size = len(times)
    new_res = []

    if curr_ind < size - 1:
        for time_b in times[curr_ind + 1]:
            if curr_val[1] + 1 < time_b[0]:
                break

            if curr_val[1] <= time_b[0] and curr_val[1] >= time_b[0] - 1:
                new_res.append(back_track(times, curr_ind + 1, time_b, prev_chain + [curr_val]))

        return max(new_res, key=len) if new_res != [] else prev_chain + [curr_val]
    
    else:
        return prev_chain + [curr_val]
    
    return prev_chain + [curr_val] 


class Search:
    def __init__(self):
        pass

    def search_transcript(self, filename, inp):
        words = [''.join(list(filter(str.isalpha, w))).lower() for w in inp.split(' ')]
        times = [[(int(key)/10, int(value)/10) for key, value in db.child(f'{filename}/transcript/{word}').get().val().items()] for word in words]

        new_res = []
        for i, time in enumerate(times[0]):
            new_res.append(back_track(times, 0, time))
        
        path = max(new_res, key=len)

        return path[0][0]


    def search_caption(self, filename, inp):
        frames = db.child(filename + "/frames/").get()
        max_corr = 0
        frame_id = 0
        for frame in frames.each():
            corr = fuzz.token_sort_ratio(inp, frame.val()['caption'])
            if corr > max_corr:
                max_corr = corr
                frame_id = int(frame.key())

        # return the second of the video
        return 2*frame_id
        
    

    def search_shopping(self, filename, inp):
        frame_id = int(self.search_caption(filename, inp) / 2)
        urls = []
        stg_loc = db.child(f'{filename}/frames/{frame_id}/storage_loc').get().val()
        img = imutils.url_to_image(stg_loc)
        cv2.imwrite('./search.jpg', img)
        # retrieve the image
        ebay = db.child(f'{filename}/ebay/{frame_id}').get()
        for key, item in ebay.val().items():
            for key2, bb in item.items():
                new_img = img[bb['y_min']:bb['y_max'], bb['x_min']:bb['x_max']]
                cv2.imwrite('search.jpg', new_img)
                b64_img = base64.standard_b64encode(open('search.jpg', 'rb').read())
                # generate boxes and upload
                data = {
                    "image": b64_img,
                    "title": f'{key2}.jpg'
                }

                session = requests.Session()
                response = session.post(API_ENDPOINT, headers=headers, data=data)

                if(response.status_code == 200):
                    urls.append(response.json()['data']['link'])
    
        # return the second of the video
        return 2*frame_id, urls
        