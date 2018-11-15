from sqlalchemy import Column, String, Integer, DateTime
from project.app.models.baseModel import BaseModel
from datetime import datetime


class BatchJob(BaseModel):
    __tablename__ = 'tb_batch_job'

    # "BATJOB_ID" integer NOT NULL, -- Batch Job ID
    batch_job_id = Column("batjob_id", Integer, primary_key=True)

    # "BATJOC_CD" character varying(10) NOT NULL, -- Batch Job Code value
    job_code = Column("batjoc_cd", String(10))

    # "BATJOB_START_TS" timestamp without time zone NOT NULL, -- Start Date of a Batch Job
    start_ts = Column("batjob_start_ts", DateTime, default=datetime.utcnow)

    # "BATJOB_END_TS" timestamp without time zone, -- End Date of a Batch Job
    end_ts = Column("batjob_end_ts", DateTime)

    # "BATJOBSTA_CD" character varying(10) NOT NULL, -- Batch Status Code value
    status_code = Column("batjobsta_cd", String(10))

    # "BATJOB_DETAILS" character varying(200), -- Details of the batch job
    details = Column("batjob_details", String(200))

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))
