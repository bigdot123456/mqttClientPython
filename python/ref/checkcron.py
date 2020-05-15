from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler


# @sched.scheduled_job('cron', id='my_job_id', minute=1)
from apscheduler.triggers.cron import CronTrigger


def tick():
    print('Tick! The time is: %s' % datetime.now())

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # scheduler.add_job(tick, 'cron', hour=19,minute=23)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))
    # scheduler.add_job(tick, CronTrigger.from_crontab('0 * * * *'))
    scheduler.add_job(tick, 'interval', seconds=2)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass