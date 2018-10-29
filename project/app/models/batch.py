import json

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date, DateTime
from sqlalchemy.orm import relationship, base

from project.app.models.baseModel import BaseModel


class BatchJob(BaseModel):
    __tablename__ = 'TB_BATCH_JOB'

    # TB_BATCH_JOB
    # "BATJOB_ID" integer NOT NULL, -- Batch Job ID
    id = Column("BATJOB_ID", Integer, primary_key=True)

    # "BATJOC_CD" character varying(10) NOT NULL, -- Batch Job Code value
    jobCode = Column("BATJOC_CD", String(10)) 

    # "BATJOB_START_TS" timestamp without time zone NOT NULL, -- Start Date of a Batch Job	
    startTs = Column("BATJOB_START_TS", DateTime)

    # "BATJOB_END_TS" timestamp without time zone, -- End Date of a Batch Job
    endTs = Column("BATJOB_END_TS", DateTime)

    # "BATSTA_CD" character varying(10) NOT NULL, -- Batch Status Code value
    statusCode = Column("BATJOBSTA_CD", String(10))

    # "BATJOB_DETAILS" character varying(200), -- Details of the batch job
    details = Column("BATJOB_DETAILS", String(200))

