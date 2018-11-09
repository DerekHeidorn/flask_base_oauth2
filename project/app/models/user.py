
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from project.app.models.baseModel import BaseModel

userSecurityAssociation = Table('TB_USER_SCRTY',
                                BaseModel.metadata,
                                Column('USER_ID', Integer, ForeignKey('TB_USER.USER_ID')),
                                Column('SCRGRP_ID', Integer, ForeignKey('TB_SCRTY_GRP.SCRGRP_ID'))
                                )

userOauth2ClientAssociation = Table('TB_USER_OAUTH2_CLIENT',
                                    BaseModel.metadata,
                                    Column('USER_ID', Integer, ForeignKey('TB_USER.USER_ID')),
                                    Column('OAUTH2CL_ID', Integer, ForeignKey('TB_OAUTH2_CLIENT.OAUTH2CL_ID'))
                                    )


class User(BaseModel):
    __tablename__ = 'TB_USER'

    # USER_ID		System-generated ID for a User.
    id = Column("USER_ID", Integer, primary_key=True)

    def get_user_id(self):
        return self.id

    uuid = Column("USER_UUID", Integer, unique=True)

    # USER_FNAME		First Name of the User	
    first_name = Column("USER_FNAME", String(50))
    
    # USER_LNAME		Last Name of the User
    last_name = Column("USER_LNAME", String(80))

    # # USERNAME		Username for a User	
    username = Column("USERNAME", String(100))

    # # USER_PASSWD		Hashed password used in USERNAME authentication
    password_hash = Column("USER_PASSWD", String(256))

    # # USER_PASSWD_SALT		Used in hashing and authentication	
    password_salt = Column("USER_PASSWD_SALT", String(32))
    
    # # USER_PASSWD_EXP_TS		A timestamp for expiring a password, used for temporary passwords
    password_expire_ts = Column("USER_PASSWD_EXP_TS", DateTime)
    
    # # USRTYP_CD		Code value for user type (staff, camper)	
    type_cd = Column("USRTYP_CD", String(2))
    
    # # USER_ATTEMPT_CNT		Number of attempts since the last sucessful login.	
    failed_attempt_count = Column("USER_ATTEMPT_CNT", Integer)
    
    # # USER_ATTEMPT_TS		When the last login attempt was made.	
    last_attempts_ts = Column("USER_ATTEMPT_TS", DateTime)
    
    # # USER_PRIV_KEY		Used for encrypting the data specific to the user.	
    private_key = Column("USER_PRIV_KEY", String(32))
    
    # # USER_ACTV_CODE		A code that is used to Reactivate an account that got deactivated.	
    user_activation_code = Column("USER_ACTV_CODE", String(32))
    
    # # USER_RESET_CODE		Encrypted code passed to the user at the point of a password reset.	
    reset_code = Column("USER_RESET_CODE", String(32))
    
    # # USRSTA_CD		User Status Code	
    status_cd = Column("USRSTA_CD", String(1))
    
    # # USER_RESET_PRSN_ID		ID of the individual (Staff User) who performed the reset	
    reset_by_user = Column("USER_RESET_PRSN_ID", Integer, nullable=True)

    security_groups = relationship("SecurityGroup",
                                   secondary=userSecurityAssociation)

    oauth2_clients = relationship("OAuth2Client",
                                  secondary=userOauth2ClientAssociation)

    def __repr__(self):
        return "<User(uuid='%s', username='%s')>" % (self.uuid, self.username)
