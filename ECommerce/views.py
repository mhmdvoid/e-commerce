from django.shortcuts import render, redirect
from django.forms import inlineformset_factory, formsets

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm

from .decorators import *
from django.contrib.auth.models import Group
from ECommerce.models import *

from .forms import *
from .filters import OrderFilter, CustomerFilter
# since i wanna show things in the dashboard from the DB so i have to ge to the function
# that returns the dashboard page and set my queries on it

# to view this page you have to log in/ so log in is required
# so this function will make this page won't show up unless you log in



# @allowed_objects(allowed_user=['admin'])
@login_required(login_url="log_in")
@is_admin
# @allowed_objects(allowed_user=['admin'])
def returnDashBoard(request):



    customers = Customer.objects.all()

    form_for_filter = CustomerFilter(request.GET, queryset=customers)



    # basically this line of code will return only one value so it's {{expression}}
    # not code {% %}
    # select * from Order table now
    orders = Order.objects.all()
    all_customer = Customer.objects.all()
    total_orders = orders.count()
    # select * from where padding then count
    padding_orders = orders.filter(status_field='Padding').count()
    shipped_orders = orders.filter(status_field='Shipped').count()
    # json_format = {'all_order': total_orders}
    return render(request, 'DashBoard.html', {'total_order': total_orders,
                                              'padding': padding_orders,
                                              'shipped': shipped_orders,
                                              'customers': all_customer,
                                              'orders': orders,
                                              'search_cus': form_for_filter})

@login_required(login_url='log_in')  # so this function will make this page won't show up unless you log in
# @allowed_object(allowed_user=['admin'])
@allowed_objects(allowed_user=['admin'])
def returnProductsPage(request):
    all_product = Product.objects.all()
    # an_instance = all_product.filter(item_name='Foo')
    # tags = Tag.objects.filter(product=an_instance.id)


    return render(request, 'Product.html', {"products": all_product})
def homePage(request):
    return render(request, 'Main.html')


# one template multiple users dynamically

@login_required(login_url='log_in')
@allowed_objects(allowed_user=['admin'])# so this function will make this page won't show up unless you log in
def customerPage(request, pk_id):


    # get() returns one pk object
    # it doesn't return more than one objects
    # which's needed !

    # the page will be filled with data of the object requested by the user

    customer_by_user_request = Customer.objects.get(pk=pk_id)
    orders_of_customer = customer_by_user_request.order_set.all()

    # get here is the to take the value from the حقل
    # this line means select * from Order where request.حقل = request.GET
    # but we have to link it to the query above there

    # FilterSet alone has the ability to do where الحقل المختار = the value got
    # الفكره لازم نقوله سوي البحث على كل الانستانيس ! لذلك نمرر له كويري select * from model
    form_for_filter = OrderFilter(request.GET, queryset=orders_of_customer)

    # changing the query of all to the return filter found
    orders_of_customer = form_for_filter.qs
    json_format = {
        'customer_requested': orders_of_customer,
        'customer_info': customer_by_user_request,
        'form': form_for_filter
    }

    return render(request, 'Customer.html', json_format)


# @allowed_object(allowed_user=['admin'])# so this function will make this page won't show up unless you log in
@login_required(login_url='log_in')
# @who_is_using_it_required
def createOrder(request, pk_):

    # this page will be basically changed because this is not what it should be !

    # ليه عشان الاوردر ماينضاف الا هذا الشخص اساسا يوزر فهمت


    # here we wanna get into the private page of the specific object/instance
    # then we will create an order/ add it ot the parent same object
    # that has the page private profile obviously !!!

    # doing that will let us able to bring the object that has the specific
    # page private
    #
    from_customer_page_we_know = Customer.objects.get(id=pk_)
    # form = OrderForm(initial={'customer': from_customer_page_we_know})
    # here it is in from type widget that holds some input field and it will be sent to HTML using context dynamically

    # now there is a method that will let our parent add a lot of its child
    # fg which is gonna be effective

    # to create a lot forms, alright ?
    new_form = inlineformset_factory(Customer, Order, fields=('product', 'status_field'), extra=10)

    # to specify these bunch of orders all belong one Object !
    # and also to fetch all multiple Orders for the private object
    # we have to let the form a bit about the private object
    # and order thing on thar matter
    form = new_form(queryset=Order.objects.none(), instance=from_customer_page_we_know)
    if request.method == 'POST':
        form = new_form(request.POST, instance=from_customer_page_we_know)  # here if the method is POST which is True, write a new instance in the form that sent after taking the whole data from
        if form.is_valid():  # it returns either True or False
            form.save()
            # if request.user.
            return redirect('dashboard')
    # always key will be sent to HTML
    context = {'form': form}
    return render(request, 'order_form.html', context)


