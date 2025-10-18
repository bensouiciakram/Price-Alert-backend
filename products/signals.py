import os
import logging  
from django.db.models.signals import post_delete, pre_delete, pre_save
from django.dispatch import receiver 
from alert.scheduler import scheduler 
from django.core.mail import send_mail
from .models import Product, PriceHistory
from alert.models import Alert, AlertMet

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=Product)
def delete_product_metadata(sender, instance, **kwargs):
    if instance.meta:
        try:
            instance.meta.delete()
            logger.info(f"Deleted metadata for product ID {instance.id}")
        except Exception as e:
            logger.exception(f"Failed to delete metadata for product ID {instance.id}: {e}")


@receiver(pre_delete, sender=Product)
def delete_product_jobs(sender, instance, **kwargs):
    if not scheduler.running:
        scheduler.start()

    related_alerts = Alert.objects.filter(product=instance)
    for alert in related_alerts:
        job_id = f'scrape_alert_{alert.id}'
        try:
            scheduler.remove_job(job_id, jobstore="default")
            logger.info(f"Removed scheduled job {job_id} for alert ID {alert.id}")
        except Exception:
            logger.warning(f"Could not remove job {job_id} for alert ID {alert.id}")


@receiver(pre_save, sender=PriceHistory)
def send_alert(sender, instance, **kwargs):
    product = instance.product
    alerts = product.alerts

    if not alerts:
        return  # no need to log this every time

    alert = alerts.first()
    threshold = alert.threshold

    if instance.price < threshold:
        logger.info(f"Price dropped below threshold for product ID {product.id}")

        AlertMet.objects.create(alert=alert)
        if alert.channel.name == 'gmail':
            try:
                send_mail(
                    f'{product.meta.title} alert',
                    f'{product.meta.title} is under {threshold}',
                    from_email=os.environ.get('EMAIL_HOST_USER'),
                    recipient_list=["bensouiciakram@gmail.com"],
                    fail_silently=False,   
                )
                logger.info(f"Email alert sent for {product.meta.title}")
            except Exception as e:
                logger.exception(f"Failed to send alert email for {product.meta.title}: {e}")
