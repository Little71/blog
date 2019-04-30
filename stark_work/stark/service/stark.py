# by luffycity.com
from django.conf.urls import url

from django.shortcuts import HttpResponse, render, reverse, redirect, get_object_or_404
from django.utils.safestring import mark_safe


class ModelStark(object):
    list_display = ['__str__']
    list_display_links = []
    modelformclass = None

    # ['checkbox','__str__','.....','编辑','删除']

    def __init__(self, model, site):
        self.model = model
        self.site = site

    def _get_url(self, obj, action):
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        _url = reverse(f"{app_name}_{model_name}_{action}", args=(obj.pk,))
        return _url

    def _get_url2(self, action):
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        _url = reverse(f"{app_name}_{model_name}_{action}")
        return _url

    def change(self, obj=None, header=False):
        if header:
            return "操作"
        url = self._get_url(obj, 'change')
        return mark_safe(f"<a href='{url}'>修改</a>")

    def delete(self, obj=None, header=False):
        if header:
            return "操作"
        url = self._get_url(obj, 'delete')
        return mark_safe(f"<a href='{url}'>删除</a>")

    def checkbox(self, obj=None, header=False):
        if header:
            return mark_safe("<input id='choice' type='checkbox'>")
        else:
            return mark_safe("<input class='choice_item' type='checkbox'>")

    def get_modelform(self):
        from django.forms import ModelForm
        class AddModelForm(ModelForm):
            class Meta:
                model = self.model
                fields = '__all__'

        if not self.modelformclass:
            self.modelformclass = AddModelForm
        return self.modelformclass

    def add_view(self, request):
        modelformclass = self.get_modelform()
        if request.method == "POST":
            form = modelformclass(request.POST)
            if form.is_valid():
                form.save()
                url = self._get_url2('list')
                return redirect(url)
            else:
                return render(request, 'add_view.html', locals())
        form = modelformclass()
        return render(request, 'add_view.html', locals())

    def delete_view(self, request, id):
        obj = get_object_or_404(self.model, pk=id)
        url = self._get_url2('list')
        if request.method == "POST":
            obj.delete()
            return redirect(url)
        return render(request, 'delete_view.html', locals())

    def change_view(self, request, id):
        modelformclass = self.get_modelform()
        obj = get_object_or_404(self.model, pk=id)
        if request.method == "POST":
            form = modelformclass(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                url = self._get_url2('list')
                return redirect(url)
            else:
                return render(request, 'change_view.html', locals())
        form = modelformclass(instance=obj)
        return render(request, 'change_view.html', locals())

    def get_header_list(self):
        temp = []
        temp.append(ModelStark.checkbox)
        temp.extend(self.list_display)
        if not self.list_display_links:
            temp.append(ModelStark.change)
        temp.append(ModelStark.delete)
        return temp

    def list_view(self, request):
        header_list = []
        add_url = self._get_url2("add")
        for field in self.get_header_list():
            if callable(field):
                valh = field(self, header=True)
                header_list.append(valh)
            elif field == "__str__":
                header_list.append(self.model._meta.model_name.upper())
            else:
                field = self.model._meta.get_field(field).verbose_name
                header_list.append(field)

        data_list = self.model.objects.all()
        new_list_data = []
        for obj in data_list:
            temp = []
            for field in self.get_header_list():
                if callable(field):
                    val = field(self, obj=obj)
                else:
                    if field in self.list_display_links:
                        change_url = self._get_url(obj, "change")
                        val = mark_safe(f'<a href="{change_url}">{getattr(obj, field)}</a>')
                    else:
                        val = getattr(obj, field)
                temp.append(val)
            new_list_data.append(temp)
        return render(request, 'list_view.html', locals())

    def get_url2(self):
        temp = []
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        temp.append(url(r"add/", self.add_view, name=f"{app_name}_{model_name}_add"))
        temp.append(url(r"(\d+)/delete/", self.delete_view, name=f"{app_name}_{model_name}_delete"))
        temp.append(url(r"(\d+)/change/", self.change_view, name=f"{app_name}_{model_name}_change"))
        temp.append(url(r"^$", self.list_view, name=f"{app_name}_{model_name}_list"))

        return temp

    @property
    def urls_2(self):
        return self.get_url2(), None, None


class StarkSite(object):
    def __init__(self):
        self._registry = {}

    def register(self, model, stark_class=None):
        if not stark_class:
            stark_class = ModelStark

        self._registry[model] = stark_class(model, self)

    def get_urls(self):
        '''
        app01/model_name/
        :return:
        '''
        temp = []
        for model, stark_class in self._registry.items():
            model_name = model._meta.model_name
            app_name = model._meta.app_label
            temp.append(url(f"{app_name}/{model_name}/", stark_class.urls_2))
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


site = StarkSite()
