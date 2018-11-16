
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from project.app.models.baseModel import BaseModel

userSecurityAssociation = Table('tb_user_scrty',
                                BaseModel.metadata,
                                Column('user_id', Integer, ForeignKey('tb_user.user_id')),
                                Column('scrgrp_id', Integer, ForeignKey('tb_scrty_grp.scrgrp_id'))
                                )

userOauth2ClientAssociation = Table('tb_user_oauth2_client',
                                    BaseModel.metadata,
                                    Column('user_id', Integer, ForeignKey('tb_user.user_id')),
                                    Column('oauth2cl_id', Integer, ForeignKey('tb_oauth2_client.oauth2cl_id'))
                                    )


class User(BaseModel):
    __tablename__ = 'tb_user'

    # USER_ID		System-generated ID for a User.
    user_id = Column("user_id", Integer, primary_key=True)

    def get_user_id(self):
        return self.user_id

    def get_formatted_name(self):
        if self.last_name:
            formatted_name = ""
            if self.first_name:
                formatted_name = self.first_name + " "
            formatted_name += self.last_name
            return formatted_name
        else:
            return self.username

    user_uuid = Column("user_uuid", String(36), unique=True)

    # USER_FNAME		First Name of the User	
    first_name = Column("user_fname", String(50))
    
    # USER_LNAME		Last Name of the User
    last_name = Column("user_lname", String(80))

    # # USERNAME		Username for a User	
    username = Column("username", String(100))

    # # USER_PASSWD		Hashed password used in USERNAME authentication
    password_hash = Column("user_passwd", String(256))

    # # USER_PASSWD_SALT		Used in hashing and authentication	
    password_salt = Column("user_passwd_salt", String(32))

    # # USRTYP_CD		Code value for user type (staff, camper)	
    type_cd = Column("usrtyp_cd", String(2))
    
    # # USER_ATTEMPT_CNT		Number of attempts since the last sucessful login.	
    failed_attempt_count = Column("user_attempt_cnt", Integer)
    
    # # USER_ATTEMPT_TS		When the last login attempt was made.	
    last_attempts_ts = Column("user_attempt_ts", DateTime)
    
    # # USER_PRIV_KEY		Used for encrypting the data specific to the user.	
    private_key = Column("user_priv_key", String(32))
    
    # # USER_ACTV_CODE		A code that is used to Reactivate an account that got deactivated.	
    activation_code = Column("user_actv_code", String(32))
    
    # # USER_RESET_CODE		Encrypted code passed to the user at the point of a password reset.	
    reset_code = Column("user_reset_code", String(32))
    
    # # USRSTA_CD		User Status Code	
    status_cd = Column("usrsta_cd", String(1))

    security_groups = relationship("SecurityGroup",
                                   secondary=userSecurityAssociation)

    oauth2_clients = relationship("OAuth2Client",
                                  secondary=userOauth2ClientAssociation)

    def is_active(self):
        if self.status_cd == 'A':
            return True
        else:
            return False

    def __repr__(self):
        return "<User(uuid='%s', username='%s')>" % (self.user_uuid, self.username)
