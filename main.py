from pyexpat import model
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI, Request
import requests,json;

## imports
url : str #used for json

templates = Jinja2Templates(directory='templates')

async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request}) 
# homepage handler - applies index.html template to main page

async def item(request):
    return templates.TemplateResponse('item.html', {'request': request, 'id' :id})
# item handler - applies item.html template to various items. 
async def apiTest(request):
    return templates.TemplateResponse('apiTesting.html', {'request': request})
# id does not yet serve a purpose.


routes = [
    Route('/', endpoint=homepage),
    Route('/item/{id}', endpoint=item),
    Mount('/static', StaticFiles(directory='static'), name='static')
] # Routing configuration. Allows user to go to various paths.

app = FastAPI(debug=True, routes=routes)
app.route("/apiTesting/{vin}", apiTest)

@app.get("/apiTesting/{vin}")
async def getVIN(request : Request, vin : str):
    url = requests.get("https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/" + vin[0:17] + "?format=json")
    vinTree = json.loads(json.dumps(url.json()['Results'][0]))
    model = vinTree['Model']
    manuf = vinTree['Manufacturer']
    vinTree['Manufacturer'] =  vinTree['Manufacturer'].replace(",","")
    vinTree['OtherRestraintSystemInfo'] =  vinTree['OtherRestraintSystemInfo'].replace(",","")
    mail = vinTree
    return templates.TemplateResponse('apiTesting.html', {'request': request, "vin" : vin[0:17], "mail" : mail, "model" : model, "manuf" : manuf})
# gets a vin number from "vin", passes it thru .get, loads, dumps, and converts it into an array prior to being passed to the html

print("It's recommended you go to the following link:\nhttp://127.0.0.1:8000/")

