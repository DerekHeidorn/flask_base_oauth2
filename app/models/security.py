
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.baseModel import BaseModel


securityGroupAuthAssociation = Table('tb_scrty_grp_auth',
                                     BaseModel.metadata,
                                     Column('scrgrp_id', Integer, ForeignKey('tb_scrty_grp.scrgrp_id')),
                                     Column('scrauth_id', Integer, ForeignKey('tb_scrty_auth.scrauth_id'))
                                     )


class SecurityAuthority(BaseModel):
    __tablename__ = 'tb_scrty_auth'

    # "SCRAUTH_ID" integer NOT NULL, -- Security Authority Surrogate Key
    id = Column("scrauth_id", Integer, primary_key=True)

    # "SCRAUTH_KEY" character varying(60) NOT NULL, -- Unique key name of the security authority 
    key = Column("scrauth_key", String(60))

    # "SCRAUTH_NAME" character varying(60) NOT NULL, -- Authority Name, used within the application to
    # reference the authority
    name = Column("scrauth_name", String(60))

    # "SCRAUTH_DE" character varying(200) NOT NULL, -- Authority Description, to be displayed within
    # the administration screens.
    description = Column("scrauth_de", String(200))

    def __repr__(self):
        return "<SecurityAuthority(id='%i', key='%s')>" % (self.id, self.key)


class SecurityGroup(BaseModel):
    __tablename__ = 'tb_scrty_grp'

    # "SCRGRP_ID" integer NOT NULL, -- Security Group Surrogate Key
    id = Column("scrgrp_id", Integer, primary_key=True)

    # "SCRGRP_NAME" character varying(60) NOT NULL, -- Security group name
    name = Column("scrgrp_name", String(60))

    # "SCRGRP_DE" character varying(200) NOT NULL, -- Security Group Description
    description = Column("scrgrp_de", String(200))
   
    # "SCRGRP_LEVEL" integer NOT NULL DEFAULT 100, -- Security Level of the Security Group
    level = Column("scrgrp_level", Integer)

    authorities = relationship("SecurityAuthority", 
                               secondary=securityGroupAuthAssociation)

    def __repr__(self):
        return "<SecurityGroup(id='%i', name='%s')>" % (self.id, self.name)
