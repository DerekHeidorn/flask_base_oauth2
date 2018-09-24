from sqlalchemy.sql import text
from sqlalchemy.sql import column
from sqlalchemy.sql import select

from persist.baseDao import getSession
from models.security import SecurityUser


def getUserSecurity(userId, serialize=False, session=None):

    if(session == None):
        session = getSession()

    user = session.query(SecurityUser).filter(SecurityUser.id == userId).first()

    if(user is not None):
        if serialize:
            return user.serialize()
        else:
            return user
    else:
        return None


