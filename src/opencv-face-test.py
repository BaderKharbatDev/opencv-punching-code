import cv2
import threading
import time
import atexit
import helper_functions as help
import serial

# important fields
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)

# global face or eye array
faces = []
last_x = 0.0
last_y = 0.0

# seperate thread for constantly checking for faces
def captureUserTarget():
    global faces
    global capture_thread
    while True:
        _, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # checks for face and then eyes if unavailable
        faces = face_classifier.detectMultiScale(gray, 1.1, 4)
        # if(len(faces) == 0):
        #     faces = eye_classifier.detectMultiScale(gray, 1.1, 4)

        # draws around users face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)

        # shows img and waits and changes servo positioning
        frame = trackUser(frame)
        cv2.imshow('Video', frame)
        cv2.waitKey(20)
        cv2.destroyAllWindows()

def trackUser(img):
    global last_x, last_y
    if(capture.isOpened() and len(faces) > 0):
        # print("")
        capture_height = capture.get(4)
        capture_width = capture.get(3)

        f = faces[0]
        largest_area = ((f[1]+f[3])/2 * (f[0]+f[2]/2))

        if len(faces > 1):
            for index_temp,face_temp in enumerate(faces):
                if(index_temp == 1):
                    continue
                else:
                    temp_area = ((face_temp[1]+face_temp[3])/2 * (face_temp[0]+face_temp[2]/2))
                    if(temp_area > largest_area):
                        largest_area = temp_area
                        f = face_temp



        x = (f[0]+f[2]/2)/capture_width
        # y = (f[1]+f[3]/2)/capture_height
        y = (f[1])/capture_height
        last_x = x
        last_y = y
        text = "X: {:0.0f}% Y: {:0.0f}%".format(x*100, y*100)
        cv2.putText(img, text, 
            (10,int(capture_height)-25), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1,
            (255,255,255),
            2)
        setServos(x,y)
    else:
        setServos(last_x, last_y)
    return img

def setServos(x,y):
    inner_circle_radius = 40+50
    inner_circle_radius_y = 40+50

    adjusted_x = (1-x)*180
    adjusted_y = (1-y)*180
    if(adjusted_x < 90-inner_circle_radius):
        adjusted_x = 90 - inner_circle_radius
    elif(adjusted_x > 90+inner_circle_radius):
        adjusted_x = 90 + inner_circle_radius

    if(adjusted_y < 90-inner_circle_radius_y):
        adjusted_y = 90 - inner_circle_radius_y
    elif(adjusted_y > 90+inner_circle_radius_y):
        adjusted_y = 90 + inner_circle_radius_y

    rs = "a|"+str(adjusted_x)+"/"+str(adjusted_y)+"\n"
    # print(str(adjusted_y)+"\n")
    try:
        arduino.write(str.encode(rs))
    except:
        print("An exception occurred") 

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
frequency = 5 #difficulty [1 - 10]
delay_time = frequency*-1+11
# starts fsm
while True:
    # lock = True
    rs = "b|a\n";
    try:
        arduino.write(str.encode(rs))
    except:
        print("An exception occurred") 
    time.sleep(0.5) #time for the cylender to remain extended
    rs = "b|b\n";
    try:
        arduino.write(str.encode(rs))
    except:


        print("An exception occurred")     # lock = False
    # time.sleep(delay_time/10)
    time.sleep(1) #time in between 'punches'
    

    
    
    
