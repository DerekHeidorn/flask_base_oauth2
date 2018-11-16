
from datetime import datetime
from project.app.models.batch import BatchJob
from project.app.persist import userDao, batchDao


def run_stats():
    start_ts = datetime.now()

    user_count = userDao.get_user_count()
    print("stats: user_count=" + str(user_count))

    end_ts = datetime.now()

    batch_job = BatchJob()
    batch_job.start_ts = start_ts
    batch_job.job_code = 'STATS'
    batch_job.details = "stats: user_count=" + str(user_count)
    batch_job.status_code = 'COMPLETED'
    batch_job.end_ts = end_ts

    batchDao.add_batch_job(batch_job)



# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).days.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
