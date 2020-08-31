import json
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# # Passing API KEY and URL to the Visual Recognition
authenticator = IAMAuthenticator('IBM_API_KEY')

visual_recognition = VisualRecognitionV3(
    version='2018-03-19',
    authenticator=authenticator)

visual_recognition.set_service_url('IBM_URL') 

# Running the Visual Recognition on test.img file
with open('./test.jpg', 'rb') as image: 
    classes = visual_recognition.classify(images_file=image,threshold='0.6',classifier_ids='food').get_result()

#print(json.dumps(classes, indent=2))	
output_query = classes['images'][0]['classifiers'][0]['classes'][1]['class']
print(output_query)

# Passing 'pizza' to the HERE APIs using Python Flask
from flask import Flask,render_template

latitude = 12.959111
longitude = 77.732022

app = Flask(__name__)
@app.route('/')

def map_func():
	return render_template('map.html',
                            latitude = latitude,
                            longitude = longitude,
                            output_query=output_query
                            )

if __name__ == '__main__':
	app.run(debug = True)