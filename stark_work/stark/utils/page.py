from django.core.paginator import Paginator


def pageing(page_num, data_list, list_url):
    if page_num:
        page_num = int(page_num)
    per_page = 10
    data_start = (page_num - 1) * per_page
    data_end = page_num * per_page

    total_count = data_list.count()
    total_page, m = divmod(total_count, per_page)
    if m:
        total_page += 1

    max_page = 11
    half_max_page = max_page // 2
    page_start = page_num - half_max_page
    page_end = page_num + half_max_page

    if page_start <= 1:
        page_start = 1
        page_end = max_page

    if page_end >= total_page:
        page_end = total_page
        page_start = total_page - max_page

    data_all = data_list[data_start:data_end]

    html_list = []
    for i in range(page_start, page_end + 1):
        html_list.append(f"<li><a href='{list_url}?page={i}'>{i}</a></li>")

    html_page = ''.join(html_list)
    nextpage_url = f"'{list_url}?page={int(page_num)+1}'"
    prevpage_url = f"'{list_url}?page={int(page_num)-1}'"

    return html_page, data_all, nextpage_url, prevpage_url
