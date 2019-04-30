
from stark.service.stark import site, ModelStark

from django.urls import reverse
from .models import *

from django.utils.safestring import mark_safe


class BookConfig(ModelStark):
    list_display = ['title','price']
    list_display_links = ['title']

class PublishConfig(ModelStark):
    list_display = ['nid','name','city','email']
    list_display_links = ['name']

site.register(Book, BookConfig)

site.register(Publish,PublishConfig)
site.register(Author)
site.register(AuthorDetail)

