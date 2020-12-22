from apscheduler.schedulers.blocking import BlockingScheduler
import delete

sched = BlockingScheduler()

# This job is run every day at 4am
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=4)
def scheduled_job():
    delete.delete_old_tweets()

sched.start()