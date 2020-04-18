from django.forms import ModelForm
from .models import *
# just to call the ModelForm class
# and calling all models/objects
# that will have forms


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# creating form that will hold order fields
class OrderForm(ModelForm):
    class Meta:
        # this is overriding to let django convert this entity as form widgets based on the
        # fields and give myClass work with all Form and DB لوازم
        model = Order
        fields = '__all__'
        exclude = ['customer']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ['user']



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'last_name']

