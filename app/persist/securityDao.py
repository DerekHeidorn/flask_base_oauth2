

from app.persist import baseDao
from app.models.user import User
from app.models.security import SecurityGroup

SECURITY_GROUP_CUSTOMER_NAME = "CUSTOMER"


def get_user_security_authorities(user_id, session=None):

    if session is None:
        session = baseDao.get_session()
    user = session.query(User).filter(User.user_id == user_id).first()

    authorities = []

    for sg in user.security_groups:
        for sa in sg.authorities:
            authorities.append(sa)
            
    return authorities


def get_security_group_by_name(security_group_name, session=None):
    if session is None:
        session = baseDao.get_session()

    security_group = session.query(SecurityGroup).filter(SecurityGroup.name == security_group_name).first()

    return security_group