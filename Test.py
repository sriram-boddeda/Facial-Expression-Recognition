from tensorflow.keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import math as mt

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier = load_model('Trained_Model.h5')

class_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


def classify(frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    c=1
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        rof_gray = gray[y:y+h,x:x+w]
        rof_gray = cv2.resize(rof_gray,(48,48),interpolation=cv2.INTER_AREA)

        #ROF= Region of Face

        if np.sum([rof_gray])!=0:
            rof = rof_gray.astype('float')/255.0
            rof = img_to_array(rof)
            rof = np.expand_dims(rof,axis=0)

        # make a prediction on the ROF, then lookup the class

            preds = classifier.predict(rof)[0] #predictions 0=highest one
            label=class_labels[preds.argmax()]  #which expression has the highest probability values (0 to 6)
            label_position = (x,y+h+8)
            facex="face "+str(c)
            cv2.putText(frame,facex,(x,y),cv2.FONT_HERSHEY_SIMPLEX,w*(2/227),(0,255,0),mt.ceil(h*(2/180)))
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,w*(2/227),(0,255,0),mt.ceil(h*(2/180)))
            c+=1
        else:
            cv2.putText(frame,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    return frame


def video_classify():
    cap = cv2.VideoCapture(0)
    while True:
        # Grab a single frame of video
        ret, frame = cap.read()
        frame = classify(frame)
        cv2.imshow('Emotion Detector',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def image_classify(frame):
    frame = cv2.imread(frame)
    frame1 = classify(frame)
    cv2.imwrite(r'D:\Project FER\FER\img\out.jpg', frame1)