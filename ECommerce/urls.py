from django.urls import path

from .views import *

from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', homePage),
    path('', returnDashBoard, name='dashboard'),
    path('product/', returnProductsPage, name='product'),

    # now since this button will auto write an argument will be matched here
    # i specified this arg has to come with pk id i will give the button id as well
    path('customer/<str:pk_id>', customerPage, name='customer_'),
    # whenever the create order is clicked i will call the function that returns
    # the form page and , same function will have access to work and do some
    # process on it

    # and this 'create_order' i wanna a button to write in the url blank
    # whenever it's clicked ! and will call the fun that returns the form
    # if matches
    path('create_order/<str:pk_>', createOrder, name='creat_order'),

    # this page won't show up unless you pick up the specific instance u wanna search for or update or delete !
    path('update_order/<str:pk_>', updateOrder, name='update_order'),
    path('create_customer/', createCustomer, name='create_customer'),
    path('delete_product/<str:pk_>', deleteProductFromOrder, name='delete'),
    path('customer/update_customer/<str:pk_>', updateCustomer, name="update_customer"),
    path('signup/', signUpForm, name='signup'),
    path('login/', log_in_page, name='log_in'),
    path('logout/', logOutProcess, name='log_out'),

    # وكانك هنا تقول كيفية او طريقه استدعاء الداله لانه الداله هيا الي ترحع لك الصفحه
    # يعني لازم تلتزم بهاذا الاستدعا امتب لي فالرابط كذا وانا افههم وارجع لك الصفحه
    # غيرو انا مافهم
    path('user/', userPage, name='user-page'),
    path('setting/', viewSettingPage, name='setting'),



    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='email_form_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='was_sent_page.html'),
         name='password_reset_done'),
    path('reset/<uidb64><token>',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # path('//', other_page, name='other-groups')
]

# to reset a password we need a few steps :
# 1 => build a form to take the user email      // auth_views.PasswordResetView.as_view() this function builds a form and send u to sec step
# 2 => take tha email from the form and send a link to the email and shows page success sent 'important!' // auth_views.PasswordResetDoneView.as_view()=> email sent
# 3 => put a link in the user email to lead to another form with the user info ! secure // auth_views.PasswordResetConfirmView.as_view() leads to send a link
# 4 => building the reset pass form  that will show after clicking the link on the email //auth_views.PasswordResetCompleteView.as_view() go to db and change and done

# each step has a class individually that built in an api django gives us ! so Apis built in for us to deal with each step


# <str: what comes here must be the name
# of the parameter in function page
