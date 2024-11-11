import requests


class ORCService():
    @classmethod
    def ORCApi(self):
        # K86279254688957 - pedrohes
        # K81134679488957 - canal100
        api_key = 'K81134679488957'
        image_png = r'C:\Users\pedro.santos\Downloads\ProjectCr\temp\image.png'

        with open(image_png, 'rb') as file:
            response = requests.post(
                'https://api.ocr.space/parse/image',
                files={image_png: file},
                data={'apikey': api_key, 'language': 'eng', 'OCREngine': 2}
            )
        return response.json()
