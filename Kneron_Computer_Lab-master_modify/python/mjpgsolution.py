import cv2
import requests
import numpy as np

def run_image( byte_s):
    r = requests.get('http://192.168.100.253/mjpgstreamreq/1/image.jpg', auth=('admin', 'admin'), stream=True)
    if(r.status_code == 200):
       
        for chunk in r.iter_content(chunk_size=1024):
            byte_s += chunk
            a = byte_s.find(b'\xff\xd8')
            b = byte_s.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = byte_s[a:b+2]
                byte_s = byte_s[b+2:]
                i = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imwrite("D:\jacob_liang\Desktop\Kneron_Computer_Lab-master_modify\python\images/1.jpg",i)
                cv2.imshow('i', i)
                if cv2.waitKey(1) == 27:
                    exit(0)
    else:
        print("Received unexpected status code {}".format(r.status_code))
        
byte_s = bytes()
run_image(byte_s)
