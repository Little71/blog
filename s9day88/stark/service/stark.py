# by luffycity.com
from audioop import reverse

from django.conf.urls import url
from django.shortcuts import render
from django.utils.safestring import mark_safe


class ModelStark(object):
    list_display = []
    list_display_links = []

    def __init__(self, model, site):
        self.model = model
        self.site = site

    def edit(self, obj=None, header=False):
        if header:
            return "修改"

        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        url = reverse(f"{app_name}_{model_name}_change", args=(obj.pk,))
        return mark_safe(f"<a href='{url}'>编辑</a>")

    def deletes(self, obj=None, header=False):
        if header:
            return "删除"

        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        url = reverse(f"{app_name}_{model_name}_delete", args=(obj.pk,))
        return mark_safe(f"<a href='{url}'>删除</a>")

    def checkbox(self, obj=None, header=False):
        if header:
            return mark_safe(f"<input id='choice' type='checkbox'>")
        return mark_safe(f"<input class='choice_item' type='checkbox'>")

    def add_view(self, request):
        return render(request,"add_view.html")

    def delete_view(self, request, id):
        pass

    def change_view(self, request, id):
        pass

    def new_list_display(self):
        temp = []
        temp.append(ModelStark.checkbox)
        temp.extend(self.list_display)
        if not self.list_display_links:
            temp.extend(ModelStark.edit)
        temp.extend(ModelStark.delete_view)
        return temp

    def get_header(self):
        header_list = []
        for field in self.new_list_display():
            if callable(field):
                val = field(self, header=True)
                header_list.append(val)
            elif field == "__str__":
                header_list.append(self.model._meta.model_name.upper())
            else:
                # header_list.append(field)
                var = self.model.get_field(field).verbose_name
                header_list.append(var)

        return header_list

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
                    if field in self.list_display_links:
                        model_name = self.model._meta.model_name
                        app_name = self.model._meta.app_label
                        url = reverse(f"{app_name}_{model_name}_change", args=(obj.pk,))
                        varl = mark_safe(f'<a href=“{url}”>{varl}</a>')
                temp.append(varl)
            new_data_list.append(temp)

        add_url = self.get_add_url()

        context = {'new_data_list': new_data_list, 'header_list': self.get_header,"add_url":add_url}
        return render(request, 'list_view.html', context=context)

    def get_change_url(self, obj):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        _url = reverse("%s_%s_change" % (app_label, model_name), args=(obj.pk,))

        return _url

    def get_delete_url(self, obj):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse("%s_%s_delete" % (app_label, model_name), args=(obj.pk,))

        return _url

    def get_add_url(self):

        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse("%s_%s_add" % (app_label, model_name))

        return _url

    def get_list_url(self):

        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse("%s_%s_list" % (app_label, model_name))

        return _url

    def get_urls(self):
        temp = []
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        temp.append(url(r'^add/', self.add_view, name=f'{app_name}_{model_name}_add'))
        temp.append(url(r'^(\d+)/delete/', self.delete_view, name=f'{app_name}_{model_name}_delete'))
        temp.append(url(r'^(\d+)/change/', self.change_view, name=f'{app_name}_{model_name}_change'))
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
