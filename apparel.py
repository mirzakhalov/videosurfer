from clarifai.rest import ClarifaiApp
from clarifai.rest import Image, Model

class Apparel:

    def __init__(self):
        self.app = ClarifaiApp(api_key='b70faf3a718f4f2dad9811835a24cf63')
        self.model = Model(self.app.api, model_id='72c523807f93e18b431676fb9a58e6ad')
        self.fmodel = Model(self.app.api, model_id='e466caa0619f444ab97497640cefc4dc')



    def detect(self, frame, height, width):
        response = self.model.predict_by_filename(frame)
        items = []
        boxes = []
       
       
        if 'regions' in response['outputs'][0]['data']:
            for region in response['outputs'][0]['data']['regions']:
                bb = region['region_info']['bounding_box']
                boxes.append([
                    int(height * bb['top_row']), 
                    int(height * bb['bottom_row']), 
                    int(width * bb['left_col']), 
                    int(width * bb['right_col'])
                ])
                items.append(region['data']['concepts'][0]['name'])
        return items, boxes
    

    def detect_famous(self, frame, height, width):
        response = self.fmodel.predict_by_filename(frame)
        celebs = []
        boxes = []
        
        if 'regions' in response['outputs'][0]['data']:
            regions = response['outputs'][0]['data']['regions']
            for region in regions:
                celebs.append(region['data']['concepts'][0]['name'])
                bb = region['region_info']['bounding_box']
                boxes.append([
                    int(height * bb['top_row']), 
                    int(height * bb['bottom_row']), 
                    int(width * bb['left_col']), 
                    int(width * bb['right_col']) 
                ])
                
            
        return celebs, boxes
