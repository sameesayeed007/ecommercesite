from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
import datetime
from django.urls import reverse 
from mptt.models import MPTTModel , TreeForeignKey
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
#from user_profile.models import User
from django.contrib.postgres.fields import ArrayField
import random

from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
import datetime
from django.urls import reverse 
from mptt.models import MPTTModel , TreeForeignKey
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
#from user_profile.models import User
from django.contrib.postgres.fields import ArrayField

from django.dispatch import receiver
from django.conf import settings 
from django.db.models.signals import post_save, pre_save
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from randompinfield import RandomPinField                          
from django.contrib import messages
# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from rest_framework_simplejwt.tokens import RefreshToken
from User_details.decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Min, Sum, Avg




# host_prefix = "http://"
# host_name = host_prefix+settings.ALLOWED_HOSTS[0]+":8000"

host_prefix = "https://"
host_name = host_prefix+settings.ALLOWED_HOSTS[0]

#------------------------------------- User_details--------------------------------

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<username>/<filename>
    return 'users/{0}/{1}'.format(instance.user.username, filename)


class UserManager(BaseUserManager):
    

    def create_user(self, email, password=None):
        # if username is None:
        #     raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def create_supelier(self, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, password)
        user.is_suplier = True
        user.save()
        return user

 

 

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, db_index=True,null=True,blank=True)
    email = models.EmailField(max_length=255,unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_suplier  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length= 64,default="",blank=True)
    role = models.CharField(max_length= 64,default="",blank=True)
    pwd = models.CharField(max_length= 568,default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # def __str__(self):
    #     return str(self.id)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __str__(self):
        return self.phone_number


# class GuestUser(models.Model):
  
#   ip = models.CharField(max_length=220)
#   date = models.DateTimeField(auto_now=True)

# def guest_ip_address(request):

#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

# @receiver(post_save, sender=GuestUser)
# def create_user_profile(sender, instance, created, *args, **kwargs):
#     if created:
#         Profile.objects.create(guestuser=instance)


class Profile(models.Model):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    OTHER = 'o'

    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (OTHER,'Other'),
    )

    name = models.CharField(max_length = 264,  blank = True,default="")
    email = models.CharField(max_length = 64,  blank = True,default="")
    profile_picture = models.ImageField(null=True, blank=True)
    profile_picture_url = models.CharField(max_length=255,blank=True,default="")
    phone_number = models.CharField(max_length=100 , blank=True,default="")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True,default="")
    # city = models.CharField(max_length=100, blank= True, null= True)
    # district = models.CharField(max_length=100, blank= True, null= True)
    # road_number = models.CharField(max_length = 264,blank=True, null=True)
    # building_number = models.CharField(max_length = 264,blank=True, null=True)
    # apartment_number = models.CharField(max_length = 264,blank=True, null=True)
    # user_id = models.IntegerField(blank = True, null = True,default=-1)
    address = models.TextField(blank = True, default="")
    area = models.CharField(max_length=255,blank=True,default="")
    location = models.CharField(max_length=255,blank=True,default="")
    user_id = models.IntegerField (blank = True, default=-1)



    @property
    def image(self):

        #link ='/media/'+'Product/'+str(self.product_image)
      
        #print(self.product_image)
        if self.profile_picture:
            return "{0}{1}".format(host_name,self.profile_picture.url)
        else:
            return " "
        
    
    def save(self, *args, **kwargs):
          self.profile_picture_url = self.image
          super(Profile, self).save(*args, **kwargs)


class user_relation (models.Model):
    verified_user_id = models.IntegerField (blank = True, default=-1)
    non_verified_user_id = models.IntegerField (blank = True,default=-1)


class user_supervisor_relation (models.Model):
    supervisor_id = models.IntegerField (blank = True, default=0)
    user_id = models.IntegerField (blank = True, null = True)

class ActivityLog(models.Model):
    user_id = models.IntegerField (blank = True, default=-1)
    activity_name = models.CharField(max_length=255,blank=True,default="")
    time = models.DateTimeField (auto_now_add=True)
    activity_id = models.IntegerField (blank = True, default=-1)


# class DeactivateUser(TimeStampedModel):
#     user = models.OneToOneField(User, related_name='deactivate', on_delete=models.CASCADE)
#     deactive = models.BooleanField(default=True)

class user_balance(models.Model):
    wallet = models.FloatField(blank = False, default=0)
    point = models.FloatField(blank = False,  default = 0)
    dates = models.DateTimeField (auto_now_add=True)
    user_id = models.IntegerField(blank=False, default=-1)
    ip_id = models.IntegerField(blank=False, default=-1)

class Guest_user(models.Model):
    ip_address = models.CharField(max_length = 64, blank = False,default="")
    Date = models.DateField (auto_now_add=True)
    non_verified_user_id = models.IntegerField(blank=False, default=-1)

    @property
    def sub(self):


        if self.id: 

            non_id = self.id


        else:

            non_id = 0 

        return non_id

            


    def save(self, *args, **kwargs):

        self.non_verified_user_id = self.sub
        super(Guest_user, self).save(*args, **kwargs)



# ------------------------- Advertisement ---------------------

class Advertisement(models.Model):

    image = models.ImageField(upload_to='Advertisement',null = True)
    ad_link = models.CharField(max_length=255,blank=True,default="")
    content = models.CharField(max_length=255,blank=True,default="")
    click_count = models.IntegerField(default =0)
    view_count = models.IntegerField(default=0)
    total_click_count = models.IntegerField(default =0)
    total_view_count = models.IntegerField(default=0)
    priority = models.IntegerField(default=-1)
    is_active = models.BooleanField(blank = True, default = True)
    
    def __str__(self):
        return str(self.content)

# ----------------------------- Impression ----------------------------

class ProductImpression (models.Model):

    users = ArrayField(models.IntegerField(), blank=True, default=list)
    product_id = models.IntegerField (null = False,default=-1)
    view_count = models.IntegerField (blank = True,  default = 0)
    click_count = models.IntegerField (blank = True, default = 0)
    cart_count = models.IntegerField (blank = True,default = 0)
    sales_count = models.IntegerField (blank = True,default = 0)
    non_verified_user = ArrayField(models.IntegerField(), blank=True,default=list)
    dates = models.DateTimeField(auto_now_add=True)

#-------------------------------Site Settings---------------------------------

class CompanyInfo(models.Model):
    '''
    This is Compnay Info model class.
    '''
    # company_id = models.AutoField(primary_key = True, auto_created = True, unique=True)
    name = models.CharField(max_length=500 , blank=True, default="")
    logo = models.ImageField(upload_to='Logo', blank = True,default="")
    address = models.TextField(max_length=1500,blank=True, default="" )
    icon = models.ImageField(upload_to='Icon', blank=True,default="")
    Facebook = models.CharField(max_length=264 , blank=True, default="")
    twitter = models.CharField(max_length=264 , blank=True, default="")
    linkedin = models.CharField(max_length=264 , blank=True, default="")
    youtube = models.CharField(max_length=264 , blank=True, default="")
    email = models.CharField(max_length=264 , blank=True, default="")
    phone = models.CharField(max_length=264 , blank=True, default="")
    help_center = models.CharField(max_length=264 , blank=True, default="")
    About = models.CharField(max_length=5000 , blank=True, default="")
    policy = ArrayField(models.CharField(max_length=100000), blank=True, default=list)
    terms_condition= ArrayField(models.CharField(max_length=100000), blank=True, default=list)
    slogan = models.CharField(max_length=264 , blank=True, default="")
    cookies = models.CharField(max_length=10000 , blank=True,default="")
    site_identification = models.CharField(max_length=264 , blank=True, default="", null = True)
    domain = models.CharField(max_length=500 , blank=True, default="")
    backend_domain = models.CharField(max_length=500 , blank=True, default="")


class Banner(models.Model):

    count = models.IntegerField( blank=False,default=0)
    set_time = models.IntegerField(blank = False,default=0)
    is_active = models.BooleanField(blank = True, default = True)


class Banner_Image(models.Model):
    # this call is for uploading banner images
    Banner_id = models.IntegerField(blank=True, default=-1)
    image = models.ImageField(upload_to='Banner', null = True)
    is_active = models.BooleanField(blank = True, default = True)
    link = models.CharField(max_length=500, blank=True, default="")
    content = models.CharField(max_length=264 , blank=True,default="")

