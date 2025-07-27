from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render



#editors_decorator

def editors_decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not  request.user.role=='seller':
            return HttpResponseForbidden(render(request, '403.html'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

#delete-decorator
def delete_decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role=='customer':
            return HttpResponseForbidden(render(request, '403.html'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

#add_decorator
def add_decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.role=='seller':
            return HttpResponseForbidden(render(request, '403.html'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# details_decorator
def details_decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.role in ['customer', 'seller']:
            return HttpResponseForbidden(render(request, '403.html'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view