from django.http import HttpResponse
from django.shortcuts import redirect, render


# when i say decorator i mean a sent func as arg will be called
# of course and run but we wanna do some functionality and conditions
# before that TargetFunction called so we could say simply
# that function will get called but the conditions are required to call

def mustLoggedOut(view_page):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
        #     # this is simply the calling !
            return view_page(request, *args, **kwargs)

    return wrapper


#  now we wanna add some permission and we wanna apply each permission on a specific page to understand that completely


# this will be for every page except dashboard it will be for pages will be viewed based on the user
# group
def allowed_objects(allowed_user=[]):
    def decorator(view_):
        def wrapper(request, *args, **kwargs):

            allowed_group = None

            if request.user.groups.exists():
                allowed_group = request.user.groups.all()[0].name

            #
            # if allowed_group == 'customer':
            #     return view_(request, *args, **kwargs)


            if allowed_group in allowed_user:
                # now problem view that dashboard

                # we mean by view here is the function that will get called below the decorator place
                return view_(request, *args, **kwargs)
            else:
                return HttpResponse('Not Allowed')
        return wrapper
    return decorator



# only for dashboard
def is_admin(view_function):
    def wrapper(req, *args, **kwargs):

        group = None

        if req.user.groups.exists():
            group = req.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')
        if group == 'admin':
            return view_function(req, *args, **kwargs)
    return wrapper

#
# def who_is_using_it_required(view_function):
#     def wrapper(request, *args, **kwargs):
#     return wrapper