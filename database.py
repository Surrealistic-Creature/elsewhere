import pprint
import outsource

async def insertion(db):
    document = {'nest':'collection'}
    result = await db.information.insert_one(document)
    print('result %s' % repr(result.inserted_id))


async def outload(db):
    document = db.information.find({})
    test = await document.to_list(length=100)
    for element in test:
        element['_id'] = str(element['_id'])
    return test

async def do_count(db):
    n = await db.information.count_documents({})
    print('%s docs in collection' % n)


async def del_many(db):
    coll = db.information
    d = await coll.count_documents({})
    print('%s docs in collection before delete' % d)
    result = await db.information.delete_many({})
    print('%s documents after' % (await coll.count_documents({})))


async def add_document(db):
    vkapi = outsource
    some_info = vkapi.main_auth()
    try:
        result = await db.information.insert_one(some_info)
        try:
            print('frendlist ok', some_info)
        except Exception:
            print('something went wrong on print frendlist')
        try:
            print('result ok', 'result %s' % repr(result.inserted_id))
        except:
            print('something went wrong on print !result!')
    except Exception:
        print('error on insert')



#async def modify_document():
#    document = db.information.find({})

#for one big document with many items
async def split_doc(db):
    cursor = db.information.find({})
    document = await cursor.to_list(length=1)
    for item in document:
        item['_id'] = str(item['_id'])
    req = await db.information.insert_many(
        document[0].get('items'))
    print('inserted %d docs' % (len(req.inserted_ids),))


