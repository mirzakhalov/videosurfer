from clarifai.rest import ClarifaiApp
from clarifai.rest import Image, Model

class Apparel:

    def __init__(self):
        self.app = ClarifaiApp(api_key='b70faf3a718f4f2dad9811835a24cf63')
        self.model = self.app.models.get('apparel')


    def detect(self, frame):
        return self.model.predict_by_filename(frame)
    

    def detect_famous(self, frame):
        return self.model.predict_by_filename(frame)
