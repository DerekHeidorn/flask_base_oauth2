from sqlalchemy.sql import text
from sqlalchemy.sql import column
from sqlalchemy.sql import select

from project.app.persist import baseDao
from project.app.models.batch import BatchJob


def get_batch_job_by_id(batch_job_id, session=None):

    if session is None:
        session = baseDao.get_session()

    batch_item = session.query(BatchJob).filter(BatchJob.batch_job_id == batch_job_id).first()
    return batch_item


def add_batch_job(batch_job, session=None):
    """
    Creates and saves a BatchJob to the database.

    :param batch_job: new BatchJob record
    :param session: database session

    """
    if session is None:
        session = baseDao.get_session()

    session.add(batch_job)
    session.commit()

    return batch_job.batch_job_id


def update_batch_job(batch_job_id, end_ts, details):
    session = baseDao.get_session()

    batch_job = get_batch_job_by_id(batch_job_id, session=session)

    batch_job.end_ts = end_ts
    batch_job.details = details

    session.commit()
    updated_batch_job = get_batch_job_by_id(batch_job_id, session=session)

    return updated_batch_job
