
from fuzzywuzzy import fuzz
import json
import pyrebase

config = json.loads(open('secret/config.json').read())
firebase = pyrebase.initialize_app(config)

# # build paths
db = firebase.database()
stg = firebase.storage()


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
        for frame in frames.each():
            corr = fuzz.token_sort_ratio(input, frame.val()['caption'])
            if corr > max_corr:
                max_corr = corr
                frame_id = int(frame.key())
        
        print(frame_id)
        # retrieve the image
        ebay = db.child(filename + "/ebay/").get()
        for stuff in ebay.each():
            for key, item in ebay.val().items():
                if str(frame_id) in ebay.val()[key]:
                    boxes = ebay.val()[key][str(frame_id)]
                    print(boxes)
                    # generate boxes and upload


        # return the second of the video
        return 2*frame_id, urls
        