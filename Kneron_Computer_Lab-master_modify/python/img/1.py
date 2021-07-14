import requests
import cv2
import os

url = 'http://192.168.100.110/mjpgstreamreq/1/image.jpg'

myobj = {'somekey': 'somevalue'}

#use the 'auth' parameter to send requests with HTTP Basic Auth:
x = requests.post(url, data = myobj, auth = ('admin', 'admin'))

with open('./img/aa.jpeg','wb') as f:

	f.write(x.content)