class RolesPermissions(models.Model):

    roleType = models.CharField(max_length=264 , blank=True, default="")
    roleDetails = models.CharField(max_length=264 , blank=True,default="")

    def __str__(self):
        return self.roleType

class Currency (models.Model):
    ''' This model class is for currency conversion '''
    currency_type = models.CharField (max_length=100, blank = True,  default= "Taka") 
    value = models.FloatField (blank = True, default= 1.00)
    dates = models.DateTimeField (auto_now_add=True)
    role_id = models.IntegerField (blank= True,default=-1)

class ContactUs (models.Model):
    sender_name = models.CharField (max_length = 100, blank = True, default="")
    sender_email = models.EmailField(blank = True, default="")
    subject = models.CharField(max_length = 264, blank = True, default="")
    message = models.CharField (max_length = 10000, blank = True, default="")
    is_attended = models.BooleanField(blank = True,default = False)

#---------------------------------------------------------------------------------------------------------

class Settings(models.Model):
    ''' This model class is for settings '''
    tax = models.FloatField(blank = True, default=0.00)
    vat = models.FloatField(blank = True, default=0.00)
    role_id = models.IntegerField (blank= True, default=-1)
    point_value = models.FloatField(blank = True,  default = 1.00)
    point_converted_value = models.FloatField(blank = True,  default = 0.00)
    #dates = models.DateTimeField (auto_now_add=True)
    theme_id = models.IntegerField (blank= True, default=-1)


class Theme(models.Model):
    ''' This model class is for Theme details'''
    name = models.CharField(max_length=264, blank=True, default="")
    details = models.CharField (max_length=100000, blank= True,default="")

# class APIs(models.Model):
#     ''' This model class is for APIs '''
#     name = models.CharField(max_length=264, blank= True, default="")
#     details = models.CharField (max_length=100000, blank = True,default="")


class APIs(models.Model):
    ''' This model class is for APIs '''
    name = models.CharField(max_length=264, blank= True, default="", null = True)
    details = models.CharField (max_length=100000, blank = True,default="", null = True)
    API_key = models.CharField(max_length=264, blank= True, default="", null = True)
    area_url = models.CharField(max_length=264, blank= True, default="", null = True)
    location_url = models.CharField(max_length=264, blank= True, default="", null = True)
    estimation_url = models.CharField(max_length=264, blank= True, default="", null = True)
    is_enable = models.BooleanField (default= False, null = True)
    API_type = models.CharField(max_length=264, blank= True, default="", null = True)



#-------------------------------------Support---------------------------------

# Create your models here.
status = (
    ("PENDING", "Pending"),
    ("CLOSED", "Closed"),
    
)


#sender_id is the user who makes the complain 
#receiver_id is the one from the support team who receives the comments
class Ticket(models.Model):
    
    title = models.CharField(max_length=255, blank = True,default="")
    sender_id = models.IntegerField(blank = True, default=-1)
    receiver_id = models.IntegerField(blank = True,default=-1)
    department = models.CharField(max_length=255, blank=True,default="")
    complain = models.TextField(blank = True,default="")
    #replies = ArrayField(models.TextField(blank = True))
    status = models.CharField(choices=status, max_length=155, default="pending")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_attended = models.BooleanField(default=False)

    


    def __str__(self):
        return str(self.title)
        

    class Meta:
        ordering = ["-created"]


#For one user there will be one reply
#User_id refers to the user who makes the comment(customer,support)
class TicketReplies(models.Model):

    ticket_id = models.IntegerField(blank = False,default=-1)
    reply = models.TextField(blank=True,default="")
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(blank = True,default=-1)
    name = models.CharField(max_length=255,null=True)
    is_staff = models.BooleanField(default=False)


    def _str_(self):
        return str(self.reply)

#------------------------------ Email_Configuration---------------

class EmailConfig(models.Model):
    email_backend = models.CharField (max_length=64, default = "django.core.mail.backends.smtp.EmailBackend")
    email_host = models.CharField (max_length = 64, default = "smtp.gmail.com")
    email_port = models.IntegerField(default = 587)
    Tls_value = models.BooleanField(default = True)
    email_host_user = models.EmailField()
    email_host_password= models.CharField(max_length = 264)
    Ssl_value = models.BooleanField(default = False)
   
#---------------------------------Cart----------------------------------

# Create your models here.
# class Product(models.Model):
#     title = models.CharField(max_length=255, blank=True)
#     quantity = models.IntegerField(default = 10)
    

#     def __str__(self):
#         return str(self.id)



class ProductPrice(models.Model):
    product_id = models.IntegerField(default=-1, null = True)
    specification_id = models.IntegerField(default=-1, null = True)
    price = models.FloatField(default=0.00, null = True)
    purchase_price = models.FloatField(blank = True, null = True)
    date_added = models.DateTimeField(auto_now_add=True,blank=True)
    currency_id = models.IntegerField(default=-1, null = True)

    @property
    def total(self):
        new_price = -1
        old_price = -1
        lower_spec_id = -1
        prod_info_val = Product.objects.filter(id=self.product_id)
        current_date = timezone.now().date()
        if prod_info_val.exists():
            prod_info = ProductSpecification.objects.filter(product_id=self.product_id)
            spec_ids = list(prod_info.values_list('id',flat=True).distinct())
            if self.specification_id not in spec_ids:
                spec_ids.append(self.specification_id)
            spec_values= discount_product.objects.filter(specification_id__in=spec_ids,start_date__lte= current_date, end_date__gte=current_date)
            if spec_values.exists():
                min_amount = 0
                min_spec_id = -1
                for spec in spec_values:
                    if spec.discount_type == "amount":
                        if min_amount<spec.amount:
                            min_amount = spec.amount
                            min_spec_id = spec.specification_id

                    if spec.discount_type == "percentage":
                        if spec.specification_id == self.specification_id:
                            old_prc= self.price
                        else:
                            price_amount = ProductPrice.objects.filter(specification_id = spec.specification_id)
                            if price_amount.exists():
                                old_prc = price_amount[len(price_amount)-1].price
                        percent_value = (spec.amount*old_prc)/100
                        if percent_value>min_amount:
                            min_amount=percent_value
                            min_spec_id = spec.specification_id

                
                lower_spec_id = min_spec_id
                if min_spec_id == self.specification_id:
                    old_price = self.price
                else:
                    earlier_amount = ProductPrice.objects.filter(specification_id = min_spec_id)
                    if earlier_amount.exists():
                        old_price = earlier_amount[len(earlier_amount)-1].price
                if min_amount < old_price:
                    new_price = old_price-min_amount
                else:
                    new_price = 0
            else:
                data_value_spec = []
                min_price_data = 0
                for s_id in spec_ids:
                    if s_id != self.specification_id:
                        value_spec = ProductPrice.objects.filter(specification_id=s_id)
                        if value_spec.exists():
                            data_value_spec.append(value_spec[len(value_spec)-1].price)
                # min_data = data_value_spec.aggregate(Min('price'))
                # min_price_data = min_data['price__min']
                if data_value_spec:
                    print("here is the code",data_value_spec)
                    min_price_data = min(data_value_spec)
                if self.price < min_price_data:
                    print("code belongs here",min_price_data)
                    old_price = self.price
                    new_price = self.price
                    lower_spec_id = self.specification_id
                else:
                    price_amount_data = ProductPrice.objects.filter(price = min_price_data)
                    if price_amount_data.exists():
                        print("yes exists")
                        old_price = price_amount_data[len(price_amount_data)-1].price
                        new_price = price_amount_data[len(price_amount_data)-1].price
                        lower_spec_id = price_amount_data[len(price_amount_data)-1].specification_id
                    else:
                        print("here the code is")
                        old_price = self.price
                        new_price = self.price
                        lower_spec_id = self.specification_id
    
        print("old val",old_price )
        print("new val",new_price)
        try:
            product_data = Product.objects.get(id = self.product_id)
        except:
            product_data = None
        
        if product_data:
            product_data.old_price = old_price
            product_data.new_price = new_price
            product_data.lowest_spec_id = lower_spec_id
            product_data.save()

    def __str__(self):
        return str(self.product_id)

    def save(self, *args, **kwargs):
        self.total
        super(ProductPrice, self).save(*args, **kwargs)
    

