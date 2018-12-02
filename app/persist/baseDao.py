from app.persist.infrastructure import session_factory


def get_session():
    return session_factory()
