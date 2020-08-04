def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io,os
    credential_path = "./DemoMaps-c874ca905d39.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    summary = ""
    for text in texts:
        summary = summary + '\n' + text.description
        #vertices = (['({},{})'.format(vertex.x, vertex.y)
        #            for vertex in text.bounding_poly.vertices])
        #print('bounds: {}'.format(','.join(vertices))) 
        break
    print(summary)
detect_text("./sample.jpg")