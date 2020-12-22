from apscheduler.schedulers.blocking import BlockingScheduler
import delete

sched = BlockingScheduler()

# This job runs every day at 4am
@sched.scheduled_job('cron', day_of_week='mon-sun', hour='4', minute="00", timezone='America/New_York')
def scheduled_job():
    delete.delete_old_tweets()

sched.start()