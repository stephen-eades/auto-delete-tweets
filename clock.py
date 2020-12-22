from apscheduler.schedulers.blocking import BlockingScheduler
import delete

sched = BlockingScheduler()

# This job runs every day at 4am
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=1530)
def scheduled_job():
    delete.delete_old_tweets()

sched.start()