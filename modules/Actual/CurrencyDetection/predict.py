import sys , json

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
import os
credential_path = "./demomaps-219313-cda72f9c4ea2.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
def get_prediction(content, project_id, model_id):
    prediction_client = automl_v1beta1.PredictionServiceClient()

    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned

def predictCurrency():
    file_path = "./sample.jpg"
    project_id = "demomaps-219313"
    model_id = "ICN3111800132441203883"
    print("comes here atleast !")
    with open(file_path, 'rb') as ff:
        content = ff.read()
    
    response = get_prediction(content, project_id,  model_id)\

    max_score = 0
    currency_name = ""
    for result in response.payload:
        if result.classification.score > max_score:
            currency_name = str(result.display_name)
            max_score = int(result.classification.score)
    print(currency_name)
    return currency_name

if __name__ == "__main__":
    print(predictCurrency())