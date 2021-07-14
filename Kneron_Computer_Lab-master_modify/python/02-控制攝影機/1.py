import requests
import cv2

url = 'http://192.168.100.110/cgi/ptz_set?Channel=1&Group=PTZCtrlInfo&Direction=2&PanSpeed=2&TiltSpeed=3'

myobj = {'somekey': 'somevalue'}

#use the 'auth' parameter to send requests with HTTP Basic Auth:
x = requests.post(url, data = myobj, auth = ('admin', 'admin'))

print(x.status_code)

