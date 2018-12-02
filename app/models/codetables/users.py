import json

from sqlalchemy import Column, String

from app.models.baseModel import BaseModel


class CtUserStatus(BaseModel):
    __tablename__ = 'tb_user_sta_cd'

    #   "USRSTA_CD" character(1) NOT NULL, -- User Status Code
    code = Column("usrsta_cd", String(2), primary_key=True, nullable=False)

    #   "USRSTA_DE" character(30) NOT NULL, -- User Status Description

    description = Column("usrsta_de", String(30), nullable=False)

    def __repr__(self):
        return "<CtUserStatuses(code='%s', description='%s')>" % (self.code, self.description)

    def serialize(self):
        return json.dumps({"code": self.code, "description": self.description})    

class CtUserType(BaseModel):
    __tablename__ = 'tb_user_typ_cd'

    # "USRTYP_CD" character(2) NOT NULL,
    code = Column("usrtyp_cd", String(1), primary_key=True, nullable=False)

    #  "USRTYP_DE" character(20) NOT NULL,
    description = Column("usrtyp_de", String(30), nullable=False)

    def __repr__(self):
        return "<CtUserTypes(code='%s', description='%s')>" % (self.code, self.description)

    def serialize(self):
        return json.dumps({"code": self.code, "description": self.description})           