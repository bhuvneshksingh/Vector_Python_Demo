from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import JSONResponse,Response
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.datastructures import Headers
from starlette.routing import Route
import uvicorn
from db import connect_db,close_db,myDB,account
from db.account import Account
from playhouse.migrate import SqliteMigrator
import peewee
import logging
import asyncio


templates = Jinja2Templates(directory='templates')

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['*'])
]

accountdata = [{"type":"bank-draft","title":"bank draft","position":0},
               {"type":"bill-of-lading","title":"bill of lading","position":1},
               {"type":"invoice","title":"invoice","position":2},
               {"type":"bank-draft-2","title":"bank draft 2","position":3},
               {"type":"bill-of-lading-2","title":"bill of lading 2","position":4}]

app = Starlette(middleware=middleware)
    
@app.route('/get',methods=["GET"])
async def homepage(request):
    return JSONResponse(account.get_details())
    
    
@app.route('/create',methods=["POST"])
async def create(request):
    body = await request.body()
    json = await request.json()
       
    account.create_activity(json)
    message = {'status': 'Successfully inserted!'}
    return JSONResponse(message)

@app.route('/delete',methods=["POST"])
async def deleteRequest(request):
    type = request.query_params['type']
    print('type',type)
    account.delete(type)
    message = {'status': 'Successfully deleted!'}
    return JSONResponse(message)

@app.route('/error')
async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)


if __name__ == "__main__":
    try:
        connect_db()
        Account.create_table(True)        
        account.create_activities(accountdata)   
        
                    
    except peewee.OperationalError as oe:
        if oe.args[0] == 2003:
            logging.error("Failed to connect to MySQL, won't start till db is available")
        else:
            logging.error("An error occurred while creating tables, won't start till db is available")
        logging.error(oe)
    except Exception as e:
        logging.error("An error occurred while creating tables, won't start till tables are created")
        logging.error(e)
    finally:
         close_db()
    
uvicorn.run(app, port=8000)

			
			