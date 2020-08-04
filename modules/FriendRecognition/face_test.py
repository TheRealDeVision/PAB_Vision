from face_recog import FaceRecog
#from PAB_Vision.Machine_Learning.bot.botAPI import *
import cv2
import face_recognition
#botResponseReciever("Friend Shyam")
face_recog = FaceRecog()
#frame = face_recognition.load_image_file("G:\\shyam\\Pictures\\Camera Roll\\test\\shyam\\pic.jpg")
#frame = cv2.imread("G:\\shyam\\Pictures\\Camera Roll\\test\\shyam\\pic.jpg")
#frame = frame[:, :, ::-1]
#frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#print(face_recog.render_frame(frame))
face_recog.start_video(detect_faces=True)
#face_recog.add_new_face("Shyam", frame)