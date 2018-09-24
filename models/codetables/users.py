import json

from sqlalchemy import Column, String

from models.baseModel import BaseModel


class CtUserStatuses(BaseModel):
    __tablename__ = 'TB_USER_TYP_CD'

    # "USRTYP_CD" character(2) NOT NULL,
    code = Column("USRTYP_CD", String(2), primary_key=True, nullable=False)

    #  "USRTYP_DE" character(20) NOT NULL,	
    description = Column("USRTYP_DE", String(30), nullable=False)

    def __repr__(self):
        return "<CtUserStatuses(code='%s', description='%s')>" % (self.code, self.description)

    def serialize(self):
        return json.dumps({"code": self.code, "description": self.description})    

class CtUserTypes(BaseModel):
    __tablename__ = 'TB_USER_STA_CD'

    #   "USRSTA_CD" character(1) NOT NULL, -- User Status Code
    code = Column("USRSTA_CD", String(1), primary_key=True, nullable=False)

    #   "USRSTA_DE" character(30) NOT NULL, -- User Status Description	
    description = Column("USRSTA_DE", String(30), nullable=False)

    def __repr__(self):
        return "<CtUserTypes(code='%s', description='%s')>" % (self.code, self.description)

    def serialize(self):
        return json.dumps({"code": self.code, "description": self.description})           