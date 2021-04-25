import cv2
import threading
import time
import atexit
import helper_functions as help

# important fields
face_classifier = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
eye_classifier = cv2.CascadeClassifier('resources/haarcascade_eye.xml')
capture = cv2.VideoCapture(1)

# global face or eye array
faces = []

# seperate thread for constantly checking for faces
def captureUserTarget():
    global faces
    global capture_thread
    while True:
        _, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # checks for face and then eyes if unavailable
        faces = face_classifier.detectMultiScale(gray, 1.1, 4)
        if(len(faces) == 0):
            faces = eye_classifier.detectMultiScale(gray, 1.1, 4)

        # draws around users face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)

        # shows img and waits and changes servo positioning
        cv2.imshow('Video', frame)
        trackUser()
        cv2.waitKey(20)



def trackUser():
    if(capture.isOpened() and len(faces) > 0):
        print("")
        capture_height = capture.get(4)
        capture_width = capture.get(3)

        f = faces[0]
        x = (f[0]+f[2])/capture_width
        y = (f[1]+f[3])/capture_height
        help.printf("X: %0.2f Y:%0.2f",x, y)

#Detection Thred
capture_thread = threading.Thread(target=captureUserTarget, args=())

#on exit
def exit_handler():
    capture_thread.join()
    capture.release()
    cv2.destroyAllWindows()
#closes windows and threads prior to exiting
atexit.register(exit_handler)

# main thread
capture_thread.start() # starts face tracking in the background
# gets menu input

# starts fsm
while True:
    time.sleep(0.5)
    

    
    
    
