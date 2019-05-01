# by luffycity.com
import copy

from django.conf.urls import url
from django.shortcuts import HttpResponse, render, reverse, redirect, get_object_or_404
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields.related import ForeignKey

from stark.utils.page import Page


class ShowList:

    def __init__(self, config, data_list, request):
        self.config = config
        self.data_list = data_list
        data_count = self.data_list.count()
        self.request = request
        current_page = int(self.request.GET.get('page', 1))
        base_path = self.request.path
        self.page = Page(current_page, data_count, self.request.GET, base_path)
        self.data = self.data_list[self.page.start:self.page.end]
        self.actions = self.config.new_actions()

    def get_filter_linktags(self):
        link_dic = {}
        for filter_field in self.config.list_filter:
            params = copy.deepcopy(self.request.GET)
            filter_field_obj = self.config.model._meta.get_field(filter_field)

            if isinstance(filter_field_obj,(ForeignKey,ManyToManyField)):
                data_list = filter_field_obj.rel.to.objects.all()
            else:
                data_list = self.config.model.objects.all().values('pk',filter_field)
            temp = []

            if params.get(filter_field):
                del params[filter_field]
                temp.append(f"<a href='?{params.urlencode()}'>all</a>")
            else:
                temp.append(f"<a class='active' href='#'>all</a>")

            for obj in data_list:
                if isinstance(filter_field_obj, (ForeignKey, ManyToManyField)):
                    pk = obj.pk
                    text = str(obj)
                    params[filter_field] = pk
                else:
                    pk = obj.get('pk')
                    text = obj.get(filter_field)
                    params[filter_field] = text

                if str(pk) in params.values():
                    link_tag = f"<a class='active' href='?{url}'>{text}</a>"
                else:
                    link_tag = f"<a href=?{url}>{text}</a>"

                url = params.urlencode()
                temp.append(mark_safe(link_tag))
            link_dic[filter_field] = temp
        print('link_dic', link_dic)
        return link_dic

    def get_action_list(self):
        temp = []
        for action in self.actions:
            temp.append({
                'name': action.__name__,
                'desc': action.short_description if hasattr(action, 'short_description') else action.__name__
            })
        return temp

    def get_header(self):
        # 构建表头
        header_list = []
        for field in self.config.get_header_list():
            if callable(field):
                valh = field(self.config, header=True)
                header_list.append(valh)
            elif field == "__str__":
                header_list.append(self.config.model._meta.model_name.upper())
            else:
                field = self.config.model._meta.get_field(field).verbose_name
                header_list.append(field)
        return header_list

    def get_body(self):
        # 构建表单
        new_list_data = []
        for obj in self.data:
            temp = []
            for field in self.config.get_header_list():
                if callable(field):
                    val = field(self.config, obj=obj)
                else:
                    val = getattr(obj, field)
                    filter_obj = self.config.model._meta.get_field(field)
                    if isinstance(filter_obj, ManyToManyField):
                        t = []
                        for i in  val.all():
                            t.append(str(obj))
                        val = ','.join(t)

                    if field in self.config.list_display_links:
                        change_url = self.config._get_url(obj, "change")
                        val = mark_safe(f'<a href="{change_url}">{val}</a>')
                temp.append(val)
            new_list_data.append(temp)
        return new_list_data


class ModelStark:
    list_display = ['__str__']
    list_display_links = []
    modelformclass = None
    search_filter = []
    actions = []
    list_filter = []

    def __init__(self, model, site):
        self.model = model
        self.site = site

    def patch_delete(self, request, queryset):
        queryset.delete()

    patch_delete.short_description = "批量删除"

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
            return mark_safe(f"<input class='choice_item' type='checkbox' name='selected_pk' value={obj.pk}>")

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

    def new_actions(self):
        temp = []
        temp.append(ModelStark.patch_delete)
        temp.extend(self.actions)
        return temp

    def get_search_condition(self, request):
        key_world = request.GET.get('q', "")
        self.key_world = key_world
        search_connetion = Q()
        if key_world:
            for field in self.search_filter:
                search_connetion.children.append((field + '__contains', key_world))
        return search_connetion

    def get_filter_condition(self, request):
        filter_condition = Q()
        for filter_field, val in request.GET.items():
            # if hasattr(self.model,filter_field):
            if filter_field in self.list_filter:
                filter_condition.children.append((filter_field, val))
        return filter_condition

    def list_view(self, request):
        if request.method == "POST":
            action = request.POST.get('action')
            selected_pk = request.POST.getlist('selected_pk')
            action_func = getattr(self, action)
            queryset = self.model.objects.filter(pk__in=selected_pk)
            action_func(request, queryset)

        # 获取search得q对象
        search_connetion = self.get_search_condition(request)

        # 构建filter对象
        filter_condition = self.get_filter_condition(request)

        # 筛选后得数据
        data_list = self.model.objects.all().filter(search_connetion).filter(filter_condition)
        show_list = ShowList(self, data_list, request)

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
