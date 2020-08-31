# Image Recognition with IBM and HERE Workshop

Ever wondered on how we can add AI when it comes to location based services? In this code we upload pass an image to a Python Flask Application and get recommendation based on the food picture you have passed.

#### Sign up for IBM Cloud at https://ibm.biz/HERETechnologies
#### Get your Here Maps API Key at https://developer.here.com

## Architecture

![Arch](/images/AI_Location_Sol_Arch.png)

1. User passes an image in the python code
1. As we are using the visual recognition service there is a out of the box food model which we are going to use and it detects the name of the food which we have passed
1. The name of the food is then passed to the Here Maps Discover API which then suggests places around a particular location which we have configured within the python application.

## Steps

### Step 1: Python code for Visual Recognition

install Watson Developer Cloud library -
- pip install --upgrade "ibm-watson>=4.0.1"

```python
import json 
from ibm_watson import VisualRecognitionV3 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator 

# Passing API KEY and URL to the Visual Recognition 
authenticator = IAMAuthenticator('IBM_API_KEY') 

visual_recognition = VisualRecognitionV3( 
    version='2018-03-19', 
    authenticator=authenticator) 

visual_recognition.set_service_url('IBM_URL')  

# Running the Visual Recognition on test.img file 
with open('./test.jpg', 'rb') as image:  
    classes = visual_recognition.classify(images_file=image,threshold='0.6',classifier_ids='food').get_result() 

output_query = classes['images'][0]['classifiers'][0]['classes'][1]['class'] 
print(output_query)  
```
The above code will print "Pizza"

### Step 2: Integrating Flask in Python code

```python

from flask import Flask,render_template  

#Somewhere in Bangalore, India 
latitude = 12.959111 
longitude = 77.732022 

app = Flask(__name__) 

@app.route('/') 

def map_func(): 
    return render_template('map.html', 
                            latitude = latitude, 
                            longitude = longitude, 
                            output_query=output_query 
                            ) 

if __name__ == '__main__': 
    app.run(debug = True)
```
