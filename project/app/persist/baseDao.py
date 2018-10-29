from project.app.persist.infrastructure import Session


def getSession():
    return Session()