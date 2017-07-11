import os

from django.db import models
from s3direct.fields import S3DirectField

class Motive(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def is_technical(self):
        return (self.name=='Consulta Tecnica -> No me funciona algo.')

    def is_commercial(self):
        return (self.name=='Consulta Comercial -> Me cobraron menos.')

class Contact(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    image = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'), blank=True, null=True)
    motive = models.ForeignKey(Motive)

    def get_title(self):
        return self.title

    def get_description(self):
        return  self.description

    def __str__(self):
        return self.title

    def get_image_url(self):
        if not self.image:
            '''You need to add a default photo'''
            return ''
        return self.image

    def get_motive(self):
        return self.motive


