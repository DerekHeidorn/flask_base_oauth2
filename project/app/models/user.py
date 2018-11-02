import json

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date, DateTime, Table
from sqlalchemy.orm import relationship, base

from project.app.models.baseModel import BaseModel

userSecurityAssociation = Table('TB_SCRTY_USER', BaseModel.metadata,
    Column('USER_ID', Integer, ForeignKey('TB_USER.USER_ID')),
    Column('SCRGRP_ID', Integer, ForeignKey('TB_SCRTY_GRP.SCRGRP_ID'))
)

class User(BaseModel):
    __tablename__ = 'TB_USER'

	
    # USER_ID		System-generated ID for a User.
    id = Column("USER_ID", Integer, primary_key=True)

    def get_user_id(self):
        return self.id

    # USER_FNAME		First Name of the User	
    firstName = Column("USER_FNAME", String(50))
    
    # USER_LNAME		Last Name of the User
    lastName = Column("USER_LNAME", String(80))

    # # USER_LOGIN		Login ID for a User	
    login = Column("USER_LOGIN", String(100))

    # # USER_PASSWD		Hashed password used in login authentication
    passwordHash = Column("USER_PASSWD", String(256))	

    # # USER_PASSWD_SALT		Used in hashing and authentication	
    passwordSalt = Column("USER_PASSWD_SALT", String(32))
    
    # # USER_PASSWD_EXP_TS		A timestamp for expiring a password, used for temporary passwords
    passwordExpireTs = Column("USER_PASSWD_EXP_TS", DateTime)
    
    # # USRTYP_CD		Code value for user type (staff, camper)	
    typeCd = Column("USRTYP_CD", String(2))
    
    # # USER_ATTEMPT_CNT		Number of attempts since the last sucessful login.	
    failedAttemptCnt = Column("USER_ATTEMPT_CNT", Integer)
    
    # # USER_ATTEMPT_TS		When the last login attempt was made.	
    attemptsTs = Column("USER_ATTEMPT_TS", DateTime)
    
    # # USER_PRIV_KEY		Used for encrypting the data specific to the user.	
    privateKey = Column("USER_PRIV_KEY", String(32))
    
    # # USER_ACTV_CODE		A code that is used to Reactivate an account that got deactivated.	
    userActvCode = Column("USER_ACTV_CODE", String(32))
    
    # # USER_RESET_CODE		Encrypted code passed to the user at the point of a password reset.	
    resetCode = Column("USER_RESET_CODE", String(32))
    
    # # USRSTA_CD		User Status Code	
    statusCd = Column("USRSTA_CD", String(1))
    
    # # USER_RESET_PRSN_ID		ID of the individual (Staff User) who performed the reset	
    resetByUser = Column("USER_RESET_PRSN_ID", Integer, nullable=True)

    securityGroups = relationship("SecurityGroup", 
                    secondary=userSecurityAssociation)

    def __repr__(self):
        return "<User(id='%i', login='%s')>" % (self.id, self.login)

 