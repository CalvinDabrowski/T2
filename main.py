from pydoc import doc
from pyexpat import model
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI, Request
import requests,json;
import sqlite3;
import re;

## imports
url : str #used for json

templates   = Jinja2Templates(directory='templates')
connection  = sqlite3.connect('db.sqlite')
cursor      = connection.cursor()

async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request}) 
# homepage handler - applies index.html template to main page

async def item(request):
    return templates.TemplateResponse('item.html', {'request': request, 'id' :id})
# item handler - applies item.html template to various items. 
async def apiTest(request):
    return templates.TemplateResponse('apiTesting.html', {'request': request})

routes      = [
    Route('/', endpoint=homepage),
    Route('/item/{id}', endpoint=item),
    Mount('/static', StaticFiles(directory='static'), name='static')
] # Routing configuration. Allows user to go to various paths.

app = FastAPI(debug=True, routes=routes)
app.route("/apiTesting/{vin}", apiTest)

def checkExist(vinNumber):
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+vinNumber+"';").fetchall()
    if tables == []:
        print(vinNumber +" not found...")
        return False
    else:
        print("Table found")
        return True
# Check if table exists return true/false

def createDB(jsonData, vinNumber):
    for key, value in jsonData.items():
        if value:
            cursor.execute('INSERT INTO '+vinNumber+' VALUES (?,?)', (key, value))
            print(key + " : " +value + " inserted")
    connection.commit()
# Create table w/ vin number (all vins start with A to ensure it's a string)

def getSqlData(vinNumber):
    with connection:
        cursor.execute("SELECT * FROM " +vinNumber)
        print(cursor.fetchall())
# Print off all data stored in table of vin number

@app.get("/apiTesting/{vin}")
async def getVIN(request : Request, vin : str):
    url = requests.get("https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/" + vin[0:17] + "?format=json")
    importVIN = json.loads(json.dumps(url.json()['Results'][0]))
    tempDict = ""
    vinName = "A"+re.sub('[^A-Za-z0-9]+', '', vin[0:17]) # cleans the string prevents injections
    print(vinName)
    if not checkExist(vinName):
        cursor.execute('create table if not exists '+vinName+' (id varchar(2), data json)')
        createDB(importVIN,vinName)
        # Checks if a vinnumber is already in the database - prevents multiple entries into database
    for key, value in importVIN.items():
        if value:
            tempDict = tempDict + "<b>" + key + "</b> : " + value + "<br>" 
        # Format information as a string with the HTML already included. Would look like:  <b> Model </b> : BMW <br> - sends to website
    model = importVIN['Model']
    manuf = importVIN['Manufacturer']
    
    getSqlData(vinName)
    return templates.TemplateResponse('apiTesting.html', {'request': request, "vin" : vin[0:17], "mail" : tempDict, "model" : model, "manuf" : manuf})
# gets a vin number from "vin", passes it thru .get, loads, dumps, and converts it into an array prior to being passed to the html
0
print("It's recommended you go to the following link:\nhttp://127.0.0.1:8000/")
