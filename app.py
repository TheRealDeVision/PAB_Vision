from flask import Flask, render_template ,jsonify , request

from modules.ImageToText.imageText import readText
import threading , time , cv2 , requests , os , json, io

#   External Modules ...
from modules.DialogFlowConnect import botResponseReciever
from modules.FriendRecognition.face_recog import FaceRecog
#from modules.Actual.CurrencyDetection.predict import predictCurrency

face = FaceRecog()

app = Flask(__name__)

# Variables declaration...

buffer = "Face"
data_buffer = ""
special_buffer = ""
wait_flag = ""
stop_threads = False
webcam_thread = None

import sys , json

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
import os
from google.cloud import vision
import io,os

def get_prediction(content, project_id, model_id):
    prediction_client = automl_v1beta1.PredictionServiceClient()

    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned

def predictCurrency():
    file_path = "./modules/Actual/CurrencyDetection/sample.jpg"
    project_id = "demomaps-219313"
    model_id = "ICN3111800132441203883"
    #with open(file_path, 'rb') as ff:
    #    content = ff.read()
    currency_name = "Hello"
    '''response = get_prediction(content, project_id,  model_id)\

    max_score = 0
    currency_name = ""
    for result in response.payload:
        if result.classification.score > max_score:
            currency_name = str(result.display_name)
            max_score = int(result.classification.score)
    print(currency_name)'''
    return currency_name

def webcamCap(stop):
    global buffer
    global data_buffer
    global special_buffer
    global wait_flag
    
    cap = cv2.VideoCapture("http://192.168.43.216:4747/mjpegfeed")
    #cap = cv2.VideoCapture("http://192.168.43.199:4747/mjpegfeed")
    counter = 0
    while(True):
        ret , frame = cap.read()
        #   RGB -> Grey Conversion (Optional)
        try:
            frame = frame[50: , 50:]
        except:
            pass
        #   Face Condition...
        if buffer == "Face" and counter > 20:
            counter = 0
            name = face.render_frame(frame)
            if(name != "No faces"):
                name = name.split(" ")[0]
                data_buffer = name
                if name == "":
                    buffer = "Face"
                else:
                    buffer = "Nothing"
        #   Currency Check...
        elif buffer == "currency":
            #cv2.imwrite("./modules/Actual/CurrencyDetection/sample.jpg" , frame)
            credential_path = "./modules/Actual/CurrencyDetection/demomaps-219313-cda72f9c4ea2.json"
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
            print("predict")
            #file_path = "./modules/Actual/CurrencyDetection/sample.jpg"
            project_id = "demomaps-219313"
            model_id = "ICN3111800132441203883"
            
            #with open(file_path, 'rb') as ff:
            #   content = ff.read()
            #currency_name = "Hello"
            image = frame
            success, encoded_image = cv2.imencode('.jpg', image)
            content  = encoded_image.tobytes()
            response = get_prediction(content, project_id,  model_id)

            max_score = 0
            currency_name = ""
            for result in response.payload:
                if result.classification.score > max_score:
                    currency_name = str(result.display_name)
                    max_score = int(result.classification.score)
            print(currency_name)
            data_buffer = currency_name  
            wait_flag = False
            buffer = "Nothing"
        #   Remembering person...
        elif buffer == "remember":
            face.add_new_face(str(data_buffer) , frame)
            face.manual_reboot()
            buffer = "Nothing"
        elif buffer == "read":
            credential_path = "./modules/Actual/ImageToText/DemoMaps-c874ca905d39.json"
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
            client = vision.ImageAnnotatorClient()

            image = frame
            success, encoded_image = cv2.imencode('.jpg', image)
            content  = encoded_image.tobytes()
            
            image = vision.types.Image(content=content)
            response = client.text_detection(image=image)
            texts = response.text_annotations
            data_buffer = ""
            #for text in texts:
            #    data_buffer = data_buffer + " <br> " + texts[0].description
            data_buffer = texts[0].description
            #print(data_buffer)
            wait_flag = False
            buffer = "Nothing"

        elif buffer == "scene":
            credential_path = "./modules/Actual/ImageToText/DemoMaps-c874ca905d39.json"
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
            client = vision.ImageAnnotatorClient()

            image = frame
            success, encoded_image = cv2.imencode('.jpg', image)
            content  = encoded_image.tobytes()

            image = vision.types.Image(content=content)

            response = client.web_detection(image=image)
            annotations = response.web_detection

            if annotations.best_guess_labels:
                for label in annotations.best_guess_labels:
                    #print('\nBest guess label: {}'.format(label.label))
                    b_guess = label.label

            if annotations.pages_with_matching_images:
                print('\n{} Pages with matching images found:'.format(
                    len(annotations.pages_with_matching_images)))

                for page in annotations.pages_with_matching_images:
                    print('\n\tPage url   : {}'.format(page.url))

                    if page.full_matching_images:
                        print('\t{} Full Matches found: '.format(
                            len(page.full_matching_images)))

                        for image in page.full_matching_images:
                            print('\t\tImage url  : {}'.format(image.url))

                    if page.partial_matching_images:
                        print('\t{} Partial Matches found: '.format(
                            len(page.partial_matching_images)))

                        for image in page.partial_matching_images:
                            print('\t\tImage url  : {}'.format(image.url))

            if annotations.web_entities:
                # print('\n{} Web entities found: '.format(
                #     len(annotations.web_entities)))

                for entity in annotations.web_entities:
                    #print('\n\tScore      : {}'.format(entity.score))
                    data_buffer = "I think this is either a " + entity.description + " or " + b_guess
                    break

            print(data_buffer)
            wait_flag = False
            buffer = "Nothing"

        counter = counter + 1
        
        cv2.imshow('Live Camera Feed' , frame)
        
        if stop():
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def bot_event_handler(bot_response , intent_class):
    global data_buffer
    if intent_class == "launch":
        return requests.post('http://192.168.43.218:5000/start')
    elif intent_class == "remember person":
        data_buffer = bot_response.replace("Ok, ill remember " , "")
        return requests.post('http://192.168.43.218:5000/remember')
    elif intent_class == "Sleep":
        return requests.post('http://192.168.43.218:5000/stop')
    elif intent_class == "currency":
        return requests.post('http://192.168.43.218:5000/currency')
    elif intent_class == "read":
        return requests.post('http://192.168.43.218:5000/read')
    elif intent_class == "scene":
        return requests.post('http://192.168.43.218:5000/scene')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/botResponse' , methods = ['POST' , 'GET'])
