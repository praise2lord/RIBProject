
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
# from django.template.loader import render_to_string


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('error401')
        return wrapper_func
    return decorator
           

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.groups.filter(name='RIBHeadquarter')==True:
            return redirect('home_Hq')
        elif request.user.groups.filter(name='RIBStation')==True:
            return redirect('home_Station')
        elif request.user.groups.filter(name='StationUser')==True:
            return redirect('home_Officer')
        elif request.user.groups.filter(name='Admin')==True:
            return redirect('home')      
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
