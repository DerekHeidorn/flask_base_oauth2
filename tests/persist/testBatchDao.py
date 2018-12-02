from datetime import datetime
from tests.persist.baseTest import BaseTest
from app.persist import batchDao
from app.models.batch import BatchJob


class BatchDaoTestCase(BaseTest):

    def test_get_batch_jobs(self):
        print("running test_get_batch_jobs...")

        batch_jobs = batchDao.get_batch_jobs()

        self.assertTrue(len(batch_jobs) > 0)

        batch_job = batch_jobs[0]
        self.assertEqual(1, batch_job.batch_job_id)
        self.assertEqual('STATS', batch_job.job_code)
        self.assertEqual('COMPLETED', batch_job.status_code)
        self.assertEqual('Testing Stats!', batch_job.details)

    def test_get_batch_job_by_id(self):
        print("running get_batch_job_by_id...")

        batch_job = batchDao.get_batch_job_by_id(1)

        # 1, 'STATS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'COMPLETED',
        # 'Testing Stats!'

        self.assertEqual(1, batch_job.batch_job_id)
        self.assertEqual('STATS', batch_job.job_code)
        self.assertEqual('COMPLETED', batch_job.status_code)
        self.assertEqual('Testing Stats!', batch_job.details)

    def test_add_batch_job(self):
        print("running test_add_batch_job...")

        batch_job = BatchJob()
        batch_job.start_ts = datetime.now()
        batch_job.job_code = 'STATS'
        batch_job.details = "Testing Stats!"
        batch_job.status_code = 'COMPLETED'
        batch_job.end_ts = datetime.now()

        print("batch_job->type=" + str(type(batch_job)))
        print("batch_job=" + str(batch_job))

        batch_job_id = batchDao.add_batch_job(batch_job)
        added_batch_job = batchDao.get_batch_job_by_id(batch_job_id)

        self.assertEqual(batch_job.job_code, added_batch_job.job_code)
