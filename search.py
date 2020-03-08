
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


class Search:
    def __init__(self):
        pass
    


    def search_transcript(self, input):
        pass

    

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
        