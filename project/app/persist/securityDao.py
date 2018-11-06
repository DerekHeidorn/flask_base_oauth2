

from project.app.persist.baseDao import getSession
from project.app.models.user import User
from project.app.models.security import SecurityGroup

SECURITY_GROUP_CUSTOMER_NAME = "CUSTOMER"


def getUserSecurityAuthorities(userId, session=None):

    if(session == None):
        session = getSession()
    user = session.query(User).filter(User.id == userId).first()

    authorities = []

    for sg in user.securityGroups:
        for sa in sg.authorities:
            authorities.append(sa)
            
    return authorities


def getSecurityGroupByName(securityGroupName, session=None):
    if(session == None):
        session = getSession()

    securityGroup = session.query(SecurityGroup).filter(SecurityGroup.name == securityGroupName).first() 
    print("securityGroup=" + str(securityGroup))
    return securityGroup





