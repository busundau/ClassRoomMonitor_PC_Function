import cv2
def Setcamera(cap):
    cap.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
    cap.set(3,480)
    cap.set(4,640)
#print("Before URL")
cap = cv2.VideoCapture('rtsp://192.168.100.253/1/h264major')

Setcamera(cap)



#print("After URL")

while True:

    #print('About to start the Read command')
    ret, frame = cap.read()
    #print('About to show frame of Video.')
    cv2.imshow("Capturing",frame)
    #print('Running..')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()