class Order(models.Model):
    order =(
    ("Paid", "Paid"),
    ("Unpaid", "Unpaid"),
    ("Cancelled", "Cancelled"),
    ("Not Ordered", "Not Ordered"),
    )
    order_status =  models.CharField(choices=order, max_length=155, default="Unpaid",blank=True)
    delivery = (
    ("Pending", "Pending"),
    ("Picked", "Picked"),
    ("Shipped", "Shipped"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
    )
    delivery_status = models.CharField(choices=delivery, max_length=155, default="Pending",blank=True)
    admin = (
    ("Processing", "Processing"),
    ("Confirmed", "Confirmed"),
    ("Cancelled", "Cancelled"),
    )
    admin_status = models.CharField(choices=admin, max_length=155, default="Processing",blank=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    user_id = models.IntegerField(blank=True,default=-1)
    ip_address = models.CharField(max_length = 255,blank=True,default="")
    checkout_status = models.BooleanField(default=False,blank=True,null=True)
    ordered_date = models.DateField(auto_now_add=True,blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,default=-1)
    coupon = models.BooleanField(default=False,blank=True,null=True)
    coupon_code = models.CharField(max_length = 255,blank=True,default="")
    is_seller = models.BooleanField(default=False,blank=True,null=True)
    is_purchase = models.BooleanField(default=False,blank=True,null=True)
    is_pos = models.BooleanField(default=False,blank=True,null=True)
    terminal_id = models.IntegerField(blank=True,default=-1)
    admin_id = models.IntegerField(blank=True,default=-1)
    pos_additional_discount = models.FloatField(default=0.00,blank=True)
    pos_additional_discount_type = models.CharField(max_length = 255,blank=True,default="")
    sub_total = models.FloatField(default=0.00,blank=True)
    grand_total = models.FloatField(default=0.00,blank=True)
    payment = models.FloatField(default=0.00,blank=True)
    changes = models.FloatField(default=0.00,blank=True)
    due = models.FloatField(default=0.00,blank=True)
    vat = models.FloatField(default=0.00,blank=True)
    num_items = models.IntegerField(blank=True,default=0)
    transaction_id = models.CharField(max_length = 255,blank=True,default="")
    payment_method = models.CharField(max_length = 255,blank=True,default="")
    is_mother = models.BooleanField(default=False,blank=True,null=True)
    mother_site_order_id = models.IntegerField(blank=True,default=-1)
    reference_order_id = models.IntegerField(blank=True,default=-1)

    




    def __str__(self):
        return str(self.id)


class OrderDetails(models.Model):
    order =(
    ("Paid", "Paid"),
    ("Unpaid", "Unpaid"),
    ("Cancelled", "Cancelled"),
    ("Not Ordered", "Not Ordered"),
    )
    order_status =  models.CharField(choices=order, max_length=155, default="Unpaid",blank=True)
    delivery = (
    ("Pending", "Pending"),
    ("Picked", "Picked"),
    ("Shipped", "Shipped"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
    )
    delivery_status = models.CharField(choices=delivery, max_length=155, default="Pending",blank=True)
    order_id = models.IntegerField(blank=True,default=-1)
    product_id = models.IntegerField(blank=True,default=-1)
    specification_id = models.IntegerField(blank=True,default=-1)
    quantity = models.IntegerField(default=0,blank=True)
    date_added = models.DateTimeField(auto_now_add=True,blank=True)
    is_removed = models.BooleanField(default = False)
    delivery_removed = models.BooleanField(default = False)
    total_quantity = models.IntegerField(default=0,blank=True)
    unit_price = models.FloatField(default=0.00,blank=True)
    total_price = models.FloatField(default=0.00,blank=True)
    unit_point = models.FloatField(default=0.00,blank=True)
    total_point = models.FloatField(default=0.00,blank=True)
    product_name = models.CharField(max_length=255,blank=True,default="")
    product_color = models.CharField(max_length = 255,blank=True,default="")
    product_size = models.CharField(max_length = 255,blank=True,default="")
    product_weight = models.FloatField(default=0.00,blank=True)
    product_unit = models.CharField(max_length = 255,blank=True,default="")
    product_images = ArrayField(models.CharField(max_length=100000), blank=True,default=list)
    remaining = models.IntegerField(default=0,blank=True)
    admin =(
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Cancelled", "Cancelled"),
    )
    pro_status =(
    ("None", "None"),
    ("Returned", "Returned"),
    ("Cancelled", "Cancelled"),
    ("Damaged", "Damaged"),
    )
    admin_status = models.CharField(choices=admin, max_length=155, default="Pending",blank=True)
    product_status = models.CharField(choices=pro_status,default="None", max_length=155,blank=True, null = True)
    mother_admin_status = models.CharField(choices=admin, max_length=155, default="Pending",blank=True)
    is_own = models.BooleanField(default = True)
    def _str_(self):
        return f'{self.order_id} X {self.product_id}'



class ProductPoint(models.Model):
    point = models.FloatField(blank=True,default=0.00, null = True)
    product_id = models.IntegerField(default=-1, null = True)
    specification_id = models.IntegerField(default=-1,null = True)
    start_date = models.DateField(default=datetime.date.today)
    is_active = models.BooleanField (default = True,null = True)
    end_date = models.DateField(blank=True,null=True)

    def __str__(self):
        return f'{self.id} X {self.product_id}'

class Userz(models.Model):
    address = models.TextField()
    name = models.CharField(max_length=255,null=True)

    def __str__(self):
        return str(self.id)

class BillingAddress(models.Model):
    user_id = models.IntegerField(blank=True,default=-1)
    #address = models.TextField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    date_updated = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,default=-1)
    ip_address = models.CharField(max_length = 255,blank=True,default="")
    phone_number = models.CharField(max_length=100 ,blank=True,default="")
    name = models.CharField(max_length = 255,blank=True,default="")
    #gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    # city = models.CharField(max_length=100, blank= True, null= True,default="")
    # district = models.CharField(max_length=100, blank= True, null= True,default="")
    # road_number = models.CharField(max_length = 264,blank=True, null=True,default="")
    # building_number = models.CharField(max_length = 264,blank=True, null=True,default="")
    # apartment_number = models.CharField(max_length = 264,blank=True, null=True,default="")
    address = models.TextField(blank = True, default="")
    area = models.CharField(max_length=255,blank=True,default="")
    location = models.CharField(max_length=255,blank=True,default="")

    def __str__(self):
        return str(self.id)



    #--------------------------- Product --------------------------------

def product_image_path(instance, filename):
    return "product/images/{}/{}".format(instance.title, filename)

class ProductImage(models.Model):
    
    product_id = models.IntegerField(default= -1)
    #image= models.ImageField(upload_to='Products/', blank=True,null=True)
    product_image= models.ImageField(blank=True,null=True)
    image_url = models.CharField(max_length=255,blank=True,default="")
    content = models.CharField(max_length = 1500, blank = True,default="")
    mother_url = models.CharField(max_length=255,blank=True,default="")
    is_own = models.BooleanField(default=True)


    @property
    def image(self):

        #link ='/media/'+'Product/'+str(self.product_image)
      
        
        if self.product_image:
            # print("url")

            # print(self.product_image.url)
            # image_length = len(self.product_image.url)
            # print(type(self.product_image.url))
            # print(self.product_image.url[0:7])
            # print(self.product_image.url[7:image_length])
            # name = self.product_image.url[7:image_length]

            # invalid = '%$&@<>:"/\|?* '

            # for char in invalid:
            #     name = name.replace(char,


            return "{0}{1}".format(host_name,self.product_image.url)
        else:
            return " "
        
    
    def save(self, *args, **kwargs):

        # name = self.image 
        # print("name")
        # print(name)
        # new_name = ''.join(c for c in name if c.isalpha())
        # print(new_name)


        self.image_url = self.image
        super(ProductImage, self).save(*args, **kwargs)



class SpecificationImage(models.Model):
    
    specification_id = models.IntegerField(default= -1)
    #image= models.ImageField(upload_to='Products/', blank=True,null=True)
    product_image= models.ImageField(blank=True,null=True)
    image_url = models.CharField(max_length=255,blank=True,default="")
    content = models.CharField(max_length = 1500, blank = True,default="")


    @property
    def image(self):

        #link ='/media/'+'Product/'+str(self.product_image)
      
        
        if self.product_image:
            return "{0}{1}".format(host_name,self.product_image.url)
        else:
            return " "
        
    
    def save(self, *args, **kwargs):
          self.image_url = self.image
          super(ProductImage, self).save(*args, **kwargs)


    
class Product(models.Model):
    admin_approval = (
    ("Processing", "Processing"),
    ("Confirmed", "Confirmed"),
    ("Cancelled", "Cancelled"),
    )

    product_status_choices = (
    ("Pending", "Pending"),
    ("Published", "Published"),
    ("Cancelled", "Cancelled"),
    )
    is_own = models.BooleanField(default=True)
    shared = models.BooleanField(default=False)
    seller = models.IntegerField(default=-1,blank=True)
    product_admin_status = models.CharField(choices=admin_approval, max_length=155, default="Processing",blank=True)
    product_status = models.CharField(choices=product_status_choices, max_length=155, default="Pending",blank=True)

    category_id = models.IntegerField( blank=True ,default=-1)
    sub_category_id = models.IntegerField( blank=True ,default=-1)
    sub_sub_category_id = models.IntegerField( blank=True ,default=-1)
    title = models.CharField(max_length=250 ,blank=True,default="")
    brand = models.CharField(max_length=120 , blank=True,default="" )
    date=models.DateTimeField(auto_now_add=True)
    #image = ArrayField(models.ImageField(upload_to=product_image_path, blank=True),null=True , blank=True)
    description = models.TextField( blank=True,default="")
    key_features=ArrayField(models.TextField(null=True , blank=True),blank=True,default=list)
    is_deleted = models.BooleanField(default=False)
    properties= models.BooleanField(default=True)
    is_group = models.BooleanField(default=False)
    origin = models.CharField(max_length=200, blank=True,default="")
    shipping_country = models.CharField(max_length=200, blank=True,default="")
    lowest_spec_id = models.IntegerField( blank=True ,default = -1)
    old_price = models.FloatField(blank = True,default=0.00)
    new_price = models.FloatField(blank = True,default=0.00)
    mother_approval = (
    ("Processing", "Processing"),
    ("Confirmed", "Confirmed"),
    ("Cancelled", "Cancelled"),
    )
    mother_status = models.CharField(choices=mother_approval, max_length=155, default="Processing",blank=True)
    mother_product_id = models.IntegerField(default=-1, null = True)
    


    # @property
    # def weight_u(self):
    #     weight_unit = str(self.weight)+str(self.unit)
    #     return weight_unit

    # @property
    # def old_price(self):
        
    #     product_price_val = ProductPrice.objects.filter(product_id=self.id)
    #     print("here is the code", product_price_val)
    #     if product_price_val.exists():
    #         for prices in product_price_val:
    #             print("prices2222222", prices.specification_id)
        
    #     return 50

            
        

    # def save(self, *args, **kwargs):
    #     self.lowest_old_price = self.old_price
    #     # self.weight_unit = self.weight_u
    #     print("save er moddhe")
    #     # print(self.quantity)
    #     super(Product, self).save(*args, **kwargs)





class Variation(models.Model):
    product_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=120,default="")
    sale_price = models.FloatField( blank=True,default=0.00)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True, blank=True) #refer none == unlimited amount

    def __unicode__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    # def get_html_price(self):
    #   if self.sale_price is not None:
    #       html_text = "<span class='sale-price'>%s</span> <span class='og-price'>%s</span>" %(self.sale_price, self.price)
    #   else:
    #       html_text = "<span class='price'>%s</span>" %(self.price)
    #   return mark_safe(html_text)

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def add_to_cart(self):
        return "%s?item=%s&qty=1" %(reverse("cart"), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" %(reverse("cart"), self.id)

    def get_title(self):
        return "%s - %s" %(self.product.title, self.title)



def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    # variations = product.variation_set.all()
    # if variations.count() == 0:
    #   new_var = Variation()
    #   new_var.product = product
    #   new_var.title = "Default"
    #   new_var.price = product.price
    #   new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)



class Category(models.Model):
    #product_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=120, unique=True,null=True,blank=True)
    category_id = models.IntegerField(default=-1)
    active = models.BooleanField(default=False)
    level = models.CharField(max_length=120, default="First")
    #slug = models.SlugField(unique=True)
    #active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_active = models.BooleanField(default=False)

    @property
    def sub(self):


        if self.id: 

            category_id = self.id


        else:

            category_id = 0 

        return category_id 

            


    def save(self, *args, **kwargs):

        self.category_id = self.sub
        super(Category, self).save(*args, **kwargs)




class Sub_Category(models.Model):
    category_id = models.IntegerField(default=-1)
    sub_category_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=120,default="None",blank=True)
    active = models.BooleanField(default=False)
    level = models.CharField(max_length=120,default="Second")
    is_active = models.BooleanField(default=False)
    #slug = models.SlugField(unique=True)
    #active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    children = ArrayField(models.CharField(max_length=120,null=True , blank=True),blank=True,default=list)


    @property
    def sub(self):


        if self.id: 

            sub_cat = self.id


        else:

            sub_cat = 0 

        return sub_cat

            


    def save(self, *args, **kwargs):

        self.sub_category_id = self.sub
        super(Sub_Category, self).save(*args, **kwargs)

    # @property
    # def sub(self):


    #     if self.id is not None: 

    #         print("entering here")



    #         subsub = []

    #         try:

    #             sub_sub = Sub_Sub_Category.objects.filter(sub_category_id=self.id)


    #         except:

    #             sub_sub = None 

    #         if sub_sub:
    #             print(here)

    #             subsub = list(existing.values_list('title',flat=True))

    #         else:

    #             subsub



    #     def save(self, *args, **kwargs):
    #       self.sub_sub_categories = self.sub
    #       super(Sub_category, self).save(*args, **kwargs)



class Sub_Sub_Category(models.Model):
    sub_category_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=120,default="None",blank=True)
    active = models.BooleanField(default=False)
    level = models.CharField(max_length=120,default="Third")
    is_active = models.BooleanField(default=False)
    #slug = models.SlugField(unique=True)
    #active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    sub_sub_category_id = models.IntegerField(default=-1)

    @property
    def sub(self):


        if self.id: 

            sub_sub = self.id


        else:

            sub_sub = 0 

        return sub_sub 

            


    def save(self, *args, **kwargs):

        self.sub_sub_category_id = self.sub
        super(Sub_Sub_Category, self).save(*args, **kwargs)


