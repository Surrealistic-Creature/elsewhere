async def insertion(db):
    document = {'test':'collection'}
    result = await db.information.insert_one(document)
    print('result %s' % repr(result.inserted_id))
