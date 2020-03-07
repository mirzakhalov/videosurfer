from clarifai.rest import ClarifaiApp
from clarifai.rest import Image, Model

class Apparel:

    def __init__(self):
        self.app = ClarifaiApp(api_key='b70faf3a718f4f2dad9811835a24cf63')
        self.model = self.app.models.get('apparel')
        self.fmodel = Model(self.app.api, model_id='e466caa0619f444ab97497640cefc4dc')



    def detect(self, frame):
        response = self.fmodel.predict_by_filename(frame)
        items = []
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['value'] > 0.4:
                items.append(concept['name'])
                
        return items
    

    def detect_famous(self, frame):
        response = self.fmodel.predict_by_filename(frame)
        celebs = []
        if 'regions' in response['outputs'][0]['data']:
            regions = response['outputs'][0]['data']['regions']
            for region in regions:
                celebs.append(region['data']['concepts'][0]['name'])
            
        return celebs
