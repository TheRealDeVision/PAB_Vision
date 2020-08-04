"""
import cv2
import numpy as np
import tensorflow as tf

def prepare(filepath):    
    IMG_SIZE = 150
    img_array = cv2.imread(filepath)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE,3) 
    
    
def curDetect(frame):    
    cv2.imwrite("./pics/1.png" , frame)    
    model = tf.keras.models.load_model("cur.model")
    CATEGORIES = ["two thousand","five hundred","fifty"]
    sentimg = cv2.imread("./pics/1.png")
    prediction = model.predict([prepare("./pics/1.png")])
    print(CATEGORIES[int(prediction[0][0])])

if __name__ == "__main__":
    frame = cv2.VideoCapture(0)
    curDetect(frame)
"""

import cv2
import numpy as np
import tensorflow as tf

cap = cv2.VideoCapture(0)
def prepare(filepath):    
    IMG_SIZE = 150
    img_array = cv2.imread(filepath)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE,3) 
    
    
def curDetect():    
    while(1):
        ret , frame = cap.read()
        cv2.imwrite("./pics/1.jpg" , frame)
            
        model = tf.keras.models.load_model("cur.model")
        CATEGORIES = ["two thousand","five hundred"]
        sentimg = cv2.imread("./pics/1.jpg")
        prediction = model.predict([prepare("./pics/1.jpg")])
        print(CATEGORIES[int(prediction[0][0])])
        break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    curDetect()