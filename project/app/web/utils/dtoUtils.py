

def userSerialize(user):
    return {"id": user.id, "firstName": user.firstName, "lastName": user.lastName, "username": user.username}


def codetableSerialize(codetableData):
    data = []
    for codetableItem in codetableData:
        data.append({"code": codetableItem.code.strip(), "description": codetableItem.description.strip()})
    return data


def authoritySerialize(authorities):
    data = []
    for a in authorities:
        data.append(a.key)
    return data