import requests
import json
from PIL import Image
from io import BytesIO
from backend import byte2image

url1 = 'http://localhost:5000/api/api/posts'
base_url2 = 'http://localhost:5000/api/api/files/'

response = requests.get(url1).content
response = json.loads(response)
filename0 = response['image_filenames']['0']

 # -------------------------------------------------

url2 = base_url2 + filename0

response = requests.get(url2).content

print(byte2image(response) == Image.open('image/20200617193134_freedom.jpg'))
