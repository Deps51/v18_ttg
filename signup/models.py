from django.db import models
#from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class MytypeField(models.Field):
    def db_type(self, connection):
        return 'mytype'

class Product(models.Model):
    website = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    brand = models.CharField(max_length=1000)
    price = models.CharField(max_length=1000)
    img = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    web_id = models.CharField(max_length=1000)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #index = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    def getBasket(self):
        basket_list = [self.website, self.name, self.brand, self.price, self.img, self.link]
        return basket_list



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    #basket = {'list':['1']}
    productm2m = models.ManyToManyField(Product)


    def getBasket(self):
        pass


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()