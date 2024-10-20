from google_images_search import GoogleImagesSearch
from io import BytesIO
from PIL import Image 

class GoogleImage:

    def __init__(self, prompt):
        self.prompt = prompt
    
    def searchImage(prompt):
        gis = GoogleImagesSearch("AAAIzaSyBMJkra3UfmE2Ufm-rP0tAs4NZ7euOp52III","Quicservice") #AA.II
    
        _search_params = {
            'q': prompt.prompt,
            'num': 10,
            'fileType': 'jpg',
            'rights': 'cc_noncommercial',
            'safe': 'high', ##
            ##'imgType': 'clipart|lineart', ##
            'imgSize': 'medium', ##
            ##'imgDominantColor': 'black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow|imgDominantColorUndefined', ##
            ##'imgColorType': 'color|gray|mono|trans|imgColorTypeUndefined' ##
        }
        my_bytes_io = BytesIO()
        gis.search(search_params=_search_params)
        for image in gis.results():
            my_bytes_io.seek(0)
            # take raw image data
            raw_image_data = image.get_raw_data()
            image.copy_to(my_bytes_io, raw_image_data)
            return raw_image_data