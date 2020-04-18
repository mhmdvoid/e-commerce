import django_filters as f
from django_filters import DateFilter
from .models import *
class OrderFilter(f.FilterSet):
    order_date = DateFilter(field_name='order_date', lookup_expr='gte')
    end_date = DateFilter(field_name='order_date', lookup_expr='lte')

    class Meta:
        # the model that i wanna you to see it visible and filter through it

        model = Order
        fields = '__all__'
        exclude = ['customer', 'order_date']


class CustomerFilter(f.FilterSet):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'pic_profile']