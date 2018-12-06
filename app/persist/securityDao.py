
from app.models.user import User
from app.models.security import SecurityGroup

SECURITY_GROUP_CUSTOMER_NAME = "CUSTOMER"


def get_user_security_authorities(session, user_id):

    user = session.query(User).filter(User.user_id == user_id).first()

    authorities = []

    for sg in user.security_groups:
        for sa in sg.authorities:
            authorities.append(sa)
            
    return authorities


def get_security_group_by_name(session, security_group_name):

    security_group = session.query(SecurityGroup).filter(SecurityGroup.name == security_group_name).first()

    return security_group
