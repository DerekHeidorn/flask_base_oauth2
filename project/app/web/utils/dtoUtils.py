

def user_serialize(user):
    return {"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "username": user.username}


def codetable_serialize(codetable_data):
    data = []
    for item in codetable_data:
        data.append({"code": item.code.strip(), "description": item.description.strip()})
    return data


def authority_serialize(authorities):
    data = []
    for a in authorities:
        data.append(a.key)
    return data
