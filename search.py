
from fuzzywuzzy import fuzz
import json
import pyrebase
import requests

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

    

    def search_caption(self, filename, input):
        frames = db.child(filename + "/frames/").get()
        max_corr = 0
        frame_id = 0
        for frame in frames.each():

            corr = fuzz.token_sort_ratio(input, frame.val()['caption'])
            if corr > max_corr:
                max_corr = corr
                frame_id = int(frame.key())

        # return the second of the video
        return 2*frame_id
        
    

    def search_shopping(self, filename, input):
        frames = db.child(filename + "/frames/").get()
        max_corr = 0
        frame_id = 0
        urls = []
        for frame in frames.each():
            corr = fuzz.token_sort_ratio(input, frame.val()['caption'])
            if corr > max_corr:
                max_corr = corr
                frame_id = int(frame.key())
        
        print(frame_id)
        # retrieve the image
        # ebay = db.child(filename + "/ebay/").get()
        # for stuff in ebay.each():
        #     for key, item in ebay.val().items():
        #         if str(frame_id) in ebay.val()[key]:
        #             boxes = ebay.val()[key][str(frame_id)]
        #             print(boxes)
        #             # generate boxes and upload

                    # send post requests
        data = {
            "image": None
        }

        session = requests.Session()
        response = session.post(API_ENDPOINT, headers=headers, data=data)

        if(response.statusCode == 200):
            urls.append(response.json()['data']['link'])

        

        # return the second of the video
        return 2*frame_id, urls
        