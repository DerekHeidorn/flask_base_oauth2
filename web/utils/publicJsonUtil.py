import json

def userSerialize(user):
        return {"id": user.id, "firstName": user.firstName, "lastName": user.lastName, "login": user.login}