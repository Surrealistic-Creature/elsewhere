import pprint

async def insertion(db):
    document = {'nest':'collection'}
    result = await db.information.insert_one(document)
    print('result %s' % repr(result.inserted_id))


async def outload(db):
    document = db.information.find({})
    test = await document.to_list(length=10)
    for element in test:
        element['_id'] = str(element['_id'])
 
    #print('test outload', test)
    return test 
    #for data in await document.to_list(length=10):
        #print('from db outload', data)
        #return test
