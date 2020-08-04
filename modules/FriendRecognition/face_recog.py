import face_recognition
import numpy as np
import cv2
import time
import os

class FaceRecog:
    def __init__(self):
        self.image_dir = "./modules/FriendRecognition/pics/"

        self.people = [x.split(".")[0] for x in os.listdir(self.image_dir)]

        self.cap = cv2.VideoCapture(0)
        self.encodings = []

        for image in os.listdir(self.image_dir):
            img = face_recognition.load_image_file(os.path.join(self.image_dir, image))
            self.encodings.append(face_recognition.face_encodings(img))
    
    def manual_reboot(self):
        self.image_dir = "./modules/FriendRecognition/pics/"

        self.people = [x.split(".")[0] for x in os.listdir(self.image_dir)]

        self.cap = cv2.VideoCapture(0)
        self.encodings = []

        for image in os.listdir(self.image_dir):
            img = face_recognition.load_image_file(os.path.join(self.image_dir, image))
            self.encodings.append(face_recognition.face_encodings(img))

    def add_new_face(self, name, face):
        self.encodings.append(face_recognition.face_encodings(face))
        self.people.append(name)
        cv2.imwrite(os.path.join(self.image_dir, name + ".jpeg"), face)
        print("Done! Added new face")

    def start_video(self, detect_faces=False):
        while True:
            ret, frame = self.cap.read()
            cv2.imshow("Video", frame)

            frame = frame[:, :, ::-1]
            #frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            if detect_faces: print(self.render_frame(frame))
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord("a"):
                self.add_new_face("Ankitnath", frame)

            elif key == ord("q"):
                cv2.destroyAllWindows()
                break
        

    def render_frame(self, frame):
        i = 0
        face_encodings = (face_recognition.face_encodings(frame))
        face_locations = face_recognition.face_locations(frame)
        op = ""
        
        if len(face_encodings) == 0:
            op = "No faces"
        else:
            result = []

            stime = time.time()
            for face_enc in face_encodings:
                for enc in self.encodings:
                    res = face_recognition.compare_faces(enc, face_enc)
                    try:
                        if res[0] == True:
                            break
                        else:
                            i+=1
                    except:
                        pass
                if i >= len(self.encodings):
                    #result.append("Unknown")
                    pass
                else:
                    result.append(self.people[i])

            for _, x in sorted(zip([i[3] for i in face_locations], result)):
                op += x+","
            op = op[:-1] + " {:.3f}s".format(time.time() - stime)
            #print(op)
        
        return op

    def __del__(self):
        self.cap.release()