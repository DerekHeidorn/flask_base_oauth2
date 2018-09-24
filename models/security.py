import json

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date, DateTime
from sqlalchemy.orm import relationship, base

from models.baseModel import BaseModel


class SecurityAuthority(BaseModel):
    __tablename__ = 'TB_SCRTY_AUTH'


    # "SCRAUTH_ID" integer NOT NULL, -- Security Authority Surrogate Key
    id = Column("SCRAUTH_ID", Integer, primary_key=True)

    # "SCRAUTH_KEY" character varying(60) NOT NULL, -- Unique key name of the security authority 
    key = Column("SCRAUTH_KEY", String(60))   

    # "SCRAUTH_NAME" character varying(60) NOT NULL, -- Authority Name, used within the application to reference the authority
    name = Column("SCRAUTH_NAME", String(60))    

    # "SCRAUTH_DE" character varying(200) NOT NULL, -- Authority Description, to be displayed within the administration screens.
    description = Column("SCRAUTH_DE", String(200))   

    

    def __repr__(self):
        return "<SecurityAuthority(id='%i', key='%s')>" % (self.id, self.key)

    def serialize(self):
        return json.dumps({"id": self.id, "key": self.key}) 

class SecurityGroup(BaseModel):
    __tablename__ = 'TB_SCRTY_GRP'

    # "SCRGRP_ID" integer NOT NULL, -- Security Group Surrogate Key
    id = Column("SCRGRP_ID", Integer, primary_key=True) 

    # "SCRGRP_NAME" character varying(60) NOT NULL, -- Security group name
    name = Column("SCRGRP_NAME", String(60))    

     # "SCRGRP_DE" character varying(200) NOT NULL, -- Security Group Description
    description = Column("SCRGRP_DE", String(200))      
   
    # "SCRGRP_LEVEL" integer NOT NULL DEFAULT 100, -- Security Level of the Security Group
    level = Column("SCRGRP_LEVEL", Integer) 

    authorities = relationship("SecurityAuthority")

    def __repr__(self):
        return "<SecurityGroup(id='%i', name='%s')>" % (self.id, self.name)

    def serialize(self):
        return json.dumps({"id": self.id, "name": self.name}) 


class SecurityUser(BaseModel):
    __tablename__ = 'TB_USER'  # similar User data model object

    # USER_ID		System-generated ID for a User.
    id = Column("USER_ID", Integer, primary_key=True)    

    # # USER_LOGIN		Login ID for a User	
    login = Column("USER_LOGIN", String(100))    

    securityGroups = relationship("SecurityGroup")  

    def __repr__(self):
        return "<SecurityUser(id='%i', login='%s')>" % (self.id, self.login)

    def serialize(self):
        return json.dumps({"id": self.id, "login": self.login})               