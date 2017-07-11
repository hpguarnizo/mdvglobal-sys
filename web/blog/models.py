from django.db import models

# Create your models here.
class Subscriber(models.Model):
    #Suscripto
    email = models.CharField(max_length=60)
    confirmed = models.NullBooleanField(default=False)
    subscribe_email = models.NullBooleanField(default=True)

    def get_code(self):
        return abs(hash(self.email))

    def __str__(self):
        return self.email

    def activate_email(self):
        self.confirmed=True
        self.save()
        return self

    def get_email(self):
        return self.email

    def get_confirmed(self):
        return self.confirmed

    def get_subscribe_email(self):
        return self.subscribe_email

    def set_subscribe_email(self, boolean):
        self.subscribe_email = boolean

class CodeValidatorBlog(models.Model):
    code = models.CharField(max_length=40, primary_key=True)
    subscriber = models.ForeignKey(Subscriber)

    def get_code(self):
        return self.code

    def get_subscriber(self):
        return self.subscriber
