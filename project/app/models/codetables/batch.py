import json

from sqlalchemy import Column, String

from project.app.models.baseModel import BaseModel


class CtBatchJobCodes(BaseModel):
    __tablename__ = 'TB_BATCH_JOB_CD'

    # "BATJOC_CD" character varying(10) NOT NULL, -- Batch Job Code value   
    code = Column("BATJOC_CD", String(10), primary_key=True, nullable=False)

    #  BATJOC_DE" character varying(30) NOT NULL, -- Batch Job Code description
    description = Column("BATJOC_DE", String(30), nullable=False)

    def __repr__(self):
        return "<CtBatchJobCodes(code='%s', description='%s')>" % (self.code, self.description)

    def serialize(self):
        return json.dumps({"code": self.code, "description": self.description})  

class CtBatchJobStatuses(BaseModel):
    __tablename__ = 'TB_BATCH_JOB_STATUS_CD'

    # "BATJOBSTA_CD" character varying(10) NOT NULL, -- Batch Status Code value 
    code = Column("BATJOBSTA_CD", String(10), primary_key=True, nullable=False)

    #  "BATJOBSTA_DE" character varying(50) NOT NULL, -- Batch Status Code description
    description = Column("BATJOBSTA_DE", String(30), nullable=False)

    def __repr__(self):
        return "<CtBatchJobStatuses(code='%s', description='%s')>" % (self.code, self.description)

    def serialize(self):
        return json.dumps({"code": self.code, "description": self.description})        