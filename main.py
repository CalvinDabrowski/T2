from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

## imports

templates = Jinja2Templates(directory='templates')

async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request}) 
# homepage handler - applies index.html template to main page

async def item(request):
    return templates.TemplateResponse('item.html', {'request': request, 'id' :id})
# item handler - applies item.html template to various items. 
# id does not yet serve a purpose.


routes = [
    Route('/', endpoint=homepage),
    Route('/item/{id}', endpoint=item),
    Mount('/static', StaticFiles(directory='static'), name='static')
] # Routing configuration. Allows user to go to various paths.

app = Starlette(debug=True, routes=routes)

print("It's recommended you go to the following link:\nhttp://127.0.0.1:8000/")