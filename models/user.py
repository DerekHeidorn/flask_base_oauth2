import json

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date, DateTime
from sqlalchemy.orm import relationship, base

from models.baseModel import BaseModel


class User(BaseModel):
    __tablename__ = 'TB_USER'

	
    # USER_ID		System-generated ID for a User.
    id = Column("USER_ID", Integer, primary_key=True)

    # USER_FNAME		First Name of the User	
    first_name = Column("USER_FNAME", String(50))
    
    # USER_LNAME		Last Name of the User
    last_name = Column("USER_LNAME", String(80))

    # # USER_LOGIN		Login ID for a User	
    login = Column("USER_LOGIN", String(100))

    # # USER_PASSWD		Hashed password used in login authentication
    password_hash = Column("USER_PASSWD", String(256))	

    # # USER_PASSWD_SALT		Used in hashing and authentication	
    password_salt = Column("USER_PASSWD_SALT", String(32))
    
    # # USER_PASSWD_EXP_TS		A timestamp for expiring a password, used for temporary passwords
    password_expire_ts = Column("USER_PASSWD_EXP_TS", DateTime)
    
    # # USRTYP_CD		Code value for user type (staff, camper)	
    type_cd = Column("USRTYP_CD", String(2))
    
    # # USER_ATTEMPT_CNT		Number of attempts since the last sucessful login.	
    failed_attempt_cnt = Column("USER_ATTEMPT_CNT", Integer)
    
    # # USER_ATTEMPT_TS		When the last login attempt was made.	
    attempts_ts = Column("USER_ATTEMPT_TS", DateTime)
    
    # # USER_PRIV_KEY		Used for encrypting the data specific to the user.	
    private_key = Column("USER_PRIV_KEY", String(32))
    
    # # USER_ACTV_CODE		A code that is used to Reactivate an account that got deactivated.	
    user_actv_code = Column("USER_ACTV_CODE", String(32))
    
    # # USER_RESET_CODE		Encrypted code passed to the user at the point of a password reset.	
    reset_code = Column("USER_RESET_CODE", String(32))
    
    # # USRSTA_CD		User Status Code	
    status_cd = Column("USRSTA_CD", String(1))
    
    # # USER_RESET_PRSN_ID		ID of the individual (Staff User) who performed the reset	
    reset_by_user = Column("USER_RESET_PRSN_ID", Integer, nullable=True)
    
    def __repr__(self):
        return "<User(id='%i', login='%s')>" % (self.id, self.login)

    def serialize(self):
        return json.dumps({"id": self.id, "first_name": self.first_name, "last_name": self.last_name, "login": self.login})