# this concept called return same page , with different URL as well as different Data based on a chosen an instance
@login_required(login_url='log_in')
# @allowed_object(allowed_user=['admin'])# so this function will make this page won't show up unless you log in
def updateOrder(request, pk_):

    # bring the order that's id will be sent with url dynamic and compare the condition and only return one instance !
    specific_order_user_picked = Order.objects.get(id=pk_)
    # here we say this OrderForm taking the type of form right now so i wanna it to go to html with different widget basically, to go to the object 'model' of the
    # instance sent and look for the row that represent that instance and take its columns and send widgets corresponding to the columns number of that one row
    # returns thank of get method (id=pk)
    form = OrderForm(instance=specific_order_user_picked)  # to change the shape of the widget
    context = {'form': form}
    # it means if data is sent using the post method which is gonna be for sure
    if request.method == 'POST':
        # اساسا هذي بوست تكتب لكن ذي المره ابغاها تكتب على بيانات الانستانس الي اليوزر تحديدا يبغا يغير بياناتو وليس كل او خلق صف جديد
        form = OrderForm(request.POST, instance=specific_order_user_picked)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request, 'order_form.html', context)
#
# def customerUpdateOrder(request, pk):
#     specific_order_user_picked = Order.objects.get(id=pk)
#

@login_required(login_url='log_in')
# @allowed_object(allowed_user=['admin'])# so this function will make this page won't show up unless you log in
def createCustomer(request):
    # so when we do new instance = new object , we create simply a new instance => a new row in the object table selected !no need of getting a specific row
    # or instance

    form_sent_html = CustomerForm()
    context = {
        'form': form_sent_html,
    }
    # since i am writing something and inserting to the DB, so we will use the method POST
    if request.method == "POST":
        form = CustomerForm(request.POST)  # this POST returns the value that're in the widget inserted by each new user !
        if form.is_valid():
            form.save()

            # after saving the data, the new instance created will be sent to DB so objects.last() would return the latest instance has been created
            # then i will reach to its id and use it ! important 'after saving of course'
            latest_customer_added = Customer.objects.last()
            return redirect("customer_", latest_customer_added.id)
    return render(request, 'customers_form.html', context)

@login_required(login_url='log_in')
# @allowed_object(allowed_user=['admin'])
def deleteProductFromOrder(request, pk_):
    # now when updating or deleting we're already getting the id of the object
    # looking for to search or delete so it is better to store and save in the
    # same function that returns the instance_id by it we could use get(id=pk_)!
    order_wanna_removed = Order.objects.get(id=pk_)
    if request.method == "POST":
        order_wanna_removed.delete()
        return redirect('dashboard')

    return render(request, 'delete_product.html', {
        'item': order_wanna_removed
    }
                  )



@login_required(login_url='log_in')
@allowed_objects(allowed_user=['admin'])
def updateCustomer(request, pk_):

    customer_chosen_to_update = Customer.objects.get(id=pk_)
    # html widget and type of form that will go the front-end
    form = CustomerForm(instance=customer_chosen_to_update)  # it means goes to the instance table and get its cells and draw some html input based on the
    # columns that instance has

    context = {
        'form': form
    }
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer_chosen_to_update)
        form.save()
        return redirect('customer_', customer_chosen_to_update.id)

    # here we get our pk_ form user dynamically, now we will hold the instance by the pk and get() method
    return render(request, 'customers_form.html', context)
@mustLoggedOut
def signUpForm(request):

    # here as well if the user request is working and still accepted it means it has used the page of logged in and
    # the request logged in they're in the dashboard why would they see signup page !
    #
    # if request.user.is_authenticated:
    #     return redirect('dashboard')


    # front-end part and drawing the form built in

    # also this form deals with User model so we can actually
    # override to get some other fields as we like
    form = SignUpForm()
    # extend_form = CustomerForm(e)

    # group_customer = Group.objects.get(name='customer')
    # now backENd
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # if it is not valid we deal with that in html field let's go ahead and see

            # so basically form.save is the whole data is written in the form, which is the instance that after saving goes as row in the
            # user table, لذلك بعد حفظ البيانات اصبحت صف كامل يمثل انستانس then instance_jus_added_to_table.groups.add() add a group to that new
            # instance
            form.save()
            # extend_data = request.POST.

            # user_data.groups.add(group_customer)
            # Customer.objects.create(
            #     # user=user_data,
            #     first_name=request.POST.get('username'),
            #     email=request.POST.get('email'),
                # address=extend_data,

            # )
            # here i am gonna use flash messages if the form is valid and send its data properly
            messages.success(request, 'Account was successfully created ' + request.POST.get('username'))
            return redirect('log_in')
        # else:
        #     error_mess = form.error_messages.get('password_mismatch')

    context = {
        'form': form,
        # 'error_': error_mess
    }
    return render(request, 'SingUp.html', context)


