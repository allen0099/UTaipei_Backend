from app import scheduler

__all__ = ['sync_tables']


@scheduler.task('cron', id='sync_tables', hour='*/12')
def sync_tables():
    print('Syncing tables...')
