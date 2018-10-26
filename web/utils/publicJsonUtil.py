import json

def userSerialize(user):
    return {"id": user.id, "firstName": user.firstName, "lastName": user.lastName, "login": user.login}

def codetableSerialize(codetableData):
    data = []
    for codetableItem in codetableData:
        data.append({"code": codetableItem.code.strip(), "description": codetableItem.description.strip()})
    return data