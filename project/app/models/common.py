import json

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date, DateTime
from sqlalchemy.orm import relationship, base

from project.app.models.baseModel import BaseModel


class Config(BaseModel):
    __tablename__ = 'TB_CONFIG'


    # "CFGPRM_ID" integer NOT NULL, -- Surrogate ID for a configurable system parameter
    id = Column("CFGPRM_ID", Integer, primary_key=True)

    # "CFGPRM_KEY" character varying(100) NOT NULL, -- ID name for a configurable parameter value
    key = Column("CFGPRM_KEY", String(100)) 

    # "CFGPRM_VAL" character varying(100) NOT NULL, -- Parameter value for a configurable system parameter
    value = Column("CFGPRM_VAL", String(60)) 
