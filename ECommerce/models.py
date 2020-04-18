from django.db import models

from django.contrib.auth.models import User
class Address(models.Model):
    country = models.CharField(max_length=100)
#     here Python allows us to do OOP concept really like java which makes that so
#     powerful for Django !
#     each class معناتو راح تشرح للكمبيوتر ايش هوا هذا الاوبكجيكت بعيدا عن انه راح يصبح جدول اشرح كانك تشرح في جافل
#     الكلاسات
    city = models.CharField(max_length=100)

    zip = models.IntegerField()
    neighborhood = models.CharField(max_length=200)

    def __str__(self):
        return self.country + ' ' + self.city + ' ' + self.neighborhood


class Customer(models.Model):

    # we will extend the User model why, cuz teh User has got the ability to deal with Django and do a lot of work for us
    # in terms of the authentication and permission but there are a lot of columns and relation not exist in Use
    # so we extend it by adding the required columns and then link them to user so user will be having these columns all
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    pic_profile = models.ImageField(null=True, blank=True, default="user.png")
    email = models.EmailField(max_length=200)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class Tag(models.Model):
    tag_section_name = models.CharField(max_length=40)

    def __str__(self):
        return self.tag_section_name


class Product(models.Model):
    item_name = models.CharField(max_length=40)
    quantity = models.IntegerField()
    item_price = models.FloatField()
    categories = (
        ('In Door', 'In Door'),
        ('Out Door', 'Out Door')
    )
    category = models.CharField(max_length=40,null=True, choices=categories)
    # once a product created give in which a tag it exists !
    # it could be in more than one tag so, we need a list of multiple generated
    section_tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.item_name

class Order(models.Model):

    CAT = (
        ('Shipped', 'Shipped'),
        ('Not Shipped', 'Not Shipped'),
        ('Padding', 'Padding'),
    )
    order_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    # so creating a drop-down list will be by doing so = ((userDB, front-end), and so on)
    # then char1 = Char(length=n, null=True
    status_field = models.CharField(max_length=30, null=True, choices=CAT)

    def __str__(self):
        return self.product.item_name