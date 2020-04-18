from django.db.models.signals import post_save
from .models import *
from django.contrib.auth.models import User, Group

# Group is a models ! and as it is a model has got objects.get(name_of_the group = '')
# returns one and only one group, cuz Group is a model contains a lot of groups objects we can get to one
# group between all the groups that this model has !

from django.dispatch import receiver





# here sender means, السوسه الذي يمتلك كل البيانات التي نحن مهتمين فيها ونبغا يترسل لنا كلشي جديد عنها ونبقى على اطلاع بحيث User is a model لديه بيانات جديده تجي وبيانات تتحدث على جدوله
# واكيد اقدر اخلي اي اوبجيكت يصير observer بحيث يشترك ويستمع اليه بحيث اي انستانس يتخلق جديد في Subject التي لديه كل البيانات المطلع عليها يتم على طول ارسالها للمشتركين الذين turned on notification
# بحيث من حق المستمعين ان يصل لهم اي شي يصير في بيانات the sender

# طبعا يتم اختيار السبجيكت بحيث تعرف انه اي انستانس او داتا تخش عليه راح توصل الي الجدول ويتم عمل نيو انستانس على طول الجدول الي هوا observer
# => sender = '' تعني هنا هذا الموديل هوا المهتمين فيه بحيث اول ماتدخل عليه بيانات جديده وهيا علي شكل انستانس تكون ارسلي الانستانس كما هوا وابقيني على اطلاع
@receiver(post_save, sender=User)
def sendMeEverything(sender, instance, created, **kwargs):

    # created returns True if the subject gets a new data and of course new data means will be stored in form of instance/row so it can be sent to the subscribers
    # table as row that corresponding to the row created in the subject/server and one of the subscribers' right is that they get it at once created to their table
    if created:
        # just to add everybody gets our web to the customer page cuz they're of course not admin but customer
        specific_group = Group.objects.get(name='customer')
        instance.groups.add(specific_group)
        Customer.objects.create(user=instance,
                                first_name=instance.username,
                                email=instance.email,
                                last_name=instance.last_name)

    # here comes the subscribers those who will listen and get updated and new instances sent to their table whenever the sender get new data to their table
    # and the data stored in form instance to be sent to the subscribers at once a sender has them



# now after holding the data and send them to the subscribers now there might be some changes to the current
# data and instances that are stored in the subject, so to be good we have to ننادي حلقات الوصل من المشتركين ونرسل لهم
# البيانات الي تم تحديثها فالبيانات الي مطلع عليها فقط ال sender/subject/
# def keepMeUpdate(sender, instance, created, **kwargs):
#     if not created:
#         Customer.
        # then  it means it is now new recoed has been added to the sender on the contrary it is already-data
        # has been just updated and we have to even send updated data to our subscribers

        # it turns out that in this case there is no need cuz a user just became a customer
        # so changes will be done by the user !,  I LOVE IT

