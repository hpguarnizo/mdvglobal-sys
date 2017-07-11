import os
from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import SimpleLazyObject


def dashboard(request):
    user = request.user

    if not user.is_anonymous() and user.is_authenticated:

        return {
            'full_name': user.get_full_name(),
            'name' : user.get_first_name(),
            'photo': user.get_photo(),
            'plan': user.get_name_plan()
        }
    else :
        return {}


def site(request):
    site = SimpleLazyObject(lambda: get_current_site(request))
    protocol = 'https' if request.is_secure() else 'http'

    return {
        'site': site,
        'site_root': SimpleLazyObject(lambda: "{0}://{1}".format(protocol, site.domain)),
    }

def company(request):
    return {
        'company': os.environ.get("COMPANY","")
    }