import os 
from django.db.models.signals import post_delete,pre_delete,pre_save
from django.dispatch import receiver 
from alert.scheduler import scheduler 
from django.core.mail import send_mail
from .models import Product,PriceHistory,Website
from alert.models import Alert,AlertMet


@receiver(post_delete,sender=Product)
def delete_product_metadata(sender,instance,**kwargs):
    if instance.meta :
        instance.meta.delete()


@receiver(pre_delete,sender=Product)
def delete_product_jobs(sender,instance,**kwargs):
    if not scheduler.running:
        scheduler.start()
    related_alerts = Alert.objects.filter(product=instance)
    for alert in related_alerts :
        jobs_id = f'scrape_alert_{alert.id}'
        try :
            scheduler.remove_job(jobs_id,jobstore="default")
        except Exception:
            print('Something is Wrong with job deletion')


@receiver(pre_save,sender=PriceHistory)
def send_alert(sender,instance,**kwargs):
    product = instance.product
    alerts = product.alerts
    if not alerts:
        print('No alerts attached into the product')
        return 
    alert = alerts.first()
    threshold = alert.threshold
    if instance.price < threshold:
        AlertMet.objects.create(
            alert=alert
        )
        send_mail(
            f'{product.meta.title} alert',
            f'{product.meta.title} is under {threshold}',
            from_email=os.environ.get('EMAIL_HOST_USER'),
            recipient_list=["bensouiciakram@gmail.com"],
            fail_silently=False,   
        )