from __future__ import absolute_import
from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts.models import CodeValidator

admin.site.register(get_user_model())
admin.site.register(CodeValidator)


