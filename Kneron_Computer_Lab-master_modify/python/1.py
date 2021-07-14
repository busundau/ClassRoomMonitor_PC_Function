import requests
import cv2
import os
from PIL import Image

url = 'http://192.168.100.253/mjpgstreamreq/1/image.jpg'

myobj = {'somekey': 'somevalue'}

#use the 'auth' parameter to send requests with HTTP Basic Auth:
x = requests.post(url, data = myobj, auth = ('admin', 'admin'))

with open('./img/aa.jpg','wb') as f:

	f.write(x.content)

im = Image.open('./img/aa.jpg')

im.show()


#pip install Pillow


