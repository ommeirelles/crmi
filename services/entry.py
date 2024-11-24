from models import EntryModel, Session
from sqlalchemy import select
from sqlalchemy.orm import aliased

def getNamespaceData(namespaceId: int):
    aliasedEntryModel = aliased(EntryModel)

    query = select(
        EntryModel.id,
        EntryModel.key,
        EntryModel.value,
        aliasedEntryModel.key.label("parent")
    ).outerjoin(
        aliasedEntryModel,
        aliasedEntryModel.id == EntryModel.parent and
        aliasedEntryModel.namespace_id == EntryModel.namespace_id
    ).where(EntryModel.namespace_id == namespaceId)

    with Session() as session:
        return __parseNamespaceDataToJson(rows=list(session.execute(query)))

        
def __parseNamespaceDataToJson(rows: list[EntryModel], parentElement: str | None = None, parentObj: dict | None = None) -> dict:
    if (parentElement is None):
        root = [entry for entry in rows if entry.parent is None and entry.value is None]
        if (len(root) == 0): raise Exception("No root found")

        return __parseNamespaceDataToJson(rows, root[0].key, {})

    for entry in [el for el in rows if el.parent == parentElement]:
        if (entry.value == None):
            parentObj[entry.key] = __parseNamespaceDataToJson(rows, entry.key, {})
        elif (entry.value != None and entry.key != None):
            parentObj[entry.key] = entry.value
        else:
            raise Exception("Inconsistent row. id = %d" %  entry.id)
    
    return parentObj


# CTE_JSON_QUERY = """WITH RECURSIVE
#     cte(id, `KEY`, value) AS (
#         SELECT entry.id, entry.KEY, value FROM entry WHERE parent IS null and namespace_id = :nsid
#         UNION ALL
#         SELECT 
#             entry.id, 
#             cte.KEY || "." || entry.KEY, 
#             entry.value 
#         FROM entry 
#         JOIN cte on entry.parent = cte.id  
#     )
#     SELECT key, value FROM cte 
#     WHERE value IS NOT null;
# """

def saveEntry(namespace_id: int, key: str, value: str | None, parent: int | None, session=Session()) -> EntryModel:
    model = EntryModel()
    model.key = key
    model.value = value
    model.parent = parent
    model.namespace_id = namespace_id

    session.add(model)
    session.flush()
    session.refresh(model)
    return model
    
def saveEntryRecursive(obj: dict, namespace_id: int, parent_id: int | None = None, session=Session()):
    parent: EntryModel | None = None
    for key in obj:
        if (type(key) == str):
            value = obj[key]
            if (type(value) == str):
                saveEntry(namespace_id, key, value, parent_id, session=session)
            elif (type(value) ==  dict or type(value) == list):
                parent = saveEntry(namespace_id, key, None, parent_id, session=session)
                saveEntryRecursive(value, namespace_id, parent.id, session=session)
        elif (type(key) == dict):
            saveEntryRecursive(key, namespace_id, parent_id=parent_id, session=session)