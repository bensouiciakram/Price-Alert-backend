from django.db.models.signals import post_delete,pre_delete
from django.dispatch import receiver 
from .models import Product 
from alert.scheduler import scheduler 
from alert.models import Alert 


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