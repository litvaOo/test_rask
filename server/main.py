from aiohttp import web
import jinja2
import aiohttp_jinja2
import motor.motor_asyncio
import pymongo
import json
import re


async def index_handler(request):
    context = {}
    response = aiohttp_jinja2.render_template(
        "index.html", request, context)
    return response


async def autocomplete_handler(request):
    res = await app.collection.create_index([("word", pymongo.TEXT)])
    regex = re.compile(request.query.get('q'))
    cursor = app.collection.find({"word": {"$regex": regex}})
    print('/' + request.query.get('q') + '/', flush=True)
    print(cursor, flush=True)
    print(request.query.get('q'), flush=True)
    list_of_suggestions = []
    for doc in await cursor.to_list(length=100):
        print(doc, flush=True)
        list_of_suggestions.append({"word": doc.get('word')})

    return web.json_response(json.dumps(list_of_suggestions))


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(''))
app.client = motor.motor_asyncio.AsyncIOMotorClient('database', 27017)
app.db = app.client.test
app.collection = app.db.test_collection
app.router.add_get('/auto_complete', autocomplete_handler)
app.router.add_get('/', index_handler)

web.run_app(app, host='0.0.0.0', port=80)
