from django.core.paginator import Paginator


class Page:
    def __init__(self, page_num, data_list, params, max_page=11, per_page=10, url_prefix=None):
        '''

        :param page_num: 当前页
        :param data_list: 分页数据
        :param params: url参数列表
        :param max_page: 分页导航最大数量
        :param per_page: 每页数据条目
        :param url_prefix: url前缀
        '''
        self.url_prefix = url_prefix
        self.page_num = page_num
        self.data_list = data_list

        total_count = self.data_list.count()
        self.total_page, m = divmod(total_count, per_page)
        if m:
            self.total_page += 1
        if self.page_num:
            try:
                self.page_num = int(self.page_num)
                if self.page_num > self.total_page:
                    self.page_num = self.total_page
            except Exception as e:
                self.page_num = 1
        self.data_start = (self.page_num - 1) * per_page
        self.data_end = self.page_num * per_page

        if self.total_page < max_page:
            max_page = self.total_page

        half_max_page = max_page // 2
        self.page_start = self.page_num - half_max_page
        self.page_end = self.page_num + half_max_page

        if self.page_start <= 1:
            self.page_start = 1
            self.page_end = max_page

        if self.page_end >= self.total_page:
            self.page_end = self.total_page
            self.page_start = self.total_page - max_page + 1

        import copy
        self.params = copy.copy(params)

        '''request.GET.urlencode()  将字典序列化  即转成 key=value&key1=value1..'''

        print(self.params.urlencode())

    def get_data(self):
        return self.data_list[self.data_start:self.data_end]

    def get_html(self):
        html_list = []

        html_list.append(f"<li><a href='{self.url_prefix}?page=1'>首页</a></li>")

        if self.page_num == 1:
            html_list.append('''
                <li class="disabled">
                    <a href="#" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                </li>
                ''')
        else:
            html_list.append(f'''
                        <li>
                            <a href="{self.url_prefix}?page={self.page_num-1}" aria-label="Previous">
                                <span aria-hidden="true">&laquo;</span>
                            </a>
                        </li>
                        ''')

        for i in range(self.page_start, self.page_end + 1):
            self.params['page'] = i
            if i == self.page_num:
                tmp = f"<li class='active'><a href='{self.url_prefix}?{self.params.urlencode()}'>{i}</a></li>"
            else:
                tmp = f"<li><a href='{self.url_prefix}?{self.params.urlencode()}'>{i}</a></li>"
            html_list.append(tmp)

        if self.page_num == self.total_page:
            html_list.append('''
                <li class="disabled">
                    <a href="#" aria-label="Previous">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>
                ''')
        else:
            html_list.append(f'''
                        <li>
                            <a href="{self.url_prefix}?page={self.page_num+1}" aria-label="Previous">
                                <span aria-hidden="true">&raquo;</span>
                            </a>
                        </li>
                        ''')

        html_list.append(f"<li><a href='{self.url_prefix}?page={self.total_page}'>尾页</a></li>")

        html_page = ''.join(html_list)

        return html_page
