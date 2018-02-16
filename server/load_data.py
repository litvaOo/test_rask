import motor.motor_asyncio
import asyncio
client = motor.motor_asyncio.AsyncIOMotorClient('database', 27017)

db = client.test
collection = db.test_collection

async def read_and_insert():
    with open('file.txt') as f:
        for line in f.readlines():
            number, word = line.strip().split(" ")
            doc_to_insert = {"popularity": int(number), "word": word}
            result = await collection.insert_one(doc_to_insert)
            print('result %s' % repr(result.inserted_id))
    collection.create_index("word")

loop = asyncio.get_event_loop()
loop.run_until_complete(read_and_insert())