import time
import schedule
from project.app.services import schedulerService

print("setting up scheduler")
schedule.every(2).minutes.do(schedulerService.run_stats)

# while True:
#     schedule.run_pending()
#     time.sleep(10)
