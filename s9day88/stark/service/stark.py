# by luffycity.com
from django.conf.urls import url

from django.shortcuts import HttpResponse, render


class ModelStark(object):

    def __init__(self, model, site):
        self.model = model
        self.site = site


class StarkSite(object):
    def __init__(self):
        self._registry = {}

    def register(self, model, stark_class=None):
        if not stark_class:
            stark_class = ModelStark

        self._registry[model] = stark_class(model, self)

site = StarkSite()