class GroupProduct(models.Model):
    specification_ids = ArrayField(models.IntegerField( null=True , blank=True),blank=True,default=list)
    title = models.CharField(max_length=120, blank = True,default="")
    #slug = models.SlugField(unique=True , blank=True)
    startdate=models.DateField(auto_now_add=True,blank=True)
    enddate=models.DateField(null=True , blank=True)
    flashsellname = models.CharField(max_length=120, blank = True , null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    product_id = models.IntegerField(null = True, blank = True)

    def __unicode__(self):
        return self.title

# class DeliveryInfo(models.Model):
#     specification_id = models.IntegerField(null = True, blank = True)
#     height = models.FloatField(blank = True, default= 0.00, null = True)
#     width = models.FloatField(blank = True, default= 0.00,null = True)
#     length = models.FloatField(blank = True, default= 0.00,null = True)
#     weight = models.FloatField(blank = True, default= 0.00,null = True)
#     measument_unit= models.CharField(max_length=120, blank = True , null=True)
#     charge_inside = models.IntegerField(blank = True, default= 0.00,null = True)
#     charge_outside= models.IntegerField(blank = True, default= 0.00,null = True)

#------------------------------------- Product_Comments--------------------------------
class Comment(models.Model):
    comment = models.TextField(blank = True)
    date_created = models.DateField(auto_now_add=True)
    product_id = models.IntegerField(default=0)

    user_id = models.IntegerField(blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return self.comment

    class Meta:
        ordering = ["-date_created"]


class CommentReply(models.Model):
    comment_id = models.IntegerField(blank = True,null=True)
    reply = models.TextField(blank = True)
    date_created = models.DateField(auto_now_add=True)
    user_id = models.IntegerField(blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.reply

    class Meta:
        ordering = ["-date_created"]

#------------------------------------- Product_Reviews--------------------------------
class Reviews(models.Model):
    product_id = models.IntegerField(default=0)
    
    user_id = models.IntegerField(blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,null=True)
    content = models.TextField(blank = True)
    image = models.ImageField(upload_to = 'product_reviews' ,null=True, blank = True)
    num_stars = (
        (1 , "Worst"),
        (2 , "Bad"),
        (3 , "Not Bad"),
        (4 , "Good"),
        (5 , "Excellent"),
        )
    rating = models.IntegerField(choices=num_stars,blank=True,null=True)
    date_created = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-date_created"]

# -------------------------- Product Code ------------------------------------



#------------------------- Product Discount ---------------------------------

class discount_product(models.Model):
    Sales_type = (

        ('none', 'none'),
        ('amount', 'amount'),
        ('percentage', 'percentage'),
    )
    discount_type = models.CharField(max_length=264, blank=True, null= True,choices=Sales_type)
    amount = models.FloatField (blank = False, default =0.00,null= True)
    start_date = models.DateField (blank=True,null=True)
    end_date = models.DateField (blank = False, null = True)
    max_amount = models.FloatField (blank = False, default =0,null= True)
    group_product_id = models.IntegerField(blank=False, null=True)
    product_id = models.IntegerField(blank=False, default = -1,null= True)
    specification_id = models.IntegerField(blank=False, default = -1,null= True)
    is_active = models.BooleanField (default = True,null= True)

    @property
    def total(self):
        current_date = timezone.now().date()
        selling_price = 0
        old_price= 0
        new_price = 0
        lowest_spec_id = -1
        spec_id = -1
        if self.start_date <=current_date and self.end_date >=current_date:
            # selling_price = 0
            # old_price= 0
            # new_price = 0
            # lowest_spec_id = -1
            # spec_id = -1
            price_amount = ProductPrice.objects.filter(specification_id = self.specification_id)
            if price_amount.exists():
                selling_price = price_amount[len(price_amount)-1].price
                #print("current selling price value", selling_price)
            prod_info_val = Product.objects.filter(id=self.product_id)
            if prod_info_val.exists():
                if prod_info_val[0].old_price and prod_info_val[0].new_price:
                    old_price = prod_info_val[0].old_price
                    new_price = prod_info_val[0].new_price
                    lowest_spec_id = prod_info_val[0].lowest_spec_id
            
            if self.discount_type == 'amount':
                #print("here is the earlier value", old_price)
                new_dis_price = selling_price - self.amount
                #print("new dis price",new_dis_price)
                if new_dis_price <0:
                    new_dis_price = 0
                #print("current spec id", self.specification_id)
                if lowest_spec_id == self.specification_id:
                    #print("here is the code")
                    new_price = new_dis_price
                    old_price = selling_price
                    spec_id = self.specification_id
                if lowest_spec_id != self.specification_id and new_dis_price <new_price:
                    new_price = new_dis_price
                    old_price = selling_price
                    spec_id = self.specification_id

            elif self.discount_type == 'percentage':
                percent_price = (selling_price * self.amount)/100
                new_dis_price = selling_price - percent_price
                if new_dis_price <0:
                    new_dis_price = 0
                if lowest_spec_id == self.specification_id:
                    new_price = new_dis_price
                    old_price = selling_price
                    spec_id = self.specification_id
                if lowest_spec_id != self.specification_id and new_dis_price <new_price:
                    new_price = new_dis_price
                    old_price = selling_price
                    spec_id = self.specification_id
            else:
                pass
        try:
            product_data = Product.objects.get(id = self.product_id)
        except:
            product_data = None
        
        if product_data:
            product_data.old_price = old_price
            product_data.new_price = new_price
            product_data.lowest_spec_id = self.specification_id
            product_data.save()

    def __str__(self):
        return str(self.product_id)

    def save(self, *args, **kwargs):
        self.total
        # self.weight_unit = self.weight_u
        print("save er moddhe")
        # print(self.quantity)
        super(discount_product, self).save(*args, **kwargs)




# ---------------------- Product Cupon -------------------------------------------

class Cupons(models.Model):
    cupon_code = models.CharField(max_length= 264, blank = True, null = True)
    amount = models.FloatField (blank = True, null = True)
    start_from = models.DateField(blank = True, null = True)
    valid_to = models.DateField(blank = True, null = True)
    is_active = models.BooleanField()

# ---------------------------------- FAQ-----------------------------------------

class FAQ (models.Model):
    question = models.CharField(max_length = 264, blank = True, null = True)
    ans = models.CharField (max_length = 3000, blank = True, null = True)
    date = models.DateField(auto_now_add=True)


class ProductCode (models.Model):
    Barcode_img = models.CharField(max_length = 264,null = True, blank = True)
    date = models.DateField(auto_now_add=True)
    product_id = models.IntegerField(blank = False, default = -1)
    specification_id = models.IntegerField(blank = False, default = -1)
    Barcode = models.CharField(max_length = 264,null = True, blank = True)
    manual_Barcode = models.CharField(max_length = 264,null = True, blank = True)
    SKU = models.CharField(max_length = 264,null = True, blank = True)
    manual_SKU = models.CharField(max_length = 264,null = True, blank = True)
    SKU_img = models.CharField(max_length = 264,null = True, blank = True)


# ----------------------------------- Product Inventory ---------------------------
class ProductSpecification(models.Model):
    product_id = models.IntegerField(default=-1, null = True)
    mother_specification_id = models.IntegerField(default=-1, null = True)
    shared = models.BooleanField(default=False)
    size = models.CharField(max_length=200, blank=True,default="", null = True)
    unit = models.CharField(max_length=200, blank=True,default="", null = True)
    weight = models.CharField(max_length = 255,blank=True,default="", null = True)
    #color = ArrayField(models.CharField(max_length=200,default="abc"),default=list,blank=True)
    color = models.CharField(max_length=200, blank=True,default="", null = True)
    warranty = models.CharField(max_length=200, blank=True,default="", null = True)
    warranty_unit = models.CharField(max_length=200, blank=True,default="", null = True)
    quantity = models.IntegerField(default=0, null = True)
    vat = models.FloatField (blank = True, default =0.0,null= True)
    weight_unit = models.CharField(max_length=200, blank=True,default="", null = True)
    manufacture_date = models.DateField(blank=True, null = True)
    admin_id = models.IntegerField(blank = True, default = -1,null= True)
    expire = models.DateField(blank=True,null = True)
    seller_quantity = models.IntegerField(default=0, null = True)
    remaining = models.IntegerField(default=0, null = True)
    is_own = models.BooleanField(default=True)
    admin_approval = (
    ("Processing", "Processing"),
    ("Confirmed", "Confirmed"),
    ("Cancelled", "Cancelled"),
    )
    admin_status = models.CharField(choices=admin_approval, max_length=155, default="Processing",blank=True)
    mother_approval = (
    ("Processing", "Processing"),
    ("Confirmed", "Confirmed"),
    ("Cancelled", "Cancelled"),
    )
    mother_status = models.CharField(choices=mother_approval, max_length=155, default="Processing",blank=True)
    specification_status_choices = (
    ("Pending", "Pending"),
    ("Published", "Published"),
    ("Cancelled", "Cancelled"),
    )
    specification_status = models.CharField(choices=specification_status_choices, max_length=155, default="Published",blank=True)
    on_hold = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
        
    @property
    def weight_u(self):
        weight_unit = str(self.weight)+str(self.unit)
        return weight_unit

    @property
    def total(self):
        try:
            warehouses = WarehouseInfo.objects.filter(specification_id=self.id)
        except:
            warehouses = None 
        if warehouses:
            w_quantity_list = list(warehouses.values_list('quantity',flat = True))
            w_quantity = sum(w_quantity_list)
        else:
            w_quantity = 0
        try:
            shops = ShopInfo.objects.filter(specification_id=self.id)
        except:
            shops = None 
        if shops:
            s_quantity_list = list(shops.values_list('quantity',flat = True))
            s_quantity = sum(s_quantity_list)
        else:
            s_quantity = 0
        total_quantity = w_quantity + s_quantity
        return total_quantity

    def save(self, *args, **kwargs):
        self.quantity = self.total
        self.weight_unit = self.weight_u
        # print("save er moddhe")
        # print(self.quantity)
        super(ProductSpecification, self).save(*args, **kwargs)
        # print("save er pore")
        # print(self.quantity)
    # @property
    # def quantity(self):
    #     total = self.warehouse_quantity + self.shop_quantity
    #     float_total = format(total, '0.2f')
    #     return float_total
    # @property
    # def total(self):
    #     #link ='/media/'+'Product/'+str(self.product_image)
    #     # print(self.product_image)
    #     print("id ase")
    #     try:
    #         warehouses = Warehouse.objects.filter(specification_id=self.id)
    #     except:
    #         warehouses = None
    #     print(warehouses)
    #     if warehouses:
    #         w_quantity_list = list(warehouses.values_list('product_quantity',flat = True))
    #         w_quantity = sum(w_quantity_list)
    #         print(w_quantity)
    #     else:
    #         w_quantity = 0
    #     try:
    #         shops = Shop.objects.filter(specification_id=self.id)
    #     except:
    #         shops = None
    #     if shops:
    #         s_quantity_list = list(shops.values_list('product_quantity',flat = True))
    #         s_quantity = sum(s_quantity_list)
    #         print(s_quantity)
    #     else:
    #         s_quantity = 0
    #     total_quantity = w_quantity + s_quantity
    #     return total_quantity
    # def save(self, *args, **kwargs):
    #     self.quantity = self.total
    #     print("save er moddhe")
    #     print(self.quantity)
    #     super(ProductSpecification, self).save(*args, **kwargs)
    #     print("save er pore")
    #     print(self.quantity)
# class Warehouse(models.Model):
#     warehouse_name = models.CharField(max_length=264, blank=True, null= True)
#     warehouse_location = models.CharField(max_length=2048, blank=True, null= True)
#     product_quantity = models.IntegerField(blank=False, null=True,default=0)
#     specification_id = models.IntegerField(blank=False, null=True,default=-1)
#     date = models.DateField (auto_now_add=True,blank=True,null=True)
#     shop_quantity = models.IntegerField(blank=False, null=True,default=0)
#     warehouse_quantity = models.IntegerField(blank=False, null=True,default=0)
#     @property
#     def shop(self):
#         try:
#             spec = Shop.objects.filter(specification_id=self.specification_id)
#         except:
#             spec = None
#         if spec:
#             s_list = list(spec.values_list('product_quantity',flat = True))
#             s_quantity = sum(s_list)
#         else:
#             s_quantity = 0
#         return s_quantity
#     @property
#     def warehouse(self):
#         try:
#             spec = Warehouse.objects.filter(specification_id=self.specification_id)
#         except:
#             spec = None
#         if spec:
#             s_list = list(spec.values_list('product_quantity',flat = True))
#             s_quantity = sum(s_list)
#         else:
#             s_quantity = 0
#         return s_quantity
#     def save(self, *args, **kwargs):
#         self.shop_quantity = self.shop
#         self.warehouse_quantity = self.warehouse
#         super(Warehouse, self).save(*args, **kwargs)
#         # print(self.shop_quantity)
#         # print(self.warehouse_quantity)
#         try:
#             ware = Warehouse.objects.get(id = self.id)
#             print(ware)
#         except:
#             ware = None
#         if ware:
#             warehouse_quantity = ware.warehouse_quantity
#             shop_quantity = ware.shop_quantity
#             print(warehouse_quantity)
#             print(shop_quantity)
#             total_quantity = warehouse_quantity + shop_quantity
#             try:
#                 prod_spec = ProductSpecification.objects.get(id=self.specification_id)
#             except:
#                 prod_spec = None
#             if prod_spec:
#                 prod_spec.quantity = total_quantity
#                 prod_spec.save()
# class Shop(models.Model):
#     shop_name = models.CharField(max_length=264, blank=True, null= True)
#     shop_location = models.CharField(max_length=2048, blank=True, null= True)
#     product_quantity = models.IntegerField(blank=False, null=True)
#     specification_id = models.IntegerField(blank=False, null=True)
#     date = models.DateField (auto_now_add=True,blank=True,null=True)
#     shop_quantity = models.IntegerField(blank=False, null=True,default=0)
#     warehouse_quantity = models.IntegerField(blank=False, null=True,default=0)
#     # @property
#     # def save_specification(self):
#     #     spec = ProductSpecification()
#     #     # spec_id = spec.id
#     #     spec.save()
#     #     # print("after save")
#     #     # print(spec.total_quantity)
#     #     return 1
#     # def save(self, *args, **kwargs):
#     #     self.specification_id = self.save_specification
#     #     super(Shop, self).save(*args, **kwargs)
#     @property
#     def shop(self):
#         try:
#             spec = Shop.objects.filter(specification_id=self.specification_id)
#         except:
#             spec = None
#         if spec:
#             s_list = list(spec.values_list('product_quantity',flat = True))
#             s_quantity = sum(s_list)
#         else:
#             s_quantity = 0
#         return s_quantity
#     @property
#     def warehouse(self):
#         try:
#             spec = Warehouse.objects.filter(specification_id=self.specification_id)
#         except:
#             spec = None
#         if spec:
#             s_list = list(spec.values_list('product_quantity',flat = True))
#             s_quantity = sum(s_list)
#         else:
#             s_quantity = 0
#         return s_quantity
#     def save(self, *args, **kwargs):
#         self.shop_quantity = self.shop
#         self.warehouse_quantity = self.warehouse
#         super(Shop, self).save(*args, **kwargs)
#         # print(self.shop_quantity)
#         # print(self.warehouse_quantity)
#         try:
#             ware = Shop.objects.get(id = self.id)
#             print(ware)
#         except:
#             ware = None
#         if ware:
#             warehouse_quantity = ware.warehouse_quantity
#             shop_quantity = ware.shop_quantity
#             print(warehouse_quantity)
#             print(shop_quantity)
#             total_quantity = warehouse_quantity + shop_quantity
#             try:
#                 prod_spec = ProductSpecification.objects.get(id=self.specification_id)
#             except:
#                 prod_spec = None
#             if prod_spec:
#                 prod_spec.quantity = total_quantity
#                 prod_spec.save()
      



class Inventory_Price(models.Model):

    product_id = models.IntegerField( blank=True ,default=-1)
    specification_id = models.IntegerField( blank=True ,default=-1)
    quantity = models.IntegerField( blank=True ,default=0)
    date = models.DateField(blank=True,default="")
    price = models.IntegerField(blank=True,default=0)

    def __str__(self):
        return f'{self.product_id} X {self.specification_id}'



# class OrderInfo(models.Model):

#     order_id = models.IntegerField( blank=True , null=True,default=-1)



class Warehouse(models.Model):

    warehouse_name = models.CharField(max_length=264, blank=True, default = "")
    warehouse_location = models.CharField(max_length=264, blank=True, default = "")



class Shop(models.Model):


    shop_name = models.CharField(max_length=264, blank=True, default = "")
    shop_location = models.CharField(max_length=264, blank=True, default = "")


class WarehouseInfo(models.Model):

    warehouse_id = models.IntegerField(blank=True,default=-1)
    specification_id = models.IntegerField(blank=True,default=-1)
    product_id = models.IntegerField(blank=True,default=-1)
    quantity = models.IntegerField(blank=True,default=0)

    def save(self, *args, **kwargs):


        #self.shop_quantity = self.shop
        # self.warehouse_quantity = self.warehouse
        super(WarehouseInfo, self).save(*args, **kwargs)
        # print(self.shop_quantity)
        # print(self.warehouse_quantity)
        try:

            warehouses = WarehouseInfo.objects.filter(specification_id=self.specification_id)


        except:

            warehouses = None 


        if warehouses:

            w_quantity_list = list(warehouses.values_list('quantity',flat = True))
            w_quantity = sum(w_quantity_list)


        else:

            w_quantity = 0



        try:

            shops = ShopInfo.objects.filter(specification_id=self.specification_id)


        except:

            shops = None 


        if shops:

            s_quantity_list = list(shops.values_list('quantity',flat = True))
            s_quantity = sum(s_quantity_list)


        else:

            s_quantity = 0



        total_quantity = w_quantity + s_quantity

        
        



        try:
            
            prod_spec = ProductSpecification.objects.get(id=self.specification_id)

        except:

            

            prod_spec = None

           

        if prod_spec:
            prod_spec.quantity = total_quantity
            prod_spec.save()

           


class ShopInfo(models.Model):

    shop_id = models.IntegerField(blank=True,default=-1)
    specification_id = models.IntegerField(blank=True,default=-1)
    quantity = models.IntegerField(blank=True,default=0)
    product_id = models.IntegerField(blank=True,default=-1)


    def save(self, *args, **kwargs):

        

        #self.shop_quantity = self.shop
        # self.warehouse_quantity = self.warehouse
        super(ShopInfo, self).save(*args, **kwargs)
        # print(self.shop_quantity)
        # print(self.warehouse_quantity)
        try:

            warehouses = WarehouseInfo.objects.filter(specification_id=self.specification_id)


        except:

            warehouses = None 


        if warehouses:

            w_quantity_list = list(warehouses.values_list('quantity',flat = True))
            w_quantity = sum(w_quantity_list)


        else:

            w_quantity = 0



        try:

            shops = ShopInfo.objects.filter(specification_id=self.specification_id)


        except:

            shops = None 


        if shops:

            s_quantity_list = list(shops.values_list('quantity',flat = True))
            s_quantity = sum(s_quantity_list)


        else:

            s_quantity = 0



        total_quantity = w_quantity + s_quantity

        

        try:
            

            prod_spec = ProductSpecification.objects.get(id=self.specification_id)

        except:

            prod_spec = None

           

        if prod_spec:
            prod_spec.quantity = total_quantity
            prod_spec.save()



# class inventory_report(models.Model):

#     product_id = models.IntegerField(blank=False,default = -1)
#     specification_id = models.IntegerField(blank=False,default = -1)
#     debit = models.IntegerField(blank=True, null=True,default=0)
#     credit = models.IntegerField(blank=True, null=True,default=0)
#     warehouse_id = models.IntegerField(blank=True,default = -1)
#     shop_id = models.IntegerField(blank=True,default = -1)
#     date = models.DateField(auto_now_add=True,null=True , blank=True)
#     selling_price = models.FloatField(blank=True, null=True)
#     purchase_price = models.FloatField(blank=True, null=True)
#     requested = models.IntegerField(blank=True, null=True,default=0)
#     admin_id = models.IntegerField(blank=False,default = -1)



class inventory_report(models.Model):
    product_id = models.IntegerField(blank=False,default = -1)
    specification_id = models.IntegerField(blank=False,default = -1)
    debit = models.IntegerField(blank=True, null=True,default=0)
    credit = models.IntegerField(blank=True, null=True,default=0)
    warehouse_id = models.IntegerField(blank=True,default = -1)
    shop_id = models.IntegerField(blank=True,default = -1)
    date = models.DateField(auto_now_add=True,null=True , blank=True)
    selling_price = models.FloatField(blank=True, null=True)
    purchase_price = models.FloatField(blank=True, null=True)
    requested = models.IntegerField(blank=True, null=True,default=0)
    admin_id = models.IntegerField(blank=False,default = -1)
    manager_attend = models.BooleanField(default=False)



class OrderInfo(models.Model):


    order_id = models.IntegerField(blank=True,default=-1)
    billing_address_id = models.IntegerField(blank=True,default=-1)
    area_id = models.IntegerField(blank=True,default=-1)
    company_id = models.IntegerField(blank=True,default=-1)
    company_name = models.CharField(max_length=264,blank=False,default= "")
    company_details = models.TextField(blank = True,default="")
    delivery_type_id = models.IntegerField(blank=True,default=-1)
    delivery_date = models.DateField(auto_now_add=True,blank=True,null=True)
    days = models.IntegerField(blank=True,default=0)
    host_site = models.CharField(max_length=264,blank=True,default= "")
    location_id = models.IntegerField(blank=True,default=-1)
    location_details = models.TextField(blank = True,default="")
    payment_type = models.CharField(max_length=264,blank=True,default= "")
    total_amount = models.FloatField(blank=True,default=0.00)



class Invoice(models.Model):


    order_id = models.IntegerField(blank=False,default=-1)
    date = models.DateTimeField(default=timezone.now, null=True,blank=True )
    time = models.DateTimeField(default=timezone.now, null=True,blank=True )
    ref_invoice = models.IntegerField(blank=False,default=0)
    is_active = models.BooleanField(default=True)
    admin_id = models.IntegerField(blank=True,default=-1)
    invoice_no = models.CharField(max_length=264,blank=True,default= "")


class ProductBrand (models.Model):
    Brand_name = models.CharField(max_length=264,blank=True,default= "")
    Brand_owner = models.CharField(max_length=264,blank=True,default= "")
    Brand_country = models.CharField(max_length=264,blank=True,default= "")
    created_date = models.DateField (auto_now_add=True,blank=True,null=True)


class DeliveryArea(models.Model):
    specification_id = models.IntegerField(null = True, blank = True)
    Area_name = models.CharField(max_length=120, blank = True,default="")
    Area_details = models.CharField(max_length=264, blank = True,default="")
    date_created = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(blank= True, null = True, default = False)

    def __str__(self):
        return str(self.Area_name)

class DeliveryLocation(models.Model):
    area_id = models.IntegerField(null = True, blank = True)
    location_name = models.CharField(max_length=120, blank = True,default="")
    date_created = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(blank= True, null = True, default = False)

    def __str__(self):
        return str(self.location_name)

class DeliveryInfo(models.Model):
    location_id = models.IntegerField(null = True, blank = True)
    height = models.FloatField(blank = True, default= 0.00, null = True)
    width = models.FloatField(blank = True, default= 0.00,null = True)
    length = models.FloatField(blank = True, default= 0.00,null = True)
    weight = models.FloatField(blank = True, default= 0.00,null = True)
    measument_unit= models.CharField(max_length=120, blank = True , null=True)
    unit_price = models.IntegerField(blank = True, default= 0.00,null = True)
    delivery_day = models.IntegerField(blank = True,null = True)
    minimum_amount = models.FloatField(blank = True, default= 0.00,null = True)
    specification_id = models.IntegerField(null = True, blank = True)
    delivery_free = models.BooleanField(blank= True, null = True, default = False)





class subtraction_track(models.Model):
    order_id = models.IntegerField(blank=False,default = -1)
    specification_id = models.IntegerField(blank=False,default = -1)
    debit_quantity = models.IntegerField(blank=True, null=True,default=0)
    warehouse_id = models.IntegerField(blank=True,default = -1)
    shop_id = models.IntegerField(blank=True,default = -1)
    date = models.DateField(auto_now_add=True,null=True , blank=True)
    admin_id = models.IntegerField(blank=False,default = -1)



class OTP_track(models.Model):
    user_id = models.IntegerField(blank=False, default=-1)
    order_id=models.IntegerField(blank=False, default=-1)
    phone_number = models.CharField(max_length= 64,default="",blank=True)
    otp_token=models.CharField(max_length=10 , default="", blank=False )
    isVerified = models.BooleanField(blank=False, default=False)
    otp_session_id = models.CharField(max_length=120, null=True, default = "")
    
    def __str__(self):
        return str(self.phone_number) + ' is sent ' + str(self.otp_token)




class product_delivery_area (models.Model):
    specification_id = models.IntegerField(blank=True,default = -1, null = True)
    is_Bangladesh = models.BooleanField(blank=True, default=True, null = True)
    delivery_area_id = models.IntegerField(blank=True,default = -1, null = True)
    delivery_location_ids =  ArrayField(models.IntegerField(), blank=True, default=list, null = True) 

    def __str__(self):
        return str(self.specification_id) + ' X ' + str(self.delivery_area_id)




# class Notifications(models.Model):

#     support_id = models.IntegerField(blank=True,default = -1, null = True)
#     supportreply_id = models.IntegerField(blank=True,default = -1, null = True)
#     comment_id = models.IntegerField(blank=True,default = -1, null = True)
#     commentreply_id = models.IntegerField(blank=True,default = -1, null = True)
#     purchaseinvoice_id = models.IntegerField(blank=True,default = -1, null = True)

class Terminal(models.Model):

    terminal_name = models.CharField(max_length=120, null=True, default = "")
    warehouse_id = models.IntegerField(blank=True,default = -1, null = True)
    shop_id = models.IntegerField(blank=True,default = -1, null = True)
    site_id = models.IntegerField(blank=True,default = 1234 , null = True)
    API_key = models.CharField(max_length=120, null=True, default = "",blank = True)
    date_creation = models.DateField(auto_now_add=True,null=True , blank=True)
    admin_id = models.IntegerField(blank=True,default = -1, null = True)
    is_active = models.BooleanField(blank=False, default=True)


    @property
    def generate(self):

        name = ""
        stock_id = -1 

        if self.warehouse_id:
            w_id = self.warehouse_id

        else:
            w_id = -1 


        if self.shop_id:
            s_id = self.shop_id

        else:
            s_id = -1 


        if s_id == -1:

            name = "W"
            stock_id = w_id

        elif w_id == -1:

            name = "S"
            stock_id = s_id


        random_number = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) 



        API_key = name + str(stock_id) + "Z" +str(self.id) + "X" + str(self.site_id) + "Y" + random_number

        return API_key

    
    def save(self, *args, **kwargs):

        self.API_key = self.generate
        super(Terminal, self).save(*args, **kwargs)
        # print("save hoise")
        # try:
        #     term  = Terminal.objects.get(id=self.id)

        # except:
        #     term = None 

        # # print("terminal hoise")
        # # print(term)

        # if term:
        #     term.save()
            # print(term.API_key)



class TerminalUsers(models.Model):

    terminal_id = models.IntegerField(blank=True,default = -1, null = True)
    user_id = models.IntegerField(blank=True,default = -1, null = True)
    is_active = models.BooleanField(blank=False, default=True)


class SpecificationPrice(models.Model):

    status_choices = (
    ("Single", "Single"),
    ("Minimum", "Minimum"),
    ("Maximum", "Maximum"),
    )
    status = models.CharField(choices= status_choices, max_length=155, default="Single",blank=True)
    quantity = models.IntegerField(blank=True,default = 0, null = True)
    purchase_price = models.FloatField(default=0.0,blank=True, null=True)
    selling_price = models.FloatField(default=0.0,blank=True, null=True)
    mrp = models.FloatField(default=0.0,blank=True, null=True)
    is_active = models.BooleanField(blank=False, default=True)
    specification_id = models.IntegerField(blank=True,default = -1, null = True)
    is_own = models.BooleanField(blank=False, default=True)
    mother_specification_id = models.IntegerField(blank=True,default = -1, null = True)
    increament_choices = (
    ("Percentage", "Percentage"),
    ("Amount", "Amount"),
    )
    increament_type = models.CharField(choices= increament_choices, max_length=155, default="Percentage",blank=True)
    increament_value = models.FloatField(default=0.0,blank=True, null=True)



class MotherSpecificationPrice(models.Model):

    status_choices = (
    ("Single", "Single"),
    ("Minimum", "Minimum"),
    ("Maximum", "Maximum"),
    )
    status = models.CharField(choices= status_choices, max_length=155, default="Single",blank=True)
    quantity = models.IntegerField(blank=True,default = 0, null = True)
    purchase_price = models.FloatField(default=0.0,blank=True, null=True)
    selling_price = models.FloatField(default=0.0,blank=True, null=True)
    mrp = models.FloatField(default=0.0,blank=True, null=True)
    is_active = models.BooleanField(blank=False, default=True)
    specification_id = models.IntegerField(blank=True,default = -1, null = True)
    is_own = models.BooleanField(blank=False, default=True)
    mother_specification_id = models.IntegerField(blank=True,default = -1, null = True)

class PaymentInfo(models.Model):

    order_id = models.IntegerField(blank=True,default = -1, null = True)
    transaction_id = models.CharField(max_length = 1024,blank=True,default="",null = True)
    payment_method = models.CharField(max_length = 1024,blank=True,default="",null = True)
    merchant_id = models.CharField(max_length = 1024,blank=True,default="",null = True)
    payment_reference_id = models.CharField(max_length = 1024,blank=True,default="",null = True)
    amount = models.CharField(max_length = 1024,blank=True,default="",null = True)
    client_mobile_number = models.CharField(max_length = 1024,blank=True,default="",null = True)
    order_datetime = models.CharField(max_length = 1024,blank=True,default="",null = True)
    issuer_payment_datetime = models.CharField(max_length = 1024,blank=True,default="",null = True)
    issuer_payment_ref_no = models.CharField(max_length = 1024,blank=True,default="",null = True)
    additional_merchant_info = models.CharField(max_length = 1024,blank=True,default="",null = True)
    status = models.CharField(max_length = 1024,blank=True,default="",null = True)
    status_code = models.CharField(max_length = 1024,blank=True,default="",null = True)
    cancelissuer_datetime = models.CharField(max_length = 1024,blank=True,default="",null = True)
    cancelissuer_ref_no = models.CharField(max_length = 1024,blank=True,default="",null = True)



class Subscribers(models.Model):


    subscription_choices = (
    ("None", "None"),
    ("Newsletter", "Newsletter"),
    )
    subscription_status = models.CharField(choices= subscription_choices, max_length=155, default="Newsletter",blank=True)
    email = models.CharField(max_length = 64,  blank = True,default="")
    is_subscribed = models.BooleanField(blank=True, default=True)


class BkashPaymentInfo(models.Model):

    order_id = models.IntegerField(blank=True,default = -1, null = True)
    payment_id = models.CharField(max_length = 1024,blank=True,default="",null = True)
    create_time = models.CharField(max_length = 1024,blank=True,default="",null = True)
    update_time = models.CharField(max_length = 1024,blank=True,default="",null = True)
    transaction_id = models.CharField(max_length = 1024,blank=True,default="",null = True)
    transaction_status = models.CharField(max_length = 1024,blank=True,default="",null = True)
    payment_method = models.CharField(max_length = 1024,blank=True,default="",null = True)
    amount = models.FloatField(default=0.0,blank=True, null=True)
    intent = models.CharField(max_length = 1024,blank=True,default="",null = True)
    merchant_invoice_number = models.CharField(max_length = 1024,blank=True,default="",null = True)
    refund_amount = models.FloatField(default=0.0,blank=True, null=True)
    currency = models.CharField(max_length = 1024,blank=True,default="",null = True)
    payment_reference_id = models.CharField(max_length = 1024,blank=True,default="",null = True)



class Managers_list(models.Model):
    shop_id = models.IntegerField(blank=True,default=-1)
    warehouse_id = models.IntegerField(blank=True,default=-1)
    is_active = models.BooleanField(default=True)
    user_id = models.IntegerField(blank=True,default=-1)
    created_at = models.DateTimeField(auto_now_add=True)


class manager_inventory_status(models.Model):
    inv_rep_id = models.IntegerField(blank=False,default = -1)
    manager_approval = (
        ("Approved", "Approved"),
        ("Not Found", "Not Found"),
        ("Damaged", "Damaged"),
        ("Pending", "Pending"),
    )
    manager_status = models.CharField(choices=manager_approval, max_length=155, default ="Pending",blank=True, null = True)
    manager_id =  models.IntegerField(blank=False,default = -1)
    product_quantity = models.IntegerField(blank=True, null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank = True, null = True)




# class TransferRequest(models.Model):
#     date = models.DateTimeField(auto_now_add=True)
#     request_setter = models.CharField(max_length = 1024,blank=True,default="",null = True)
#     request_getter = models.CharField(max_length = 1024,blank=True,default="",null = True)
#     status_choices = (
#         ("Approved", "Approved"),
#         ("Pending", "Pending"),
#         ("Declined", "Declined"),
#         ("Partially Approved", "Partially Approved"),
#         )
#     status = models.CharField(choices= status_choices, max_length=155, default="Pending",blank=True)
#     is_active = models.BooleanField(blank=True, default=True)
#     requestee_user = models.IntegerField(blank=True,default = -1, null = True)
    
class TransferProductSpec(models.Model):
    transfer_id = models.IntegerField(blank=True, null = True)
    specification_id = models.IntegerField(blank=True, null = True)
    requested_qty = models.CharField(max_length = 1024,blank=True,default="",null = True)
    approved_qty = models.CharField(max_length = 1024,blank=True,default="",null = True)
    approved_user = models.IntegerField(blank=True,default = -1, null = True)


class TransferRequest(models.Model):
    date = models.DateField(auto_now_add=True)
    request_setter = models.CharField(max_length = 1024,blank=True,default="",null = True)
    request_getter = models.CharField(max_length = 1024,blank=True,default="",null = True)
    status_choices = (
        ("Approved", "Approved"),
        ("Pending", "Pending"),
        ("Declined", "Declined"),
        ("Partially Approved", "Partially Approved"),
        )
    status = models.CharField(choices= status_choices, max_length=155, default="Pending",blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    requestee_user = models.IntegerField(blank=True,default = -1, null = True)