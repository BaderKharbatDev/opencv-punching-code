import cv2
import threading
import time
import atexit

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

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)

        cv2.imshow('Video', frame)
        cv2.waitKey(20)
        # if cv2.waitKey(20) & 0xFF==ord('d'):
        #     break

#Detection Thred
capture_thread = threading.Thread(target=captureUserTarget, args=())
capture_thread.start()

#on exit
def exit_handler():
    capture_thread.join()
    capture.release()
    cv2.destroyAllWindows()
#closes windows and threads prior to exiting
atexit.register(exit_handler)

# main thread
while True:
    time.sleep(0.5)
    print(len(faces))

    
    
    