# to view this page which's log in page u have to be log out, otherwise ur
# of course authenticated and logged in why would u go there !
@mustLoggedOut
def log_in_page(request):
    # هذا اللوجيك كلو مسوول عن اضافه التحقق وتسحيل الدخول وكلو !
    # getting the value within input widget
    # لو اليوزر مسجل دخوله امنعه من الوصول لهذا الصفحه عن طريق ارجاعه الى الصفحه الريسيه
    # if request.user.is_authenticated:
    #     return redirect('dashboard')

    # there is an attribute that returns True if the request is logged in
    # since we said that, each object log in has got their own private request going on with them so we know by their request
    # if they log in or no
    # here it becomes so obvious each user has got request that let them special and let us know what they are doing
    # in our page in terms of processing or logging terms
    # if request.user.is_authenticated:
    #     # if they are logged in why would they access this page this what exactly it means !
    #     return redirect('dashboard')

    # else:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    # now we have the value will be input by the user, now we will send them to the fun down to do the process taking the
    # request and username and password, those are columns in the model and then check their value and returns None if
    # mot matched or not found or not correct
        user_data = authenticate(request, username=username, password=password)
        # this will check if true then an object/row will be created we would love to have that row
        # which is just the new object added to our DB user and save in a variable

        # means if user data is a row so it's data has been taken  and accepted now log it in (req, user)
        if user_data is not None:
            # there is a fun responsible of logging the data in once it's authenticated then redirect to wherever you want
            login(request, user_data)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'log_in.html')


def logOutProcess(request):
    # now i understand why every fun takes a request, cuz it's yours i mean this fun represents a process and your request
    # will distinguish that this objects that holds that request المميز will do this process

    # it is preferable to use current.user.customer cuz that's better or u could use the user real object
    # actually it does not matter, cuz a user becomes a customer and a customer is a user so no difference
    # at all either u use .user or .user.customer, request handel that for us !
    current_user = request.user
    # now we wanna really log out that person who holds that request
    logout(request)

    context = {
        'current_user': current_user
    }

    # حتى الي يودي لنفس الصفحه اذا الفانكشن تسوي عمليه لازم لها لينك مختلف انتبه !
    # اصلا لازم يكون فيه عمليه معينه اجل ليه رايح لنفس الصفحه الي فيه داله اخرى تودي لها!، اكيد ماسويت داله تانيه الا تبا تروح لنفس الصفحه بس بفعل مختلف دي المره !
    # لذلك على طول فكر في رابط تاني يوديك لنفس التمبلت لكن الداله المختلفه

    #  it means once this function logout gets called it will do its process and then
    # type the log_in url in the url blank and all know if the matching syntax True will always call another page that's why

    return render(request, 'log_out_page.html', context)
    # return redirect('log_in')

# they are just conditions nothing else
@login_required(login_url='log_in')
@allowed_objects(allowed_user=['customer'])
def userPage(request):

    # request.user.customer.id

    owner_page = request.user.customer



    owner_order = request.user.customer.order_set.all()

    total_orders = owner_order.count()
    # select * from where padding then count
    padding_orders = owner_order.filter(status_field='Padding').count()
    shipped_orders = owner_order.filter(status_field='Shipped').count()
    context = {
        'owner': owner_page,
        'owner_orders': owner_order,
        'total_order': total_orders,
        'shipped': shipped_orders,
        'padding': padding_orders

    }

    # if request.method.
    return render(request, 'user_page.html', context)

#
# def other_page(request):
#     return render(request, 'other.html')

#



@login_required(login_url='log_in')
@allowed_objects(allowed_user=['customer'])
def viewSettingPage(request):

    customer_current = request.user.customer

    # front-end and to show that form with initial data
    form = CustomerForm(instance=customer_current)

    # it means the user wanna write data we have to take them
    # what comes after the if is back end ModelForm job
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer_current)
        if form.is_valid():
            form.save()
            # return redirect('user-page')


    context = {
        'form': form,
        'the_user': customer_current
    }
    return render(request, 'user_setting.html', context)