def botResponse():
    global special_buffer
    global wait_flag
    global data_buffer

    botMessage = botResponseReciever(request.form["utext"])
    handler_data = bot_event_handler(botMessage[0] , botMessage[1])
    try:
        if special_buffer == True:
            while(wait_flag == True and special_buffer == True):
                continue
            print("Comes this way too !" + data_buffer)
            #   print("buffer : " + special_buffer)
            special_buffer = False
            return jsonify({'response': data_buffer , 'class' : botMessage[1]})
        handler_data = handler_data.json()
        if not handler_data['flag']:
            print("comes handler")
            return jsonify({'response': handler_data['message'] , 'class' : botMessage[1]})
    except:
        pass
    return  jsonify({'response': botMessage[0] , 'class' : botMessage[1]})

@app.route('/start' , methods = ['POST' , 'GET'])
def startRender():
    global stop_threads
    global buffer
    global data_buffer
    global webcam_thread
    if not stop_threads:
        webcam_thread = threading.Thread(target = webcamCap, args =(lambda : stop_threads, )) 
        webcam_thread.start()
        while(buffer == "Face"):
            continue
        print("comes out of face !{}".format(data_buffer))
        return jsonify({ 'flag' : False, 'message': "Your friend "+data_buffer +" is nearby"})
    print('[STATUS] Thread running...')
    return jsonify({'flag': True})

@app.route('/stop' , methods = ['POST' , 'GET'])
def stopRender():
    global stop_threads
    global buffer
    stop_threads = True
    time.sleep(0.3)
    buffer = "Face"
    stop_threads = False
    print('[STATUS] Thread stops...')
    return jsonify({'flag' : True})

@app.route('/remember' , methods = ['POST' , 'GET'])
def remember():
    global buffer
    global data_buffer
    #print("comes here 2")
    buffer = "remember"
    return jsonify({'flag' : True})

@app.route('/currency' , methods = ['POST' , 'GET'])
def predictCurrency():
    global buffer
    global wait_flag
    global special_buffer
    special_buffer = True
    wait_flag = True
    buffer = "currency"
    return "done"

@app.route('/read' , methods = ['POST' , 'GET'])
def imageToText():
    global buffer
    global wait_flag
    global special_buffer
    special_buffer = True
    wait_flag = True
    buffer = "read"
    return "done"

@app.route('/scene' , methods = ['POST' , 'GET'])
def sceneDetection():
    global buffer
    global wait_flag
    global special_buffer
    special_buffer = True
    wait_flag = True
    buffer = "scene"
    return "done"

if __name__ == "__main__":
    app.run(debug = True , host= "0.0.0.0" , port= 5000)