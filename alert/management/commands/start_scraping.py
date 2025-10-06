from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from alert.scheduler import set_periodic_scraping
from alert.models import Alert

class Command(BaseCommand):
    help = 'Starts the APScheduler for periodic scraping jobs'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        alerts = Alert.objects.all()
        for alert in alerts:
            scheduler.add_job(
                set_periodic_scraping,
                'interval',
                seconds=alert.frequency,
                args=[alert.id],
                id=f"scrape_alert_{alert.id}",
                replace_existing=True,
                max_instances=1
            )
        scheduler.start()
        self.stdout.write(self.style.SUCCESS('Scheduler started. Press Ctrl+C to exit.'))
        try:
            # Keep the command running
            import time
            while True:
                time.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()