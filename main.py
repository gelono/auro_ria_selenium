from apscheduler.schedulers.background import BackgroundScheduler

from parse_tools.parse_utils import ParseUtils

parse_utils = ParseUtils()
scheduler = BackgroundScheduler()
scheduler.add_job(parse_utils.manager, 'cron', hour=12)
scheduler.add_job(parse_utils.bd_dump, 'cron', hour=0)


if __name__ == '__main__':
    scheduler.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
