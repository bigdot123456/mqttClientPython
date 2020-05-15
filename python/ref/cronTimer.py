import datetime

from apscheduler.schedulers.background import BackgroundScheduler


def job_func(text):
    print("当前时间：", datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])


scheduler = BackgroundScheduler()
# 在每年 1-3、7-9 月份中的每个星期一、二中的 00:00, 01:00, 02:00 和 03:00 执行 job_func 任务
scheduler.add_job(job_func, 'cron', hour=19,minute=23)

scheduler.start()
