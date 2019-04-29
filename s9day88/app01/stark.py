from stark.service.stark import site, ModelStark

from django.urls import reverse
from .models import *

from django.utils.safestring import mark_safe


class UserConfig(ModelStark):

    list_display = ['pk', 'name', 'age']


site.register(UserInfo, UserConfig)
site.register(Book)

print("_registry ", site._registry)
