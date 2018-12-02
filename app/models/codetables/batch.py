
from sqlalchemy import Column, String

from app.models.baseModel import BaseModel


class CtBatchJobCode(BaseModel):
    __tablename__ = 'tb_batch_job_cd'

    # "BATJOC_CD" character varying(10) NOT NULL, -- Batch Job Code value   
    code = Column("batjoc_cd", String(10), primary_key=True, nullable=False)

    #  BATJOC_DE" character varying(30) NOT NULL, -- Batch Job Code description
    description = Column("batjoc_de", String(30), nullable=False)

    def __repr__(self):
        return "<CtBatchJobCodes(code='%s', description='%s')>" % (self.code, self.description)


class CtBatchJobStatus(BaseModel):
    __tablename__ = 'tb_batch_job_status_cd'

    # "BATJOBSTA_CD" character varying(10) NOT NULL, -- Batch Status Code value 
    code = Column("batjobsta_cd", String(10), primary_key=True, nullable=False)

    #  "BATJOBSTA_DE" character varying(50) NOT NULL, -- Batch Status Code description
    description = Column("batjobsta_de", String(30), nullable=False)

    def __repr__(self):
        return "<CtBatchJobStatuses(code='%s', description='%s')>" % (self.code, self.description)
