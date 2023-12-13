from django.shortcuts import redirect
from tasks.filters import TASK_FILTERSETS_LIST
from categories.filters import CATEGORY_FILTERSETS_LIST
from .filters import TASKLIST_FILTERSETS_LIST

FILTERSETS_LIST = TASK_FILTERSETS_LIST + TASKLIST_FILTERSETS_LIST + CATEGORY_FILTERSETS_LIST
ALL_FILTERSETS_FIELD_NAMES = set()
for filterset in FILTERSETS_LIST:
    for field_name, lookup_exprs in filterset.get_fields().items():
        for lookup_expr in lookup_exprs:
            ALL_FILTERSETS_FIELD_NAMES.add(filterset.get_filter_name(field_name, lookup_expr))


class DjangoFiltersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if len(request.GET) == 0:
            return self.get_response(request)
        new_get = request.GET.copy()
        for k, v in request.GET.items():
            if k in ALL_FILTERSETS_FIELD_NAMES and not v:
                new_get.pop(k)
        if new_get == request.GET:
            return self.get_response(request)
        request.GET = new_get
        pure_path = request.META.get('PATH_INFO')
        new_path = f'{pure_path}?' + '&'.join(['%s=%s' % (k, v.replace(' ', '+')) for k, v in new_get.items()])
        if len(request.GET) == 0:
            new_path = new_path.split('?')[0]
        return redirect(new_path)

