from django.db import models

# Create your models here.

from manager.models import Manager

#create subscriptions model
class Subscription(models.Model):
    plan = models.CharField('plan',max_length=50)
    date = models.DateField('date')
    price = models.IntegerField('price')
    expire = models.CharField('expire_plan', max_length=50, default='No')
    expireDate = models.DateField('expire_date',null=True)
    transactionId = models.CharField('transaction_id',max_length=100,null=True)
    active = models.CharField('active', max_length=50, default='Yes')
    mangerref = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='subref', null=True)

    @staticmethod
    def dummy_subscription():   #create dummy_subscriptions
        return Subscription(id='',plan='',date='',price='',expire='',expireDate='',transactionId='',active='',mangerref='')

    class Meta:
        db_table='Subscription'
