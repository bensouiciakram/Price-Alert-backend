# alert/management/commands/start_scraping.py

from django.core.management.base import BaseCommand
from alert.scheduler import scheduler, scheduler_started, set_periodic_scraping
from alert.models import Alert
import time

class Command(BaseCommand):
    help = "Starts the APScheduler for periodic scraping jobs"

    def handle(self, *args, **options):
        global scheduler_started

        if not scheduler_started:
            scheduler.start()
            scheduler_started = True
            self.stdout.write(self.style.SUCCESS("Scheduler started. Press Ctrl+C to exit."))
        else:
            self.stdout.write(self.style.WARNING("Scheduler already running."))

        try:
            while True:
                alerts = Alert.objects.all()
                existing_jobs = {job.id: job for job in scheduler.get_jobs()}

                # --- Add or update jobs ---
                for alert in alerts:
                    job_id = f"scrape_alert_{alert.id}"
                    job = existing_jobs.get(job_id)

                    if job is None:
                        # Add new job for new alert
                        scheduler.add_job(
                            set_periodic_scraping,
                            'interval',
                            seconds=alert.frequency,
                            args=[alert.id],
                            id=job_id,
                            max_instances=1,
                            replace_existing=True
                        )
                        self.stdout.write(self.style.SUCCESS(f"Added job for alert {alert.id}"))

                    elif job.trigger.interval.total_seconds() != alert.frequency:
                        # Update frequency if changed
                        scheduler.reschedule_job(job_id, trigger='interval', seconds=alert.frequency)
                        self.stdout.write(self.style.WARNING(f"Updated frequency for alert {alert.id}"))
                time.sleep(60)  
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            self.stdout.write(self.style.WARNING("Scheduler stopped."))