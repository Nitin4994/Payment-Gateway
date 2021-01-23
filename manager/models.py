from django.db import models

# Create your models here.

#create manager model
class Manager(models.Model):
    fName = models.CharField('first_name',max_length=50)
    lName = models.CharField('last_name',max_length=50)
    email = models.EmailField('email',unique=True)
    password = models.CharField('password',max_length=500)
    address = models.CharField('address', max_length=350)
    dob = models.DateField('date_of_birth')
    company = models.CharField('company', max_length=50)

    @staticmethod
    def dummy_manager(): #create dummy manager model
        return Manager(id='',fName='',lName='',email='',password='',address='',dob='',company='')

    class Meta:
        db_table='Manager'
