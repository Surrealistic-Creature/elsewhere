import pprint
import outsource
from postgredb import Friend, Session

async def insertion(db):
    document = {'nest':'collection'}
    result = await db.information.insert_one(document)
    print('result %s' % repr(result.inserted_id))


async def outload(db):
    document = db.information.find({})
    test = await document.to_list(length=100)
    for element in test:
        element['_id'] = str(element['_id'])
        #print(test)
    return test

async def print_people(db):
    doc_people = db.people.find({})
    press = await doc_people.to_list(length=75)
    for element in press:
        element['_id'] = str(element['_id'])
    return press

async def do_count_docs(db):
    n = await db.information.count_documents({})
    print('%s docs in collection' % n)
    h = await db.people.count_documents({})
    print('%s docs in collection' % h)

async def del_one(db):
    coll = db.people
    d = await coll.count_documents({})
    print('%s docs in collection before delete' % d)
    result = await db.information.delete_one({})


async def del_many(db):
    coll = db.people
    d = await coll.count_documents({})
    print('%s docs in collection before delete' % d)
    result = await db.people.delete_many({})
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
    req = await db.people.insert_many(
        document[0].get('items'))
    print('inserted %d docs' % (len(req.inserted_ids),))


async def import_friend(db):
    session = Session()
    u = await print_people(db)
    for friend in u:
        pfriend = Friend(
            first_name=friend['first_name'],
            vk_id=friend['id'],
            last_name=friend['last_name'],
            sex=friend['sex'],
            nickname=friend['nickname'],
            domain=friend['domain']
        )
        session.add(pfriend)
    session.commit()
    session.close()


def show_postgre():
    session = Session()
    users = session.query(Friend).all()
    for user in users:
        print(user.first_name, user.last_name, user.vk_id)
    session.close()