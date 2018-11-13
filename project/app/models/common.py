
from sqlalchemy import Column, String, Integer
from project.app.models.baseModel import BaseModel


class Config(BaseModel):
    __tablename__ = 'tb_config'

    # "CFGPRM_KEY" character varying(100) NOT NULL, -- ID name for a configurable parameter value
    key = Column("cfgprm_key", String(100), primary_key=True)

    # "CFGPRM_VAL" character varying(100) NOT NULL, -- Parameter value for a configurable system parameter
    value = Column("cfgprm_val", String(60))

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))
