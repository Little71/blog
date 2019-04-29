# by luffycity.com
from audioop import reverse

from django.conf.urls import url
from django.shortcuts import render
from django.utils.safestring import mark_safe


class ModelStark(object):
    list_display = []

    def __init__(self, model, site):
        self.model = model
        self.site = site

    def edit(self, obj):

        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        url = reverse(f"{app_name}_{model_name}_change", args=(obj.pk,))
        return mark_safe(f"<a href='{url}'>编辑</a>")

    def deletes(self, obj):

        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        url = reverse(f"{app_name}_{model_name}_delete", args=(obj.pk,))
        return mark_safe(f"<a href='{url}'>删除</a>")

    def checkbox(self, obj):
        return mark_safe(f"<input type='checkbox'>")

    def add(self, request):
        pass

    def delete(self, request, id):
        pass

    def change(self, request, id):
        pass

    def new_list_display(self):
        temp = []
        temp.append(ModelStark.checkbox)
        temp.extend(self.list_display)
        temp.extend([ModelStark.edit, ModelStark.delete])
        return temp

    def list_view(self, request):
        data_list = self.model.objects.all()
        new_data_list = ['__str__']
        for obj in data_list:
            temp = []
            for field in self.new_list_display():
                if callable(field):
                    varl = field(self, obj)
                else:
                    varl = getattr(obj, field)
                temp.append(varl)
            new_data_list.append(temp)
        context = {'new_data_list': new_data_list}
        return render(request, 'list_view.html', context=context)

    def get_urls(self):
        temp = []
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        temp.append(url(r'^add/', self.add, name=f'{app_name}_{model_name}_add'))
        temp.append(url(r'^(\d+)/delete/', self.delete, name=f'{app_name}_{model_name}_delete'))
        temp.append(url(r'^(\d+)/change/', self.change, name=f'{app_name}_{model_name}_change'))
        temp.append(url(r'^$', self.list_view, name=f'{app_name}_{model_name}_list'))
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


class StarkSite(object):
    def __init__(self, name="site"):
        self._registry = {}
        self.name = name

    def register(self, model, stark_class=None):
        if not stark_class:
            stark_class = ModelStark

        self._registry[model] = stark_class(model, self)

    def get_urls(self):
        temp = []
        for model, stark_class_obj in self._registry.items():
            temp.append(url(f"^{model._meta.app_label}/{model._meta.model_name}/", stark_class_obj.urls))
        return temp

    @property
    def urls(self):
        return self.get_urls(), 'site', self.name


site = StarkSite()
