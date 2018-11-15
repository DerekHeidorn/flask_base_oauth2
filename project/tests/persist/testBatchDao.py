from datetime import datetime
from project.tests.persist.baseTest import BaseTest
from project.app.persist import batchDao
from project.app.models.batch import BatchJob


class BatchDaoTestCase(BaseTest):

    def test_add_batch_job(self):
        print("running test_add_batch_job...")
        start_ts = datetime.utcnow()
        end_ts = datetime.utcnow()

        batch_job = BatchJob
        batch_job.start_ts = start_ts
        batch_job.job_code = 'STATS'
        batch_job.details = "Testing Stats!"
        batch_job.status_code = 'COMPLETED'
        batch_job.end_ts = end_ts

        batch_job_id = batchDao.add_batch_job(batch_job)
        added_batch_job = batchDao.get_batch_job_by_id(batch_job_id)

        self.assertEquals(batch_job.job_code, added_batch_job.job_code)
