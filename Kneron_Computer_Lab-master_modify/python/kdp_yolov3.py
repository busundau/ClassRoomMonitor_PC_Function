import argparse
import os
import cv2
import ctypes
import requests
import numpy as np
import time

from common import constants
from python_wrapper import kdp_wrapper
from python_wrapper import kdp_examples
from python_wrapper import update_app
from python_wrapper import dme_keras
from kdp_host_api import (kdp_add_dev, kdp_init_log, kdp_lib_de_init, kdp_lib_init, kdp_lib_start)

# Define KL520 parameters
KDP_USB_DEV     = 1
IMG_SRC_WIDTH	= 640
IMG_SRC_HEIGHT	= 480
ISI_YOLO_ID     = constants.APP_TINY_YOLO3
image_size      = IMG_SRC_WIDTH * IMG_SRC_HEIGHT * 2
user_id         = 0

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
                #cv2.imshow('i', i)
                #if cv2.waitKey(1) == 27:
                 #   exit(0)
           
    else:
        print("Received unexpected status code {}".format(r.status_code))
    time.sleep(2)
    #time.sleep(.001) 

def detect_image(dev_idx, user_id):

    # Initialize image capture parameters
    frames      = []
    img_id_tx   = 0

    # Setup image path
    data_path = os.path.join(os.getcwd(), 'images')
    print(data_path)
    # Read input image
    #image_name = input('Input image file: ')
    image_name = '1.jpg'
    print(image_name)
    image_path = os.path.join(data_path, image_name)
    print(image_path)
    image_flag = os.path.isfile(image_path)
    
    # Start ISI mode
    if (kdp_wrapper.start_isi(dev_idx, ISI_YOLO_ID, IMG_SRC_WIDTH, IMG_SRC_HEIGHT)):
        return -1

    # Perform image inference
    while image_flag:
        byte_s = bytes()
        run_image(byte_s)

        image = cv2.imread(image_path)
        kdp_examples.image_inference(dev_idx, ISI_YOLO_ID, image_size, image, img_id_tx, frames)
        img_id_tx += 1
        #image_name = input('Input image file: ')
        image_path = os.path.join(data_path, image_name)
        image_flag = os.path.isfile(image_path)

    cv2.destroyAllWindows()

def detect_camera(dev_idx, user_id):

    # Initialize camera capture parameters
    frames      = []
    img_id_tx   = 0

    # Setup webcam capture
    #capture     = kdp_wrapper.setup_capture(0, IMG_SRC_WIDTH, IMG_SRC_HEIGHT)
    capture     = kdp_wrapper.setup_capture('rtsp://192.168.100.253/1/h264minor', IMG_SRC_WIDTH, IMG_SRC_HEIGHT)

    if capture is None:
        print("Can't open webcam")
        return -1

    # Start ISI mode
    if (kdp_wrapper.start_isi(dev_idx, ISI_YOLO_ID, IMG_SRC_WIDTH, IMG_SRC_HEIGHT)):
        return -1

    # Perform video inference
    while True:
        kdp_examples.camera_inference(dev_idx, ISI_YOLO_ID, image_size, capture, img_id_tx, frames)
        img_id_tx += 1

    capture.release()
    cv2.destroyAllWindows()

# Read input arguments
parser = argparse.ArgumentParser(description="Kneron Neural Processing Unit")
parser.add_argument('-t', '--task_name', help=("image, camera, update_app, dme_keras"), default="camera")
args = parser.parse_args()

# Initialize Kneron USB device
kdp_init_log("/tmp/", "mzt.log")

print("Initialize kdp host lib  ....\n")
if (kdp_lib_init() < 0):
    print("Initialize kdp host lib failure\n")

print("Add kdp device ....")
dev_idx = kdp_add_dev(KDP_USB_DEV, "")
if (dev_idx < 0):
    print("Add kdp device failure\n")

print("Start kdp host lib ....\n")
if (kdp_lib_start() < 0):
    print("Start kdp host lib failure")

print("Start kdp task: ", args.task_name)

if (args.task_name == "image"):
    detect_image(dev_idx, user_id)
elif (args.task_name == "camera"):
    detect_image(dev_idx, user_id)
    #detect_camera(dev_idx, user_id)
elif (args.task_name == "update_app"):
    update_app.user_test_update_app(dev_idx, user_id)
elif (args.task_name == "dme_keras"):
    dme_keras.user_test_dme_keras(dev_idx, user_id)

# Exit Kneron USB device
print("Exit kdp host lib ....\n")
kdp_lib_de_init()
