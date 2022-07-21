from django import template

register = template.Library()

@register.filter
def replace(request, page_num):
    query_args = request.GET.copy()
    query_args['page'] = page_num
    return query_args.urlencode()


@register.filter
def get_sort(request, sort):
    query_args = request.GET.copy()
    old_sort = query_args.get('sort')
    if old_sort and sort == old_sort:
        sort = f"-{sort}"
    query_args['sort'] = sort
    return query_args.urlencode()



@register.filter
def lower(value):
    return value.lower()
