
from fuzzywuzzy import fuzz
import json
import pyrebase
import cv2
import imutils


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
        print(stg_loc)
        img = imutils.url_to_image(stg_loc)
        cv2.imwrite('./search.jpg', img)
        # retrieve the image
        ebay = db.child(f'{filename}/ebay/{frame_id}').get()
        for key, item in ebay.val().items():
            print(key)
            for key2, bb in item.items():
                print(bb)
                new_img = img[bb['y_min']:bb['y_max'], bb['x_min']:bb['x_max']]
                # generate boxes and upload


        # return the second of the video
        return 2*frame_id, urls
        