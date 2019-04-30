
from stark.service.stark import site, ModelStark

from django.urls import reverse
from .models import *

from django.utils.safestring import mark_safe


class BookConfig(ModelStark):
    list_display = ['title','price']
    list_display_links = ['title']


site.register(Book, BookConfig)

site.register(Publish)
site.register(Author)
site.register(AuthorDetail)

