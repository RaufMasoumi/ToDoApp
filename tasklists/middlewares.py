from django.shortcuts import redirect
from .filters import ALL_FILTERSETS_FIELD_NAMES


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

