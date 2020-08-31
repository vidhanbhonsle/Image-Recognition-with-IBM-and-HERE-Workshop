# Image Recognition with IBM and HERE Workshop

Ever wondered on how we can add AI when it comes to location based services? In this code we upload pass an image to a Python Flask Application and get recommendation based on the food picture you have passed.

#### Sign up for IBM Cloud at https://ibm.biz/HERETechnologies
#### Get your Here Maps API Key at https://developer.here.com

## Architecture

![Arch](/images/AI_Location_Sol_Arch.png)

1. User passes an image in the python code
1. As we are using the visual recognition service there is a out of the box food model which we are going to use and it detects the name of the food which we have passed
1. The name of the food is then passed to the Here Maps Discover API which then suggests places around a particular location which we have configured within the python application.

## Prerequisites

- Code IDE
- Python 3.X (https://www.python.org/downloads/)
- HERE Developer Account (https://developer.here.com/sign-up?create=Freemium-Basic&keepState=true&step=account)
- IBM Cloud account (https://cloud.ibm.com/login)
- Bring your Coffee/Tea and enjoy the journey 

## Steps

### Step 1: Python code for Visual Recognition

install Watson Developer Cloud library -
- pip install --upgrade "ibm-watson>=4.0.1"

```python
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
```
The above code will print "Pizza"

### Step 2: Integrating Flask in Python code

install Flask library -
- pip install flask

```python
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
	app.run(debug = False)
```

### Step 3: Show your location on a map

Create a folder 'templates' and create a file 'map.html' inside it.

```html
<html>   
<head>   
<meta name="viewport" charset="UTF-8" content="initial-scale=1.0, width=device-width" />
<script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-core.js"></script> 
<script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-service.js"></script> 
<script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-ui.js"></script> 
<script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-mapevents.js"></script> 
<link rel="stylesheet" type="text/css" href="https://js.api.here.com/v3/3.1/mapsjs-ui.css"/> 
</head> 

<body style='margin: 0'> 
<div id="mapContainer" style="width: 90vw; height: 80vh; display: block; margin: 0 auto; border: solid 2px black; margin-top: 10px;" >
</div> 
 <div style="width: 100vw; height: 40px; margin-top: 30px;"> 
 <input type="button" onclick="showRestaurants()" value = "Show Restaurants" style="width: 200px; height: 30px; border: 2px solid black; display: block; margin: 0 auto; margin-top: 20px;"> 
 </div>
</body> 

<script>    
    const lat = {{latitude}}; 
    const lng = {{longitude}}; 
    var query = "{{output_query}}"; 

    //Initialise communication with backend services 
     var platform = new H.service.Platform({ 
            apikey: "JS_API_KEY"    
        }); 

    // Obtain the default map types from the platform object: 
    var defaultLayers = platform.createDefaultLayers(); 

    // Get your current position from wego.here.com 
    var myPosition = {lat: lat, lng: lng}; 

    // Instantiate (and display) a map object: 
    var map = new H.Map( 
        document.getElementById('mapContainer'), 
        defaultLayers.vector.normal.map, 
        { 
            zoom: 15, 
            center: myPosition 
        }); 

    //zoom and view controls 
    var ui = H.ui.UI.createDefault(map, defaultLayers, 'en-US'); 

    //Move around the map 
    var mapEvents = new H.mapevents.MapEvents(map); 
    var behavior = new H.mapevents.Behavior(mapEvents); 

    // create an icon for the marker. Choose any image you want. 
    var homeIcon = new H.map.Icon('/static/YOUR_IMAGE');  

    // Create a marker using the previously instantiated icon: 
    var posMarker = new H.map.Marker(myPosition,{icon:homeIcon}); 

    // Add the marker to the map  
    map.addObject(posMarker);    
</script>
</html>
```
Substitute the 'YOUR_IMAGE' with the image you want to use.

### Step 4: Show pizza serving places on Map

Show pizza places around you on a map with a click of a button

An instance of Geocoding and Search Service

```javascript
var service = platform.getSearchService();
```

Button click logic

```javascript
    function showRestaurants(){ 
            let param = { 
                at : myPosition.lat+','+myPosition.lng, 
                q: query, 
                limit:10 
            };  
            service.browse(param,displayRestaurants,alert); 
        } 
```

Pizza places as a clickable icon on the map

```javascript
function displayRestaurants(response){ 
            var restaurantIcon = new H.map.Icon('/static/PIZZA_IMAGE'); 

            // A group that can hold map objects: 
            var restGroup = new H.map.Group(); 

            for(let i = 0; i<response.items.length; i++){ 
                let restPosition = response.items[i].position; 
                let address = response.items[i].address.label; 
                 
                let restMarker = new H.map.Marker(restPosition,{icon: restaurantIcon} ); 
                 
                restMarker.setData("<p>" + address + "</p>"); 
                 
                restMarker.addEventListener('tap', function(evt){ 
                    var bubble =  new H.ui.InfoBubble(evt.target.getGeometry(), { 

                    // read custom data 
                    content: evt.target.getData() 
                }); 

                ui.addBubble(bubble); 
                }, false); 

                // Add the marker to the group (which causes it to be displayed on the map) 
                restGroup.addObject(restMarker); 
                } 

            // Add the group to the map object 
            map.addObject(restGroup); 
    }
```