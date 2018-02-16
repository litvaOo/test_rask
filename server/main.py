from aiohttp import web
import jinja2
import aiohttp_jinja2
import motor.motor_asyncio
import pymongo
import json


async def index_handler(request):
    context = {}
    response = aiohttp_jinja2.render_template(
        "index.html", request, context)
    return response


async def autocomplete_handler(request):
    res = await app.collection.create_index([("word", pymongo.TEXT)])
    cursor = app.collection.find({"$text": {'$search': request.query.get('q') }}).sort("popularity").limit(3)
    print(cursor, flush=True)
    print(request.query.get('q'), flush=True)
    list_of_suggestions = []
    for doc in await cursor.to_list(length=3):
        list_of_suggestions.append({"word": doc.get('word')})
    
    return web.json_response(json.dumps(list_of_suggestions), headers={"Content-Type": "application/json; charset=utf-8"})


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(''))
app.client = motor.motor_asyncio.AsyncIOMotorClient('database', 27017)
app.db = app.client.test
app.collection = app.db.test_collection
app.router.add_get('/auto_complete', autocomplete_handler)
app.router.add_get('/', index_handler)

web.run_app(app, host='0.0.0.0', port=80)

    # cursor = app.collection.find({word: {'$search': request.query.get('q') }}).sort("popularity").limit(3)
    # cursor = await app.db.command({"text": {"search": "dogs"}})
    # print(dir(response), flush=True)
    # print(response.result(), flush=True)
    # for document in await cursor.to_list(length=3):
    #     print(document, flush=True)