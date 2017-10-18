from __future__ import absolute_import

from cities_light.models import Region
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
import binascii
import os
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from s3direct.fields import S3DirectField
from home.emails import email_welcome
from pay.models import Customer, Gratis


def _generate_code():
    return binascii.hexlify(os.urandom(20))


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()

        if not username:
            raise ValueError(_('El email es necesario'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if email!=None and  len(email)>3 and user.verify_email:
            email_welcome(user)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        #Verify exist email
        email = self.normalize_email(email)
        if email!=None:
            user = MyUser.objects.filter(email=email)
            if len(user)==1:
                return user[0]

        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    username = models.CharField(_('username'), max_length=255, unique=True,
                                help_text=_(
                                    'Required. 255 characters or fewer.'),
                                )
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'), max_length=255)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    receive_newsletter = models.BooleanField(_('receive newsletter'), default=False)
    photo = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'), blank=True,null=True)
    verify_email = models.NullBooleanField(default=True,blank=True,null=True)
    customer = models.OneToOneField(Customer,blank=True,null=True)
    subscribe_email = models.NullBooleanField(default=True,blank=True,null=True)
    provincia = models.ForeignKey(Region, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_provincia(self):
        return self.provincia

    def get_receive_newsletter(self):
        return self.receive_newsletter

    def get_date_joined(self):
        return self.date_joined

    def set_provincia(self,provincia):
        self.provincia=provincia

    def get_date_joined(self):
        return self.date_joined

    def set_customer(self):
        return self.customer

    def get_is_active(self):
        return self.is_active

    def get_full_name(self):
        full_name = '%s %s' % (self.get_first_name(), self.get_last_name())
        return full_name.strip()

    def get_short_name(self):
        return self.first_name if self.first_name != None else ""

    def get_photo(self):
        return self.photo

    def photo_url(self):
        if not self.photo:
            '''You need to add a default photo'''
            return '/static/common/img/default_photo.png'
        return self.photo

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email],fail_silently=False)

    def get_first_name(self):
        return self.first_name if self.first_name != None else ""

    def get_last_name(self):
        return self.last_name if self.last_name != None else ""

    def set_is_active(self,is_active):
        self.is_active = is_active

    def get_name_plan(self):
        if self.get_plan() == None or self.get_plan().is_free():
            return "Cuenta Gratuita"
        else:
            return "Cuenta Premium"

    def get_plan(self):
        return (self.get_customer().get_plan() if self.get_customer() != None  else Gratis.objects.all().first())


    def get_email(self):
        return self.email

    def get_customer(self):
        return self.customer

    def set_customer(self,customer):
        self.customer = customer

    def activate_email(self):
        self.verify_email = True
        self.is_active = True
        self.save(force_update=True,update_fields=['verify_email','is_active'])
        return self

    def set_plan_free(self):
        self.set_customer(None)

    def set_customer(self, customer):
        self.customer = customer


    def set_subscribe_email(self,subscribe_email):
        self.subscribe_email = subscribe_email

    def _get_pk_val(self, meta=None):
        if not meta:
            meta = self._meta
        try:
            return getattr(self, meta.pk.attname)
        except AttributeError:
            return None

    def set_datos(self,first_name,last_name,photo):
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo

    def set_email(self,email):
        if email:
            self.email = email

    def set_verify_email(self,verify_email):
        self.verify_email = verify_email

class CodeValidator(models.Model):
    code = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(MyUser)
