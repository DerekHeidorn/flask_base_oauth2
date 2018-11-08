from project.app.persist.infrastructure import Session


def get_session():
    return Session()
