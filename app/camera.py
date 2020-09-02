import cv2
import os
from app import Attendance
from app.Attendance import *
import face_recognition
import numpy as np


path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.encodeListKnown = Attendance.findEncodings(images)

    def __del__(self):
        self.cap.release()


    
    def get_frame(self):

        success, img = self.cap.read()
        cv2.imshow('Webcam', img)
        cv2.waitKey(1)
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        print(encodesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
            name = "Unknown"
            faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                # print(name)
            for (y1, x2, y2, x1), facename in zip(facesCurFrame, name):
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)
        ret,jpeg = cv2.imencode('.jpg',img)
        data=[]
        # dt = np.array(encodesCurFrame).tobytes()
        data.append(jpeg.tobytes())
        return data

