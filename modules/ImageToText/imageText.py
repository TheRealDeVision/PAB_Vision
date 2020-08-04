import pytesseract
#=pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
from PIL import Image
import time
import cv2
import os
#from camcap import imagecapture
ini = time.time()
import cv2 as cv
#image = "D:/juhack/Save/"+ str(round((file_count/2))) + ".png"
image = ""   #path of the file !
def readText(frame):
  image = "./modules/ImageToText/pics/1.jpg"
  basewidth = 1300
  img = Image.open(image)
  wpercent = (basewidth/float(img.size[0]))
  hsize = int((float(img.size[1])*float(wpercent)))
  img = img.resize((basewidth,hsize), Image.ANTIALIAS)
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  #pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ankit\AppData\Local\Tesseract-OCR"
  x = pytesseract.image_to_string((image))
  print(x)
  if (x == ""):
    print("Image not read")
  else:
    sent = str(pytesseract.image_to_string((image)))
    import nltk
    words = set(nltk.corpus.words.words())
    op = []
    notwanted = [";","_","-","...","..","....","»",'"',"||","|","!","'"]
    for w in nltk.wordpunct_tokenize(sent):
        if w.lower() in words or not w.isalpha() and not w in notwanted:
            op.append(w)
    res = ' '.join(op)
    return res
#print(ini - time.time())