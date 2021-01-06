import json
import requests
import base64
import datetime
import io
# import numpy as np
from rest_framework.decorators import api_view
from django.contrib import auth
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.translation import ugettext_lazy as _

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import filters
from rest_framework import viewsets
from Product_details.serializers import ProductDetailSerializer,ProductPriceSerializer,ProductPointSerializer,ProductDiscountSerializer
from Site_settings.serializers import ProductPdfSerializer
from io import BytesIO
from django.core.files import File
from Intense.models import Category, Product, GroupProduct , Variation,ProductPrice
# from user_profile.models import User
# from wand.image import Image 
from .serializers import (
        CategorySerializer, 
        ProductSerializer,
        ProductSerializer1,
        VariationSerializer,
        GroupProductSerialyzer,
        CreateProductSerializer,
        ProductImageSerializer,
        CommentSerializer,
        CommentReplySerializer,
        ReviewsSerializer,
        ProductReviewSerializer,
        ProductCodeSerializer,
        ScannerProductSerializer,
        AllGroupProductSerialyzer,
        SearchSerializer,
        SearchSerializer1,
        ProductAdminSerializer,
        ProductAdminSerializer1,
        InventorySerializer,
        SellerInfoSerializer,
        SellerInfoProductSerializer,
        ProductCodeSerializer,
        ProductPOSSerializer1,
        NewProductSerializer1,

        )


from .decorators import time_calculator
from Intense.models import (
    Comment,CommentReply,
    Reviews,Order,
    OrderDetails,
    User,
    GroupProduct, 
    Product, 
    Variation, 
    Category,
    discount_product,
    ProductImpression,
    ProductImage,
    ProductCode,
    ProductPrice,
    ProductPoint,
    ProductSpecification,
    Inventory_Price,
    WarehouseInfo,
    ShopInfo,
    CompanyInfo,
    Terminal

    )

from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView 
from User_details.serializers import UserSerializer
from django.db.models import Q
from django.utils import timezone
from django.db import transaction
from Intense.Integral_apis import (
    product_data_upload,category_data_upload,category1_data_upload,product_price_data_upload,
    product_specification_data_upload,product_point_data_upload,
    create_product_code,product_discount_data_upload,product_image_data_upload,product_data_update,price_update,
    discount_data_update,point_data_update,specification_data_update,group_product_data_update,group_product_data_modification
)
from io import BytesIO 
import barcode
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile
from PIL import Image
# import Image
import PIL
from django.conf import settings
import os
from django.utils import timezone
from django.contrib.sites.models import Site
from Product_details.serializers import get_id

# -------------------- Product -----------------------
@api_view(['POST',])
def insert_inventory(request,order_id):

    flag = 1

    try:

        specific_order = Order.objects.get(id=order_id)

    except:

        specific_order = None

    if specific_order:

        orderid = specific_order.id

        order_details = OrderDetails.objects.filter(order_id=orderid)
        order_details_ids = list(order_details.values_list('id',flat=True).distinct())
        print(order_details_ids)

        for i in range(len(order_details_ids)):

            print("ashtese")

            try:
                specific_order_details = OrderDetails.objects.get(id=order_details_ids[i])
            except:
                specific_order_details = None

            if specific_order_details:
                product_id = specific_order_details.product_id
                quantity = specific_order_details.total_quantity
                price = specific_order_details.unit_price
                date = ""

                product_color = specific_order_details.product_color
                product_size = specific_order_details.product_size

                try:
                    specification = ProductSpecification.objects.get(color=product_color,size=product_size,product_id=product_id)

                except:
                    specification = None

                if specification:
                    specification_id = specification.id

                else:
                    specification_id = 0

                data ={'product_id':product_id,'quantity':quantity,'price':price,'specification_id':specification_id,'date':'2020-09-05'}

                price_serializer = InventorySerializer(data = data)
                print(price_serializer)

                if price_serializer.is_valid():
                    price_serializer.save()
                    flag = 0 

                    

                else:
                    flag = 1
                    print(price_serializer.errors)

                    return JsonResponse({'success':False,'message':'Data could not be inserted'})


            else:

                return JsonResponse({'success':False,'message':'This product does not exist'})

        if flag==0:

            return JsonResponse({'success':True,'message':'Data has been inserted'})



    else:

        return JsonResponse({'success':False,'message':'This order does not exist'})




# @api_view(['GET',])
# def display_products(request,number):


#     latest = []
#     discount = []
#     popular = []
#     group=[]
#     current_date = timezone.now()
#     data = []


#     try:
        
#         latest_products = Product.objects.filter(is_deleted=False,product_status="Published").order_by('-date')
       
#         exit
#         #this fetches all the comment ids
#         print(latest_products)
        
#     except:
#         latest_products = None

#     if latest_products:

#         latest_products_serializer = ProductSerializer1(latest_products,many=True)
#         if(number>0):
#             latest = latest_products_serializer.data[:number]
#         else:
#             latest = latest_products_serializer.data

#     else: 

#         latest = []


#     if int(len(latest))>0:


#         dic1 = {'name':'New Arrivals','products':latest}
#         data.append(dic1)




    
#     try:
        
#         group_products = Product.objects.filter(is_group = True,is_deleted=False,product_status="Published").order_by('-date')
#         #this fetches all the comment ids
        
#     except:
#         group_products = None

   

#     if group_products:

#         group_products_products_serializer = ProductSerializer1(group_products,many=True)
#         if(number>0):
#             group = group_products_products_serializer.data[:number]
#         else:
#             group = group_products_products_serializer.data

#     else: 

#         group = []


#     if int(len(group)) > 0:

#         dic2 = {'name':'group Product','products':group}

#         data.append(dic2)
        



#     try:


#         # criterion1 = Q(start_date<=current_date)
#         # print(criterion1)
#         # criterion2 = Q(end_date>=current_date)
#         # print(criterion2)

#         product_discounts = discount_product.objects.filter(start_date__lte=current_date ,end_date__gte=current_date)

#     except:
#         product_discounts = None

#     if product_discounts:


#         discounted_product_ids = list(product_discounts.values_list('product_id',flat=True).distinct())
    
#         try:
            

#             discounted_products = Product.objects.filter(pk__in=discounted_product_ids, is_deleted=False,product_status="Published").order_by('-date')

#         except:

#             discounted_products = None


#         if discounted_products:

            

#             discounted_products_serializer = ProductSerializer1(discounted_products,many=True)
#             if(number>0):
#                 discount = discounted_products_serializer.data[:number]
#             else:
#                 discount = discounted_products_serializer.data

#         else:
            
#             discount = []

#     else:
#         discount = []


#     if int(len(discount))>0:

#         dic3 = {'name':'On Sale','products':discount}
#         data.append(dic3)



#     try:

#         popular_products =  ProductImpression.objects.order_by('-sales_count')
#         #print(popular_products)

#     except:

#         popular_products = None

#     print("impression")
#     print(popular_products)

#     if popular_products:

#         #Fetch the product ids 
#         product_ids = list(popular_products.values_list('product_id' , flat = True))
#         print("imression")


#         print(product_ids)


#         try:

#             pop_products = Product.objects.filter(pk__in = product_ids,is_deleted=False,product_status="Published")

#         except:

#             pop_products = None



#         print(pop_products)


#         if pop_products:


#             popular_products_serializer = ProductSerializer1(pop_products,many=True)
#             if(number>0):
#                 popular = popular_products_serializer.data[:number]
#             else:
#                 popular = popular_products_serializer.data

#         else:

#             popular = []

#     else:

#         popular = []


#     if int(len(popular)) > 0:

#         dic4 = {'name':'Popular','products':popular}
#         data.append(dic4)
  
#     # data = [{'name':'New Arrivals','products':latest},{'name':'On Sale','products':discount},{'name':'Popular','products':popular},
#     # {'name':'group Product', 'products':group}]



#     return Response({
#                 'success': True,
#                 'message': 'The values are shown below',
#                 'data': data 
#                 })


''' New display code (after optimization) '''
@api_view(['GET',])
def display_products(request,number):


    latest = []
    discount = []
    popular = []
    group=[]
    current_date = timezone.now()
    data = []
  
    latest_products = Product.objects.filter(is_deleted=False,product_status="Published").order_by('-date')
  

    if latest_products.exists():

        latest_products_serializer = NewProductSerializer1(latest_products,many=True)
        if(number>0):
            latest = latest_products_serializer.data[:number]
        else:
            latest = latest_products_serializer.data

    else: 

        latest = []

    if int(len(latest))>0:
        dic1 = {'name':'New Arrivals','products':latest}
        data.append(dic1)


   
    group_products = Product.objects.filter(is_group = True,is_deleted=False,product_status="Published").order_by('-date')
    #this fetches all the comment ids
        
    if group_products.exists():

        group_products_products_serializer = NewProductSerializer1(group_products,many=True)
        if(number>0):
            group = group_products_products_serializer.data[:number]
        else:
            group = group_products_products_serializer.data

    else: 

        group = []


    if int(len(group)) > 0:

        dic2 = {'name':'group Product','products':group}

        data.append(dic2)
        




        # criterion1 = Q(start_date<=current_date)
        # print(criterion1)
        # criterion2 = Q(end_date>=current_date)
        # print(criterion2)

    product_discounts = discount_product.objects.filter(start_date__lte=current_date ,end_date__gte=current_date)



    if product_discounts.exists():

        discounted_product_ids = list(product_discounts.values_list('product_id',flat=True).distinct())
    
     
        discounted_products = Product.objects.filter(pk__in=discounted_product_ids, is_deleted=False,product_status="Published").order_by('-date')

        if discounted_products.exists():

            discounted_products_serializer = NewProductSerializer1(discounted_products,many=True)
            if(number>0):
                discount = discounted_products_serializer.data[:number]
            else:
                discount = discounted_products_serializer.data

        else:
            
            discount = []

    else:
        discount = []


    if int(len(discount))>0:

        dic3 = {'name':'On Sale','products':discount}
        data.append(dic3)



    try:

        popular_products =  ProductImpression.objects.order_by('-sales_count')
        #print(popular_products)

    except:

        popular_products = None

    if popular_products:

        #Fetch the product ids 
        product_ids = list(popular_products.values_list('product_id' , flat = True))

        pop_products = Product.objects.filter(pk__in = product_ids,is_deleted=False,product_status="Published")
        if pop_products.exists():

            popular_products_serializer = NewProductSerializer1(pop_products,many=True)
            if(number>0):
                popular = popular_products_serializer.data[:number]
            else:
                popular = popular_products_serializer.data

        else:

            popular = []

    else:

        popular = []


    if int(len(popular)) > 0:

        dic4 = {'name':'Popular','products':popular}
        data.append(dic4)
  
    # data = [{'name':'New Arrivals','products':latest},{'name':'On Sale','products':discount},{'name':'Popular','products':popular},
    # {'name':'group Product', 'products':group}]



    return Response({
                'success': True,
                'message': 'The values are shown below',
                'data': data 
                })




@api_view(['POST',])
def show_more(request):


    latest = {}
    discount = {}
    popular = {}
    group={}
    current_date = timezone.now()

    name = request.data.get('name')


    try:
        
        latest_products = Product.objects.filter(is_deleted=False,product_status="Published").order_by('-date')
        #this fetches all the comment ids
        
    except:
        latest_products = None

   

    if latest_products:

        latest_products_serializer = NewProductSerializer1(latest_products,many=True)
     
        latest = latest_products_serializer.data

    else: 

        latest = {}

    
    try:
        
        group_products = Product.objects.filter(is_group = True,is_deleted=False,product_status="Published").order_by('date')
        #this fetches all the comment ids
        
    except:
        group_products = None

   

    if group_products:

        group_products_products_serializer = NewProductSerializer1(group_products,many=True)

        group = group_products_products_serializer.data

    else: 

        group = {}


    try:


        # criterion1 = Q(start_date<=current_date)
        # print(criterion1)
        # criterion2 = Q(end_date>=current_date)
        # print(criterion2)

        product_discounts = discount_product.objects.filter(start_date__lte=current_date ,end_date__gte=current_date)

    except:
        product_discounts = None

    if product_discounts:


        discounted_product_ids = list(product_discounts.values_list('product_id',flat=True).distinct())
    
        try:
            

            discounted_products = Product.objects.filter(pk__in=discounted_product_ids, is_deleted=False,product_status="Published")

        except:

            discounted_products = None


        if discounted_products:

            

            discounted_products_serializer = NewProductSerializer1(discounted_products,many=True)

            discount = discounted_products_serializer.data

        else:
            
            discount = {}

    else:
        discount = {}


    try:

        popular_products = ProductImpression.objects.order_by('-sales_count')
        #print(popular_products)

    except:

        popular_products = None

    if popular_products:

        #Fetch the product ids 
        product_ids = list(popular_products.values_list('product_id' , flat = True))

        try:

            pop_products = Product.objects.filter(pk__in = product_ids,is_deleted=False,product_status="Published")

        except:

            pop_products = None


        if pop_products:


            popular_products_serializer = NewProductSerializer1(pop_products,many=True)

            popular = popular_products_serializer.data

        else:

            popular = {}

    else:

        popular = {}
  
    # data = [{'name':'New Arrivals','products':latest},{'name':'On Sale','products':discount},{'name':'Popular','products':popular},
    # {'name':'group Product', 'products':group}]

    if name == "New Arrivals":
        data = [{'name': name,'products':latest}]

    elif name == "On Sale":
        data = [{'name': name,'products':discount}]

    elif name == "Popular":
        data = [{'name': name,'products':popular}]


    elif name == "group Product":
        data = [{'name': name,'products':group}]

    else:
        data = []

  





    return Response({
                'success': True,
                'message': 'The values are shown below',
                'data': data 
                })
class ListReviewView(ListAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("rating")
    filterset_fields = ['rating']
 
    
    @time_calculator
    def time(self):
        return 0

    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response ({
            'success': True,
            'message': "Data has been retrived successfully",
            'data': serializer
            })
  

      


class ListProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = SearchSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("title",'brand')
    filterset_fields = ['title', 'brand']

    @time_calculator
    def time(self):
        return 0

    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response ({
            'success': True,
            'message': "Data has been retrived successfully",
            'data': serializer.data
        })



@api_view (["GET","post"])
def get_searched_product(request,name):
    
    # if 'brand' in request.GET:
    #     print("yessssss")
    #     my_brand = request.GET['brand']
    # else:
    #     my_brand = ''
    response_data = []
    queryset = Product.objects.filter(title__icontains=name,product_status="Published")
    product_brands = list(queryset.values_list('brand',flat=True).distinct())

    if 'brand' in request.GET:
        my_brand = request.GET['brand']
        queryset = queryset.filter(brand=my_brand)
    else:
        my_brand =''

    print(my_brand)

    
    product_serializers = SearchSerializer1(queryset, many= True)
    response_data = product_serializers.data

    rating_data = []
    if 'ratings' in request.GET:
        print("rating ey dhukse")
        my_ratings = request.GET['ratings']
        rating_list = [1,2,3,4,5]
        for pro in response_data:
            for key, value in pro.items(): 
                if(key=='ratings' and value):
                    if(value['average_ratings']>= float(my_ratings)):
                        rating_data.append(pro)

        response_data = rating_data


        # if (rating_data):
        #     print("rating ase")

        #     response_data = rating_data


    price_data = []

    if 'max_price' or 'min_price' in request.GET:
        print("price ey dhukse")
        if 'max_price' in request.GET:
            max_price = request.GET['max_price']

        else:
            max_price = 100000000 

        if 'min_price' in request.GET:
            min_price = request.GET['min_price']

        else:
            min_price = 0


        for pro in response_data:
            for key, value in pro.items(): 
                if(key=='new_price' and value):
                    print(min_price)
                    if((float(value) >= float(min_price)) and (float(value) <= float(max_price))):
                        price_data.append(pro)

        response_data = price_data


        # if (price_data):

        #     print("price ase")

        #     response_data = price_data


    return Response ({
                'success': True,
                'message' : "data has been retrived successfully",
                'brand' : product_brands,
                'data' : response_data
                })
 

@api_view (["GET",])
def approved_products(request,user_id):


    try:

        products = Product.objects.filter(seller=user_id,product_admin_status="Confirmed").order_by('-date')

    except:

        products = None


    if products:

        product_serializer = ProductAdminSerializer1(products,many=True)

        return JsonResponse({'success':True,'message':'Data is shown','data':product_serializer.data})


    else:


        return JsonResponse({'success':False,'message':'Data is not shown','data': []})






@api_view (["GET",])
def pending_products(request,user_id):


    try:

        products = Product.objects.filter(seller=user_id,product_admin_status="Processing").order_by('-date')

    except:

        products = None


    if products:

        product_serializer = ProductAdminSerializer1(products,many=True)

        return JsonResponse({'success':True,'message':'Data is shown','data':product_serializer.data})


    else:


        return JsonResponse({'success':False,'message':'Data is not shown','data': []})




@api_view (["GET",])
def cancelled_products(request,user_id):


    try:

        products = Product.objects.filter(seller=user_id,product_admin_status="Cancelled").order_by('-date')

    except:

        products = None


    if products:

        product_serializer = ProductAdminSerializer1(products,many=True)

        return JsonResponse({'success':True,'message':'Data is shown','data':product_serializer.data})


    else:


        return JsonResponse({'success':False,'message':'Data is not shown','data': []})





@api_view (["GET",])
def all_products(request,user_id):


    try:

        products = Product.objects.filter(seller=user_id).order_by('-date')

    except:

        products = None


    if products:

        product_serializer = ProductAdminSerializer1(products,many=True)

        return JsonResponse({'success':True,'message':'Data is shown','data':product_serializer.data})


    else:


        return JsonResponse({'success':False,'message':'Data is not shown','data': []})





#This shows all the seller products
@api_view (["GET","post"])
def get_all_products(request):


    try:

        products = Product.objects.filter(is_own=True)

    except:

        products = None 


    if products:


        seller_ids = list(products.values_list('seller',flat=True).distinct())

        seller_ids.remove(-1)


    else:

        seller_ids = []


    try:

        seller_products = Product.objects.filter(seller__in=seller_ids).order_by('-date')

    except:

        seller_products = None


    if seller_products:


        product_serializer = ProductAdminSerializer1(seller_products,many=True)

        return JsonResponse({'success':True,'message':'Data is shown','data':product_serializer.data})



    else:


        return JsonResponse({'success':True,'message':'Data is shown','data':[]})



@api_view (["GET","post"])
def get_all_product(request):

 #"This api is for view all Product informations"
    if (request.method == "GET"):
        queryset = Product.objects.filter(is_own=True).order_by('-date')
        print(queryset)
        product_serializers = ProductPdfSerializer(queryset , many = True)
        return Response (product_serializers.data)



@api_view (["GET",])
def shared_products(request):

    try:
        product = Product.objects.filter(properties=True).order_by('-date')

    except:

        product = None

    if product:

        product_serializer = ProductAdminSerializer1(product,many=True)
        return JsonResponse({'success':True,'message':'The products are shown','data':product_serializer.data})

    else:

        return JsonResponse({'success':False,'messsage': 'No product is shared with the mother site'})



@api_view (["GET",])
def unshared_products(request):

    try:
        product = Product.objects.filter(properties=False).order_by('-date')

    except:

        product = None

    if product:

        product_serializer = ProductAdminSerializer1(product,many=True)
        return JsonResponse({'success':True,'message':'The products are shown','data':product_serializer.data})

    else:

        return JsonResponse({'success':False,'messsage': 'No product is shared with the mother site'})



@api_view (["GET",])
def unpublished_products(request):

    try:
        product = Product.objects.filter(product_status="Pending").order_by('-date')

    except:

        product = None

    if product:

        product_serializer = ProductAdminSerializer1(product,many=True)
        return JsonResponse({'success':True,'message':'The products are shown','data':product_serializer.data})

    else:

        return JsonResponse({'success':False,'messsage': 'No product is shared with the mother site'})

@api_view (["GET",])
def get_product_info(request,product_id):


    try:

        product = Product.objects.get(id=product_id)

    except:

        product = None 


    if product:

        product_serializers = ProductAdminSerializer1(product, many = False)

        return JsonResponse({'success':True,'message':'data is shown below','data':product_serializers.data})


    else:


        return JsonResponse({'success':False,'message':'This product does not exist','data':[]})




@api_view (["GET" , "POST"])
#"This api is for view create  product.  "
def insert_specific_product_value(request):
    if(request.method == "POST"):
        product_serializers=ProductSerializer(data=request.data)
        if(product_serializers.is_valid()):
            product_serializers.save()
            return Response (product_serializers.data, status=status.HTTP_201_CREATED)
        return JsonResponse(product_serializers.errors)

@api_view(["GET","POST"])
def get_update_product_value(request , product_id):

    try:
        product = Product.objects.get(id=product_id)
        if request.method == 'POST':
            serializers = ProductSerializer(product , data=request.data )
            if serializers.is_valid():
                serializers.save()
                return JsonResponse(serializers.data)
            return JsonResponse(serializers.errors)

    except Product.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST','GET'])
def delete_product_value(request ,product_id):
    '''
  This is for delete a specific Product
    ''' 
    try:
        product = Product.objects.filter(id =product_id)
    except:
        product = None

    if product is not None:
        product.delete()
        return JsonResponse({'message': 'Product was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({'message': 'Product was deleted successfully!'})

# ------------------------- Product Image ---------------------------------

@api_view (["GET" , "POST"])
def product_image_up(request):
    if(request.method == "POST"):
        try:
            values_data = request.data
            #print(values_data['image'])
            
            serializers=ProductImageSerializer(data=request.data)
            if(serializers.is_valid()):
                serializers.save()
                return Response (serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors)
        except:
            return Response ({
                'success': False,
                'message': 'Some Internal problem occurs'
                        })

@api_view (["GET","post"])
def get_all_product_image(request):

    if (request.method == "GET"):
        try:
            queryset = ProductImage.objects.all()
            serializers = ProductImageSerializer(queryset , many = True)
            return Response (serializers.data)
        except:
            return Response({
                'success': False,
                'message': 'Some problem occurs while retriveing the data'
            })

@api_view (["GET","post"])
def get_specific_product_image(request, image_id):

    if (request.method == "GET"):
        try:
            queryset = ProductImage.objects.get(id = image_id)
            serializers = ProductImageSerializer(queryset , many = False)
            return Response (serializers.data)
        except:
            return Response({
                'success': False,
                'message': 'Requested data can not be found'
            })

@api_view(["GET","POST"])
def update_product_image_value(request, image_id):

    try:
        product_img = ProductImage.objects.get(id=image_id)
    except:
        return JsonResponse({'message': 'Image does not exists'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            serializers = ProductImageSerializer(product_img , data=request.data )
            if serializers.is_valid():
                serializers.save()
                return JsonResponse(serializers.data)
            return JsonResponse(serializers.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view (["GET","post"])
def delete_specific_product_image(request, image_id):

    if (request.method == "POST"):
        try:
            queryset = ProductImage.objects.get(id = image_id)
            queryset.delete()
            return Response ({'Message': ' data has been deleted successfully'})
        except:
            return Response ({
                'success': False,
                'Message': 'Data could not be deleted'})

@api_view (["GET","post"])
def get_all_product_category(request):

    if (request.method == "GET"):
        queryset = Category.objects.all()
        serializers = CategorySerializer(queryset , many = True)
        return Response (serializers.data)

@api_view (["GET" , "POST"])
def insert_specific_category_value(request):
    if(request.method == "POST"):
        serializers=CategorySerializer(data=request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response (serializers.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializers.errors)


@api_view(["GET","POST"])
def get_update_category_value(request, category_id):

    try:
        product = Category.objects.get(id=category_id)
        if request.method == 'POST':
            serializers = CategorySerializer(product , data=request.data )
            if serializers.is_valid():
                serializers.save()
                return JsonResponse(serializers.data)
            return JsonResponse(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return JsonResponse({'message': 'This Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['POST','GET'])
def delete_category_value(request , category_id):

    try:
        category = Category.objects.filter(id =category_id)
    except:
        category = None

    if category is not None:
        category.delete()
        return JsonResponse({'message': 'Category was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({'message': 'Category was not deleted successfully!'})



@api_view (["GET","post"])
def get_all_group_product(request):
 
    if (request.method == "GET"):
        queryset = GroupProduct.objects.all()
        serializers = GroupProductSerialyzer(queryset , many = True)
        return Response (serializers.data)

@api_view (["GET" , "POST"])
def insert_specific_group_product_value(request):

  

    if(request.method == "GET"):
        return Response({''})

    if(request.method == "POST"):
        serializers=GroupProductSerialyzer(data=request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response (serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors)

@api_view(["GET","POST"])
def get_update_group_product_value(request , product_id):
   
    try:
        product = GroupProduct.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'This Group does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializers = GroupProductSerialyzer(product , many = False)
        return Response (serializers.data)
    if request.method == 'POST':
        serializers = GroupProductSerialyzer(product , data=request.data )
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data)
        return JsonResponse(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    


@api_view(['POST','GET'])
def delete_group_product_value(request, gp_id):
    '''
   
    ''' 
    try:
        product = GroupProduct.objects.filter(id=gp_id)
    except:
        product = None

    if product is not None:
        product.delete()
        return JsonResponse({'message': 'Your Group Product was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({'message': 'Group Product was deleted successfully!'})



#------------Product comments and reviews----------------------------

#Display the comments and replies of a specific product of a specific product
@api_view(['GET',])
def comments_product(request,product_id):

    try:
        title = Product.objects.get(id=product_id)
    except:
        title = None
    if title:
        product_title = title.title
    else:
        product_title = ''

    try:
        product_images = ProductImage.objects.filter(product_id = product_id)

    except:

        product_images = None


    if product_images:
        print("ashtese")
        images = list(product_images.values_list('image_url' , flat = True))
            # images=[] 
            # for i in range(len(image_ids)):
            #     images += product_images.image


    else:
        images=[]


    try:

        comments = Comment.objects.filter(product_id = product_id)

    except:

        comments = None


    if comments:

        commentserializer = CommentSerializer(comments , many=True)
        return JsonResponse({'success':True,'message':'Comment data is shown','product_title': product_title,'images': images , 'data':commentserializer.data}, safe=False)

    else:

        return JsonResponse({'success':False,'message':'Comment data cannot be shown','product_title': product_title,'images': images ,'data':[]}, safe=False)






# @api_view(['GET',])
# def comments(request,product_id):

#   try:
#       comments = Comment()
#       comments.product_id = product_id
#       comments = Comment.objects.filter(product_id = product_id).first()
#       if request.method == 'GET':
#           commentserializer = CommentSerializer(comments)
#           return JsonResponse(comments,safe= False)

#   except Comment.DoesNotExist:
#       return JsonResponse({'message': 'This comment does not exist'}, status=status.HTTP_404_NOT_FOUND)








#This creates a comment
@api_view(['POST',])
def create_comment(request):

    if request.method == 'POST':
        commentserializer = CommentSerializer(data=request.data)
        if commentserializer.is_valid():
            commentserializer.save()
            return JsonResponse(commentserializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(commentserializer.errors)

User = get_user_model()
#This creates a reply
@api_view(['POST',])
def create_reply(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id =0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            
            names = User.objects.filter(id=user_id).last()
         
            
            
        except:
            names = None

        if names is not None:

            
            reply_name = str(names.username)

            reply = CommentReply.objects.create(name = reply_name)
            reply.save()
            replyserializer = CommentReplySerializer(reply,data=request.data)
            if replyserializer.is_valid():
                replyserializer.save()
                return JsonResponse(replyserializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(replyserializer.errors)

        else:
            
            replyserializer = CommentReplySerializer(data=request.data)
            if replyserializer.is_valid():
                replyserializer.save()
                return JsonResponse(replyserializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(replyserializer.errors)

    else:
        name = "Anonymous"
        reply = CommentReply.objects.create(name = name)
        reply.save()
        replyserializer = CommentReplySerializer(reply,data=request.data)
        if replyserializer.is_valid():
            replyserializer.save()
            return JsonResponse(replyserializer.data, status=status.HTTP_201_CREATED)









#This edits an existing comment
@api_view(['POST',])
def edit_comment(request,comment_id):

    try:
        comment = Comment.objects.get(pk = comment_id)
        if request.method == 'POST':
            commentserializer = CommentSerializer(comment , data=request.data )
            if commentserializer.is_valid():
                commentserializer.save()
                return JsonResponse(commentserializer.data)
            return JsonResponse(commentserializer.errors)


    except Comment.DoesNotExist:
        return JsonResponse({'message': 'This comment does not exist'}, status=status.HTTP_404_NOT_FOUND)



#This edits a reply
@api_view(['POST',])
def edit_reply(request,reply_id):

    try:
        reply = CommentReply.objects.get(pk = reply_id)
        if request.method == 'POST':
            replyserializer = CommentReplySerializer(reply , data=request.data )
            if replyserializer.is_valid():
                replyserializer.save()
                return JsonResponse(replyserializer.data)
            return JsonResponse(replyserializer.errors)

                
    except CommentReply.DoesNotExist:
        return JsonResponse({'message': 'This reply does not exist'}, status=status.HTTP_404_NOT_FOUND)


#This deletes all the comments and the replies of that comment 
@api_view(['POST',])
def delete_comment(request,comment_id):

    try:
        comment = Comment.objects.filter(id = comment_id)
        replies = CommentReply.objects.filter(comment_id = comment_id)
        if request.method == 'POST':
            comment.delete()
            replies.delete()
            return JsonResponse({'message': 'The comment and its replies were deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)




    except Comment.DoesNotExist:
        return JsonResponse({'message': 'This comment does not exist'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST',])
def delete_reply(request,reply_id):

    try:
        
        replies = CommentReply.objects.filter(id = reply_id)
        if request.method == 'POST':
            
            replies.delete()
            return JsonResponse({'message': 'The reply was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)




    except Comment.DoesNotExist:
        return JsonResponse({'message': 'This reply does not exist'}, status=status.HTTP_404_NOT_FOUND)


#Fetches all the reviews of a certain product   
@api_view(['GET',])
def reviews_product(request,product_id):


    try:
        title = Product.objects.get(id=product_id)
    except:
        title = None
    if title:
        product_title = title.title
    else:
        product_title = ''

    try:
        reviews = Reviews.objects.filter(product_id = product_id)
    except:
        reviews = None

    if reviews:
        reviewsserializer = ReviewsSerializer(reviews,many=True)
        return JsonResponse({'success':True,'message':'Data is shown','product_title':product_title,'data':reviewsserializer.data}, safe=False)


        

    else:
        return JsonResponse({'success':False,'message':'Data is not available','product_title':product_title,'data':[]}, safe=False)



     


 



#This creates a review
@api_view(['POST',])
def create_review(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    product_id = request.data.get('product_id')
    product_id = int(product_id)
    print(product_id)
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id =0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:
        #The user is a verified user 

        #checking if the user has purchased the following product

        #Checking if orders exist of this user 
        flag = True
    
        
        try: 
            orders = Order.objects.filter(user_id=user_id,checkout_status=True,delivery_status="Received",order_status="Paid")
            
        except:
            orders = None

        if orders is not None:
            
            order_ids = orders.values_list('id' , flat = True)
            
            for i in range(len(order_ids)):
                orderdetails = OrderDetails.objects.filter(order_id=order_ids[i],is_removed=False)
                product_ids = orderdetails.values_list('product_id',flat= True)
                

                
                if (product_id in product_ids):
                    flag = False
                    break

            if flag == True:
                
                return JsonResponse({'success':False,'message': 'You cant review this product because you din not buy it'})

            else:
                
                reviewserializer = ReviewsSerializer(data=request.data)
                if reviewserializer.is_valid():
                    reviewserializer.save()
                return JsonResponse({'success': True, 'data':reviewserializer.data})


        else:
            return JsonResponse({'success':False,'message': 'You cant review this product because you din not buy it'})

    else:   


        flag = True
    
        
        try: 
            orders = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True,delivery_status="Received",order_status="Paid")

        except:
            orders = None

        if orders is not None:
            order_ids = orders.values_list('id' , flat = True)
            for i in range(len(order_ids)):
                orderdetails = OrderDetails.objects.filter(order_id=order_ids[i],is_removed=False)
                product_ids = orderdetails.values_list('product_id',flat= True)
                if (product_id in product_ids):
                    flag = False
                    break

            if flag == True:
                return JsonResponse({'message': 'You cant review this product because you din not buy it'})

            else:
                reviewserializer = ReviewsSerializer(data=request.data)
                if reviewserializer.is_valid():
                    reviewserializer.save()
                return JsonResponse({'success': True, 'data':reviewserializer.data})

        else:
            return JsonResponse({'success':False,'message': 'You cant review this product because you din not buy it'})


        

        
#This edits an existing review
@api_view(['POST',])
def edit_review(request,review_id):

    try:
        reply = Reviews.objects.get(pk= review_id)
    except:
        reply = None
    if reply is not None:

        replyserializer = ReviewsSerializer(reply , data=request.data )
        if replyserializer.is_valid():
            replyserializer.save()
            return JsonResponse(replyserializer.data)
        return JsonResponse(replyserializer.errors)
        
     

    else:
        return JsonResponse({'message': 'The review does not exist!'})


                
    
        

#This deleted a review
@api_view(['POST',])
def delete_review(request,review_id):

    try:
        
        reviews = Reviews.objects.filter(id = review_id)
        if request.method == 'POST':
            
            reviews.delete()
            return JsonResponse({'message': 'The review was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)




    except Reviews.DoesNotExist:
        return JsonResponse({'message': 'This review does not exist'}, status=status.HTTP_404_NOT_FOUND)

# ------------------------------- Product Code -------------------------

@api_view (["GET","POST"])
def get_specific_code_values(request,product_id,height,width):
    '''
    This Api is for getting an individual product code. Calling http://127.0.0.1:8000/code/value/product_id/150/250
    will cause to invoke this API. While getting values, user may specify the image size in which user expects it. This value need to be passed
    as a parameter.

        GET Response:
            While performing get response this API will give a JSON response. As a response it will provide the following data.
            Barcode_img : (barcode will be an image. While retreiving, this will be the url of the barcode image.)
            Date : (This is the date on wchich the product code is been created.)
            Barcode : This will be the product barcode. Based on this later, the product can be found.
    '''
  

    if(request.method == "GET"):
        try:
            queryset = ProductCode.objects.get(product_id = product_id)
            resized = Image.open(queryset.Barcode_img) 
            newSize = (width , height )
            # Getting barcode url and before retreiving it resizes the barcode as per the user specification
            resized = resized.resize(newSize, resample=PIL.Image.NEAREST)
            resized.save(settings.MEDIA_DIR+'/barcode/'+ str(product_id)+'.png')
            url = settings.MEDIA_DIR+'/barcode/' + str(product_id)+'.png'
            code_serializers = ProductCodeSerializer (queryset, many = False)
            return Response (code_serializers.data)
        except:
            return Response({'message': 'Thre is no value to retrive'})

@api_view (["GET","POST"])
def insert_specific_code_values(request):
    '''
    This is for creating barcode for a particular product and insert it into the database. Calling http://127.0.0.1:8000/code/insert_value/ will 
    cause to invoke this API. This api has just post response.

    POST Response:
        While performing post response this api requires just the product id. Based on that product id this api will generate the product code 
        and will save the code as an image data into the media folder. At a same time it will store the image url into database Barcode field.
    
    '''
    if request.method == "POST":
        # demo values
        values = request.data
        your_domain = Site.objects.get_current().domain
    
        bar = barcode.get_barcode_class('code39')
        bar_value = bar(your_domain+str(values['product_id']), writer = ImageWriter())
        if not os.path.exists(settings.MEDIA_DIR+'/barcode/'):
            os.makedirs(settings.MEDIA_DIR+'/barcode/')
        bar_value.save(settings.MEDIA_DIR+'/barcode/'+ str(values['product_id']))
        url = settings.MEDIA_DIR+'/barcode/' + str(values['product_id'])+'.png'

        data_values  = {'product_id' : values['product_id'], 'Barcode_img' : url, 'Barcode' : your_domain+str((values['product_id'])) }

        code_serializer_value = ProductCodeSerializer (data= data_values)
        if(code_serializer_value.is_valid()):
            code_serializer_value.save()
            return Response (code_serializer_value.data, status=status.HTTP_201_CREATED)
        return Response (code_serializer_value.errors)

# @api_view (["GET","POST"])
# def insert_specific_code_values(request):
#     '''
#     This is for creating barcode for a particular product and insert it into the database. Calling http://127.0.0.1:8000/code/insert_value/ will 
#     cause to invoke this API. This api has just post response.

#     POST Response:
#         While performing post response this api requires just the product id. Based on that product id this api will generate the product code 
#         and will save the code as an image data into the media folder. At a same time it will store the image url into database Barcode field.
    
#     '''
#     if request.method == "POST":
#         # demo values
#         values = request.data
#         your_domain = Site.objects.get_current().domain

#         bar = barcode.get_barcode_class('code39')
#         bar_value = bar(str(values['product_id']), writer = ImageWriter())

#         if not os.path.exists(settings.MEDIA_DIR+'/barcode/'):
#             os.makedirs(settings.MEDIA_DIR+'/barcode/')
#         bar_value.save(settings.MEDIA_DIR+'/barcode/'+ str(values['product_id']))
#         url = settings.MEDIA_DIR+'/barcode/' + str(values['product_id'])+'.png'

#         data_values  = {'product_id' : values['product_id'], 'Barcode_img' : url, 'Barcode' : str((values['product_id'])) }

#         code_serializer_value = ProductCodeSerializer (data= data_values)
#         if(code_serializer_value.is_valid()):
#             code_serializer_value.save()
#             return Response (code_serializer_value.data, status=status.HTTP_201_CREATED)
#         return Response (code_serializer_value.errors)


@api_view (["GET","POST"])
def specific_code_delete(request):
    '''
    This Api is for deleting a particular product value. While performing the delete operation it expects a particualr product id. 
    Calling http://127.0.0.1:8000/code/delete_value/ will cause to invoke this API.
    '''
    #demo value
    values = {'product_id': '12'}

    try:
        specific_data = ProductCode.objects.get(product_id = values['product_id'])
    except :
        return Response({'message': 'There is no value to delete'})
    
    if request.method == "POST":
        specific_data.delete()
        os.remove(specific_data.Barcode_img)
        return Response({'message': ' Value is successfully  deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view (["GET","POST"])
def get_product_using_barcode (request,scanned_code):
    '''
    This API is for getting product id condition on passing scanned value as a parameters. This will be required while scanner will send the scanned barcode.
    Based on the scanned code this Api will provide corresponding product Id. Calling http://127.0.0.1:8000/code/scanned_value/12/ will cause to invoke this ApI.
    This will have just Get response.

    Get Response:
    Followings data will be provided while performing the get response.
    scan_product_id : This will be the product id which was scanned through the scanner. This product id will be required later to find the product details.
    date : The date on which the product barcode was created.
    '''

    if request.method == 'GET':
        try:
            specific_data = ProductCode.objects.get(Barcode = scanned_code)
            data_serializers = ScannerProductSerializer (specific_data)
            return Response (data_serializers.data)
        except:
            return Response({'message': 'There is no value'})


#This api is used to get the total rating count for a product,the average rating and how much of each rating does this product have
@api_view(['GET',])
def product_ratings(request,product_id):

    try:
        product = Reviews.objects.filter(product_id=product_id).first()
    except:
        product = None

    if product is None:
        return JsonResponse({})

    else:

        productserializer = ProductReviewSerializer(product,many=False)
        return JsonResponse(productserializer.data,safe=False)

   


@api_view(['POST',])
def upload_product(request):

    # arr={
    #     "seller_id": "18",
    #     "title": "Samsung360",
    #     "description": "This is a good product",
    #     "quantity": "3",
    #     "brand": "Samsung",
    #     "key_feature": ["This is a good product","Nice nice","good good"],
        
    #     }

    # data = request.data
    # title = data['title']
    # description = data['description']
    # brand = data['brand']
    # key_feature = data['key_feature']


    # product = Product.objects.create(title=title,description=description,brand=brand)

    # product.save()
    # product.



    product_serializer = CreateProductSerializer(data=request.data)
    if product_serializer.is_valid():
        product_serializer.save()
        return JsonResponse(product_serializer.data)
    return JsonResponse(product_serializer.errors)



@api_view(['POST',])
def edit_product(request,product_id):

    try:

        product = Product.objects.filter(id= product_id).last()

    except:
        product = None

    if product is not None:

        product_serializer = CreateProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(product_serializer.data)
        return JsonResponse(product_serializer.errors)

    else:
        JsonResponse({'message': 'This product does not exist'})



@api_view(['POST',])
def specific_product_update(request,product_id):
    if request.method == 'POST':
        product_data = Product.objects.get(id = product_id)
        product_serializer = CreateProductSerializer(product_data, data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(product_serializer.data)
        return JsonResponse(product_serializer.errors)


@api_view(['GET',])
def all_product_detail(request):

    product = Product.objects.all()
    product_serializer = ProductDetailSerializer(product,many= True)
    return JsonResponse({'success':True,'message':'The data is shown below','data':product_serializer.data},safe=False)
    

    # else:
    #   return JsonResponse({'success':False,'message':'This product does not exist','data':''}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST','GET'])
def product_insertion_admin(request):

    # print(request.data)
    data = request.data
    # data = request.body
    # print(data)



    

    # im = data['images']

    # print(len(data))
    print(data)

    count = len(data)-19
    # print(count)
    print(count)
    print(len(data))

    # print(request.data.get("Warranty"))

    key_features = request.data.get("key_features")
    # print(key_features)
    user_id = request.data.get("user_id")
    user_role = request.data.get("user_role")


    # print(key_features)
    # print(key_features)

    
    # li = list(key_features.split(",")) 
    # print(li)
    
    # key_feature = key_features.split(",")
    features = []
    # for i in range(len(key_feature)):
    #     print(key_feature[i])
    #     features.append(key_feature[i])
   
    date = timezone.now().date()

    # print(request.data['brand'])


  


    if key_features is not None:
        features = key_features.split(",")
    # print(features)

    if user_role == "Seller":
  
        product_data_value ={

            
            'seller': request.data.get("user_id"),
            'product_admin_status': 'Processing',
            'title': request.data.get("title"),
            'brand': request.data.get("brand"),
            'description':request.data.get("description"),
            'warranty':request.data.get("Warranty"),
            'origin':request.data.get("origin"),
            'shipping_country':request.data.get("shipping_country"),
            'unit':request.data.get("unit"),
            'key_features':features,
            'is_deleted': False,
            'properties': request.data.get("properties")
        }


    else:

        product_data_value ={

            
            
            'product_admin_status': 'Confirmed',
            'title': request.data.get("title"),
            'brand': request.data.get("brand"),
            'description':request.data.get("description"),
            'warranty':request.data.get("Warranty"),
            'origin':request.data.get("origin"),
            'shipping_country':request.data.get("shipping_country"),
            'unit':request.data.get("unit"),
            'key_features':features,
            'is_deleted': False,
            'properties': request.data.get("properties")
        }


    category_data_value ={

            
            'category': request.data.get("category"),
            'sub_category': request.data.get("sub_category"),
            'sub_sub_category': request.data.get("sub_sub_category")
        }


   
    product_price ={
        'price' : request.data.get("price"),
        'purchase_price': request.data.get("purchase_price"),
        #'currency_id': request.data.get('currency_id')
    }

    # product_specification= [
    #     {
    #     "weight": request.data.get('weight'),
    #     "color":request.data.get('color'),
    #     "size":request.data.get('size'),
    #     'quantity': request.data.get('quantity')
    #    },
    #     {
        
    #     "color":'Green',
    #     "size":'Large',
    #     'quantity': 20
    #    },
    #     {
        
    #     "color":'Blue',
    #     "size":'XXL',
    #     'quantity': 7
    #    }
    # ]




    product_point ={
        'point': request.data.get("point"),
        # 'end_date': data['point_end_date']
        'end_date': request.data.get("point_end_date")
    }

    product_discount ={

        'amount': request.data.get("amount"),
        #'start_date' : '2020-09-05',
        #'end_date' : data['discount_end_date']
        'end_date': request.data.get("discount_end_date")
    }

    # product_image=[
        
    #          'This is image 1', 'This is image 2', 'This is image 3', 'This is image 4'
    # ]

 

    if request.method == 'POST':
        
        try:
            #print("dbcudbfdbcducbducbducbducbd")
            category_values= category1_data_upload (category_data_value)
            #print(category_values)
            category_data = category_values.json()
            #print(category_data)
            category_id = category_data['category']
            sub_category_id = category_data['sub_category']
            sub_sub_category_id = category_data['sub_sub_category']
            product_data_value.update( {'category_id' : category_id,'sub_category_id' : sub_category_id,'sub_sub_category_id' : sub_sub_category_id} )
            product_values= product_data_upload (product_data_value)
            product_data= product_values.json()
            product_id = product_data['id']
            product_price.update( {'product_id' : product_id} )
            price_values = product_price_data_upload (product_price)
            product_point.update ({'product_id' : product_id})
            point_values = product_point_data_upload(product_point)
            product_code = create_product_code({'product_id' : product_id})
            product_discount.update({'product_id' : product_id})
            discount_data = product_discount_data_upload(product_discount)

            for i in range(int(count)):

                print("dhuklam")
                print("tarpor")

                dataz = request.data
                image = dataz['images['+str(i)+']']

                # print(dataz['images['+str(i)+']'])




                

                print("image")
                print(image)
                
                image_data = {'product_image':image,'product_id':product_id}
                product_image = ProductImage.objects.create(product_image=image,product_id=product_id)
                #product_image.save()
                product_image_serializer = ProductImageSerializer(product_image,data=image_data)

                if product_image_serializer.is_valid():

                    print("image save hochche")


                    
                    product_image_serializer.save()
                    

                else:
                    print("Image save hochche na")
                    print(product_image_serializer.errors)
                    
            # product_img =[]
            # product_spec=[]
            # for img in product_image:
            #     data = {'content':img}
            #     data.update({'product_id' : product_id})
            #     img_data= product_image_data_upload(data)
            #     product_img.append(img_data.json())


            # for spec in product_specification:
            #     spec.update({'product_id' : product_id})            
            #     product_sp = product_specification_data_upload (spec)
            #     product_spec.append(product_sp.json())
        
            return Response({
                
                'success': True,
                'product_data': product_data,
                # 'price_values': price_values.json(),
                # #'product_specification': product_spec,
                # 'product_point': point_values.json(),
                # 'product_code': product_code.json(),
                # 'product_discount': discount_data.json(),
                # 'product_image': product_img
            }) 
        except:

            # product_price = ProductPrice.objects.filter(product_id = product_id)
            # if product_price.exists():
            #     product_price.delete()

            # product_discount = discount_product.objects.filter(product_id = product_id)
            # if product_discount.exists():
            #     product_discount.delete()

            # product_code = ProductCode.objects.filter(product_id = product_id)
            # if product_code.exists():
            #     product_code.delete()

            # product_point = ProductPoint.objects.filter(product_id = product_id)
            # if product_point.exists():
            #     product_point.delete()

            # product_specification = ProductSpecification.objects.filter(product_id = product_id)
            # if product_specification.exists():
            #     product_specification.delete()
            
            product_image = ProductImage.objects.filter(product_id = product_id)
            if product_image.exists():
                product_image.delete()
            
            product_value = Product.objects.filter(id = product_id)
            if product_value.exists():
                product_value.delete()
            
            return Response({
                'success': False,
                'message': 'Product insertion could not be completed'
                })


def make_thumbnail(image, size=(100, 100)):
    """Makes thumbnails of given size from given image"""

    im = Image.open(image)

    im.convert('RGB') # convert mode

    im.crop((0,0,470,470)) # resize image

    thumb_io = BytesIO() # create a BytesIO object

    im.save(thumb_io, 'JPEG', quality=85) # save image to BytesIO object

    thumbnail = File(thumb_io, name=image.name) # create a django friendly File object

    return thumbnail



    
 
@api_view(['POST','GET'])
def product_insertion_admin1(request):
    # print(request.data)
    data = request.data
    # data = request.body
    # print(data)
    print(request.data.get("count"))
    # im = data['images']
    # print(len(data))
    # print(data)
    count = request.data.get("count")
    # print(count)
    print(count)
    print(len(data))
    # print(request.data.get("Warranty"))
    key_features = request.data.get("key_features")
    # print(key_features)
    user_id = request.data.get("user_id")
    user_role = request.data.get("user_role")
    product_status = request.data.get("publish")
    if product_status:

        if product_status == "Published":
            product_status = "Published"

        elif product_status == "Pending":
            product_status = "Pending"

    else:
        product_status = "Pending"

    # print(key_features)
    # print(key_features)
    # li = list(key_features.split(",")) 
    # print(li)
    # key_feature = key_features.split(",")
    features = []
    # for i in range(len(key_feature)):
    #     print(key_feature[i])
    #     features.append(key_feature[i])
    date = timezone.now().date()
    # print(request.data['brand'])
    if key_features is not None:
        features = key_features.split(",")
    # print(features)
    if user_role == "Seller":
        product_data_value ={
            'seller': request.data.get("user_id"),
            'product_admin_status': 'Processing',
            'title': request.data.get("title"),
            'brand': request.data.get("brand"),
            'description':request.data.get("description"),
            #'warranty':request.data.get("Warranty"),
            'origin':request.data.get("origin"),
            'shipping_country':request.data.get("shipping_country"),
            #'unit':request.data.get("unit"),
            'key_features':features,
            'is_deleted': False,
            'properties': request.data.get("properties"),
            'product_status': product_status,
            'is_own' :True,
        }
    else:
        product_data_value ={
            'product_admin_status': 'Confirmed',
            'title': request.data.get("title"),
            'brand': request.data.get("brand"),
            'description':request.data.get("description"),
            #'warranty':request.data.get("Warranty"),
            'origin':request.data.get("origin"),
            'shipping_country':request.data.get("shipping_country"),
            #'unit':request.data.get("unit"),
            'key_features':features,
            'is_deleted': False,
            'properties': request.data.get("properties"),
            'product_status': product_status,
            'is_own' :True,
        }
    category_data_value ={
            'category': request.data.get("category"),
            'sub_category': request.data.get("sub_category"),
            'sub_sub_category': request.data.get("sub_sub_category")
        }
    # product_price ={
    #     'price' : request.data.get("price"),
    #     'purchase_price': request.data.get("purchase_price"),
    #     #'currency_id': request.data.get('currency_id')
    # }
    # product_specification= [
    #     {
    #     "weight": request.data.get('weight'),
    #     "color":request.data.get('color'),
    #     "size":request.data.get('size'),
    #     'quantity': request.data.get('quantity')
    #    },
    #     {
    #     "color":'Green',
    #     "size":'Large',
    #     'quantity': 20
    #    },
    #     {
    #     "color":'Blue',
    #     "size":'XXL',
    #     'quantity': 7
    #    }
    # ]
    # product_point ={
    #     'point': request.data.get("point"),
    #     # 'end_date': data['point_end_date']
    #     'end_date': request.data.get("point_end_date")
    # }
    # product_discount ={
    #     'amount': request.data.get("amount"),
    #     #'start_date' : '2020-09-05',
    #     #'end_date' : data['discount_end_date']
    #     'end_date': request.data.get("discount_end_date")
    # }
    # product_image=[
    #          'This is image 1', 'This is image 2', 'This is image 3', 'This is image 4'
    # ]
    if request.method == 'POST':
        #print("dbcudbfdbcducbducbducbducbd")
        category_values= category1_data_upload (category_data_value)
        #print(category_values)
        category_data = category_values.json()
        #print(category_data)
        category_id = category_data['category']
        sub_category_id = category_data['sub_category']
        sub_sub_category_id = category_data['sub_sub_category']
        product_data_value.update( {'category_id' : category_id,'sub_category_id' : sub_category_id,'sub_sub_category_id' : sub_sub_category_id} )
        product_values= product_data_upload (product_data_value)
        product_data= product_values.json()
        product_id = product_data['id']
        #product_price.update( {'product_id' : product_id} )
        #price_values = product_price_data_upload (product_price)
        #product_point.update ({'product_id' : product_id})
        #point_values = product_point_data_upload(product_point)
        #product_code = create_product_code({'product_id' : product_id})
        #product_discount.update({'product_id' : product_id})
        #discount_data = product_discount_data_upload(product_discount)
        for i in range(int(count)):
            # print("dhuklam")
            dataz = request.data
            image_namez = dataz['title']
            image_name = image_namez + str(i) +".png"
            image = dataz['images['+str(i)+']']
            base_image=image.split(",")[1]
            imgdata = base64.b64decode(str(base_image))
            image = Image.open(io.BytesIO(imgdata))
            width, height = image.size
            # print(width,height)
            # image_name = "file.png"
            if width <= 475 and height <= 475:
                # print("size thikase")
                thumb_io = BytesIO() # create a BytesIO object
                # print(type(image))
                image.convert('RGB')
                image.save(thumb_io, 'PNG', quality=85) # save image to BytesIO object
                thumbnail = File(thumb_io, name=image_name)
                image_data = {'product_image':image,'product_id':product_id}
                product_image = ProductImage.objects.create(product_image=thumbnail,product_id=product_id)
                product_image.save()
                # print(product_image)
            else:
                thumb_io = BytesIO() # create a BytesIO object
                # print(type(image))
                image.convert('RGB')
                # height,width = imz.size
                imz=image.crop((0,0,width,height))
                if height > 475:
                    top = (height - 475)/2
                    botom = 475+top
                    imz=image.crop((0,top,width,botom))
                else:
                    imz=image.crop((0,0,width,height))
                new_width,new_height = imz.size
                # print("new height width", new_height, new_width)
                if width > 475:
                    left = (new_width - 475)/2
                    right = 475+left
                    imz=imz.crop((left,0,right,new_height))
                else:
                    imz=image.crop((0,0,new_width,new_height))
                # print('width resize image before')
                # imz.save("C://Users//K.M. FAIZULLAH\Desktop//Fuhad_all-works//09-11-2020//tango_ecomerce_child_backend//new_width_resize910.png")
                # print("after width saving image")
                # x_cordinate = int(width)/2
                # y_corodinate = int(height)/2
                # left = x_cordinate-237.5
                # right = width-left
                # top = height  - (y_corodinate+237.5)
                # imz=image.crop(((x_cordinate- 237.5),(y_corodinate+ 237.5),(width- 237.5),(y_corodinate-237.5)))
                height,width = imz.size
                # print("after all resize", height,  width)
                imz.save(thumb_io, 'PNG', quality=85) # save image to BytesIO object
                thumbnail = File(thumb_io, name=image_name)
                # print("here is the thumbnail", thumbnail)
                # print("fihfgudsfhds")
                # print(images)
                # image_data = {'product_image':images,'product_id':product_id}
                product_image = ProductImage.objects.create(product_image=thumbnail,product_id=product_id)
                # print(product_image)
                product_image.save()
            # product_image_serializer = ProductImageSerializer(data=image_data)
            # if product_image_serializer.is_valid():
            #     print("dhuklam1")
            #     product_image_serializer.save()
            # else:
            #     print("dhuklam2")
            #     print(product_image_serializer.errors)
        # product_img =[]
        # product_spec=[]
        # for img in product_image:
        #     data = {'content':img}
        #     data.update({'product_id' : product_id})
        #     img_data= product_image_data_upload(data)
        #     product_img.append(img_data.json())
        # for spec in product_specification:
        #     spec.update({'product_id' : product_id})            
        #     product_sp = product_specification_data_upload (spec)
        #     product_spec.append(product_sp.json())
        return Response({
            'success': True,
            'product_data': product_data,
            #'price_values': price_values.json(),
            #'product_specification': product_spec,
            #'product_point': point_values.json(),
            #'product_code': product_code.json(),
            #'product_discount': discount_data.json(),
            # 'product_image': product_img
        }) 
    # except:
    #     # product_price = ProductPrice.objects.filter(product_id = product_id)
    #     # if product_price.exists():
    #     #     product_price.delete()
    #     # product_discount = discount_product.objects.filter(product_id = product_id)
    #     # if product_discount.exists():
    #     #     product_discount.delete()
    #     # product_code = ProductCode.objects.filter(product_id = product_id)
    #     # if product_code.exists():
    #     #     product_code.delete()
    #     # product_point = ProductPoint.objects.filter(product_id = product_id)
    #     # if product_point.exists():
    #     #     product_point.delete()
    #     # product_specification = ProductSpecification.objects.filter(product_id = product_id)
    #     # if product_specification.exists():
    #     #     product_specification.delete()
    #     product_image = ProductImage.objects.filter(product_id = product_id)
    #     if product_image.exists():
    #         product_image.delete()
    #     product_value = Product.objects.filter(id = product_id)
    #     if product_value.exists():
    #         product_value.delete()
    #     return Response({
    #         'success': False,
    #         'message': 'Product insertion could not be completed'
    #         })

























@api_view(['POST','GET'])
def specific_product_delete_admin(request, product_id):

    if request.method == 'POST':

        try:
        
            product_value = Product.objects.get(id = product_id) 
            print(product_value)
            product_price = ProductPrice.objects.filter(product_id = product_id)
            print(product_price)
            product_discount = discount_product.objects.filter(product_id  = product_id)
            print(product_discount) 
            product_code = ProductCode.objects.filter(product_id  = product_id)
            print(product_code)
            product_point = ProductPoint.objects.filter(product_id = product_id)
            print(product_point)
            product_specification = ProductSpecification.objects.filter(product_id  = product_id)
            print(product_specification)
            product_image = ProductImage.objects.filter(product_id  = product_id)
            print(product_image)
            warehouse_info = WarehouseInfo.objects.filter(product_id = product_id)
            print(warehouse_info)
            shop_info = ShopInfo.objects.filter(product_id = product_id)
            print(shop_info)

           
            product_value.delete()
            if product_image.exists():
                product_image.delete()
                print("images deleted")
            if product_price.exists():
                product_price.delete()
                print("price dleted")
            if product_discount.exists():
                product_discount.delete()
                print("discount deleted")
            if product_code.exists():
                product_code.delete()
                print("code deleted")
            if product_point.exists():
                product_point.delete()
                print("point deleted")
            if product_specification.exists():
                product_specification.delete()
                print("specification deleted")

            if warehouse_info.exists():
                warehouse_info.delete()
                print("warehouse deleted")

            if shop_info.exists():
                shop_info.delete()
                print("shop deleted")

            return Response({
                'success': True,
                'message': 'Product has been deleted successfully'
            })
        
        except:
            return Response({
                'success': False,
                'message': 'Product could not be deleted successfully'
            })


@api_view(['POST','GET'])
def specific_product_hidden_delete(request, product_id):

    if request.method == 'POST':
        try:
            product_value = Product.objects.get(id = product_id) 
            product_value.is_deleted = True
            data = product_value.__dict__
            product_data_update(product_id, data)
            return Response({
                    'success': True,
                    'message': 'Product has been deleted successfully'
                })
        
        except:
            return Response({
                'success': False,
                'message': 'Product could not be deleted successfully'
            })


@api_view(['POST','GET'])
def modify_specific_product(request, product_id):
    data = request.data
    # product_values = {'title':'puffed rice'}
    # price_values = {'price': 150}
    # discount_values = {'amount': 30}
    # point_values = {'point': 20}
    # specification_values = {
    #         'color': 'blue'}



    print(data)

    key_features = request.data.get("key_features")
    features = key_features.split(",")


    product_data_value ={

            
            
            #'product_admin_status': 'Confirmed',
            'title': request.data.get("title"),
            #'title': 'XYZ',
            'brand': request.data.get("brand"),
            #'brand': 'Samsung',
            'description':request.data.get("description"),
            #'description':'xxx',
            #'warranty':request.data.get("Warranty"),
            #'warranty':'gffggfg',
            'origin':request.data.get("origin"),
            #'origin':'USA',
            'shipping_country':request.data.get("shipping_country"),
            #'shipping_country':'dwhfeuhefh',
            # 'unit':request.data.get("unit"),
            #'unit':'fhdufhdufhdufh',
            'key_features':features,
            'is_deleted': False,
            'properties': request.data.get("properties"),
            'is_own' :True
            
        }





    

    # category_data_value ={

            
    #         'category': data['category'],
    #         'category': 'ffgdsfdsf',
    #         'sub_category': data['sub_category'],
    #         'sub_category': data['sub_category'],

    #         'sub_sub_category': data['sub_sub_category'],
    #         'sub_sub_category': data['sub_sub_category']

    #     }


   
    # product_price ={
    #     #'price' : data['price'],
    #     #'price' : '1000',
    #     'price' : request.data.get("price"),
    #     #'currency_id': request.data.get('currency_id')
    # }

    # product_specification= [
    #     {
    #     "weight": request.data.get('weight'),
    #     "color":request.data.get('color'),
    #     "size":request.data.get('size'),
    #     'quantity': request.data.get('quantity')
    #    },
    #     {
        
    #     "color":'Green',
    #     "size":'Large',
    #     'quantity': 20
    #    },
    #     {
        
    #     "color":'Blue',
    #     "size":'XXL',
    #     'quantity': 7
    #    }
    # ]




    # product_point ={
    #     # 'point': data['point'],
    #     #'point' : '230',
    #     'point': request.data.get("point"),
    #     # 'end_date': data['point_end_date']
    #     'end_date' : request.data.get("end_date"),
    #     #'end_date': '2020-09-05'
    # }

    # product_discount ={

    #     # 'amount': data['amount'],
    #     #'amount' : '29',
    #     'amount' : request.data.get("amount"),
    #     #'start_date' : '2020-09-05',
    #     #'end_date' : data['discount_end_date']
    #     #'end_date': '2020-09-05',
    #     'end_date' : request.data.get("end_date"),

    # }

    # product_image=[
        
    #          'This is image 1', 'This is image 2', 'This is image 3', 'This is image 4'
    # ]

    if request.method == 'POST':
        
        try:
            
            
            
            # print(product_data)

            try:
                product = Product.objects.get(id = product_id)
            except:
                product = None

            if product:

                product_data = product_data_update(product_id, product_data_value)
                print(product_data)
                print("hochcche")

                # price_data = price_data_update (product_id, price_values)
                # print("price hoise")
                # print(price_data)

                #Update product price

                # try:
                #     product_prices = ProductPrice.objects.filter(product_id = product_id).last()

                # except:

                #     product_prices = None 

                # if product_prices:

                #     product_price_serializer = ProductPriceSerializer(product_prices,data=product_price)
                #     if product_price_serializer.is_valid():
                #         product_price_serializer.save()
                #         product_price_data = product_price_serializer.data
                #     else:
                #         return Response({'success':False,'message':'Price could not be updated'})

                # else:
                #     return Response({'success':False,'message':'Price could not be updated'})


                # try:
                #     product_points = ProductPoint.objects.filter(product_id = product_id).last()

                # except:

                #     product_points = None 

                # if product_points:

                #     product_point_serializer = ProductPointSerializer(product_points,data=product_point)
                #     if product_point_serializer.is_valid():
                #         product_point_serializer.save()
                #         product_point_data = product_point_serializer.data
                #     else:
                #         print(pr)
                #         return Response({'success':False,'message':'Point could not be updated'})

                # else:
                #     return Response({'success':False,'message':'Point could not be updated'})


                # try:
                #     product_discounts = discount_product.objects.filter(product_id = product_id).last()

                    


                # except:

                #     product_discounts = None



                # if product_discounts:

                #     product_discount_serializer = ProductDiscountSerializer(product_discounts,data=product_discount)
                   
                #     if product_discount_serializer.is_valid():
                #         product_discount_serializer.save()
                #         product_discount_data = product_discount_serializer.data
                #     else:
                #         return Response({'success':False,'message':'Point could not be updated'})

                # else:
                #     return Response({'success':False,'message':'Point could not be updated'})




            # discount_data = discount_data_update (product_id,discount_values)
            # print("discount hoise")
            # print(discount_data)
            # point_data = point_data_update (product_id,point_values)
            # print("point ase")
            # print(point_data)
            #specification_data = specification_data_update(product_id, specification_values)

            return Response({
                'success': True,
                'product': product_data.json(),
                # 'price': product_price_data,
                # 'discount':product_discount_data,
                # 'point': product_point_data,
                # 'specification': specification_data.json()

            })

        except:
            return Response({
                'success': False,
                'message': 'Product modification could not be updated'
               
            })



@api_view(['POST','GET'])
def group_product_insertion_admin(request):
    '''
    This Api is for inserting all the group related information by using a single API. This will be for the admin. Calling 
    http://127.0.0.1:8000/product/group_product_insert/ will cause to invoke this Api. 
    '''

    data = request.data 

    date = datetime.date.today()
    print(date)
    #data['key_features']=["red","blue","green"]
    
  
    product_data_value ={

            
            'title': data['title'],
            'brand':  data['brand'],
            'description': data['description'],
            'key_featues': data['key_features'],
            #'quantity': data['quantity'],
            'is_deleted': False,
            'properties': True,
            'is_group':True
        }


    category_data_value ={

            
            'category': data['category'],
            'sub_category': data['sub_category'],
            'sub_sub_category': data['sub_sub_category']
        }







    group_product_values=   {
    
            "products_ids": data['products_ids'],
            "title": data['group_title'],
            "startdate": date,
            "enddate": date,
            "flashsellname": data['flashsellname'],
            
        }

    product_price ={
        'price' : data['price'],
        # 'currency_id': '1'
    }

  #   product_specification= [
  #       {
        # "weight": '17',
        # "color":'red',
        # "size":'small',
  #       'quantity': 10
  #      },
  #       {
        
        # "color":'Green',
        # "size":'Large',
  #       'quantity': 20
  #      },
  #       {
        
        # "color":'Blue',
        # "size":'XXL',
  #       'quantity': 7
  #      }
  #   ]

    product_point ={
        'point': data['point'],
        'end_date' : date

    }

    product_discount ={

        'amount': data['amount'],
        'start_date' : date,
        'end_date' : date
    }

    # product_image=[
        
    #          'This is image 1', 'This is image 2', 'This is image 3', 'This is image 4'
    # ]

    

    if request.method == 'POST':
        try:
            category_values= category_data_upload (category_data_value)
            category_data = category_values.json()
            category_id = category_data['category']
            sub_category_id = category_data['sub_category']
            sub_sub_category_id = category_data['sub_sub_category']
            product_data_value.update( {'category_id' : category_id,'sub_category_id' : sub_category_id,'sub_sub_category_id' : sub_sub_category_id} )
            product_values= product_data_upload (product_data_value)
            product_data= product_values.json()
            product_id = product_data['id']
            print(product_id)
            
            group_product_values.update( {'product_id' : product_id} )
            group_values = group_product_data_update (group_product_values)
            product_price.update( {'product_id' : product_id} )
            price_values = product_price_data_upload (product_price)
            product_point.update ({'product_id' : product_id})
            point_values = product_point_data_upload(product_point)
            product_code = create_product_code({'product_id' : product_id})
            product_discount.update({'product_id' : product_id})
            discount_data = product_discount_data_upload(product_discount)
            product_img =[]
            product_spec=[]
            
            # for img in product_image:
            #     data = {'content':img}
            #     data.update({'product_id' : product_id})
            #     img_data= product_image_data_upload(data)
            #     product_img.append(img_data.json())
            
            # for spec in product_specification:
            #     spec.update({'product_id' : product_id})            
            #     product_sp = product_specification_data_upload (spec)
            #     product_spec.append(product_sp.json())
        
            return Response({
                'success': True,
                'product_data': product_data,
                'group_values': group_values.json(),
                'price_values': price_values.json(),
                # 'product_specification': product_spec,
                'product_point': point_values.json(),
                'product_code': product_code.json(),
                'product_discount': discount_data.json(),
                # 'product_image': product_img
            }) 
        except:

            product_price = ProductPrice.objects.filter(product_id = product_id)
            if product_price.exists():
                product_price.delete()

            group_product = GroupProduct.objects.filter(product_id = product_id)
            if group_product.exists():
                group_product.delete()

            product_discount = discount_product.objects.filter(product_id = product_id)
            if product_discount.exists():
                product_discount.delete()

            product_code = ProductCode.objects.filter(product_id = product_id)
            if product_code.exists():
                product_code.delete()

            product_point = ProductPoint.objects.filter(product_id = product_id)
            if product_point.exists():
                product_point.delete()

            product_specification = ProductSpecification.objects.filter(product_id = product_id)
            if product_specification.exists():
                product_specification.delete()
            
            product_image = ProductImage.objects.filter(product_id = product_id)
            if product_image.exists():
                product_image.delete()
            
            product_value = Product.objects.filter(id = product_id)
            if product_value.exists():
                product_value.delete()
            
            return Response({
                'success': False,
                'message': 'Group Product could not be inserted'
                })
            
@api_view(['POST','GET'])
def modify_specific_group_product(request, product_id):
    '''
    This is for modifying specific group product using a single Api. Calling the http://127.0.0.1:8000/product/modify_group_product/3/ will cause to
    invoke this Api.
    prams: product_id
    '''
    product_values = {'title':'puffed rice'}
    price_values = {'price': 150}
    discount_values = {'amount': 30}
    point_values = {'point': 20}
    specification_values = {
            'color': 'a'}

    group_product_values=   {

        "products_ids": [1,2,25],
        "title": "Have some days",
    }

    if request.method == 'GET':
        try:
             product = Product.objects.get(id=product_id)
        except:
            return JsonResponse({
                'success':False,
                'message':'Data could not be retrived'
            })

        product_serializer = AllGroupProductSerialyzer(product,many= False)
        return JsonResponse({
            'success':True,
            'message':'The data is shown below',
            'data':product_serializer.data},safe=False)


    if request.method == 'POST':
        
        try:
            
            product_data = product_data_update(product_id, product_values)
            group_data= group_product_data_modification(product_id,group_product_values)
            price_data = price_data_update (product_id, price_values)
            discount_data = discount_data_update (product_id,discount_values)
            point_data = point_data_update (product_id,point_values)
            specification_data = specification_data_update(product_id, specification_values)

            # return Response({
            #     'success': True,
            #     'product': product_data.json(),
            #     'price': price_data.json(),
            #     'discount':discount_data.json(),
            #     'point': point_data.json(),
            #     'specification': specification_data.json(),
            #     'group': group_data.json()

            # })

            return Response({
                'success': True,
                'product': product_data.json(),
                'price': price_data.json(),
                'discount':discount_data.json(),
                'point': point_data.json(),
                'specification': specification_data.json(),
                # 'group': group_data.json()

            })

        except:
            return Response({
                'success': False,
                'message': 'Data could not be updated'
               
            })


@api_view(['POST','GET'])
def get_all_detailed_group_product(request, number = 0):
    '''
    This is for showing all the group product together. An individual may send request to show the specific amount of details by sending the 
    expected number in the parameters. Number less than 0 will cause to show all the group product details.
    calling http://127.0.0.1:8000/product/all_group_product/2/ will cause to invoke this Api.

    parms: number

    '''
    
    if request.method == 'GET':
        try:
            products = Product.objects.all()
            product_serializer = AllGroupProductSerialyzer(products,many= True)
            if number>0:
                return Response({
                    'success': True,
                    'message':'Data has been retrived successfully',
                    'data':product_serializer.data[:number]
                })
            else:
                return Response({
                    'success': True,
                    'message':'Data has been retrived successfully',
                    'data':product_serializer.data
                })

        except:
            return Response({
                    'success': False,
                    'message':'Data could not be retrived',
                })
            

        
            
# Merchent Product Approval Confirmed
@api_view(['POST',])
def merchant_approval(request,product_id):
    try:
        specific_product=Product.objects.get(id=product_id)
    
    except:
        specific_product = None

    if specific_product:
        print("condition a dokce")

        # print(specific_product.admin_approval)

        specific_product.product_admin_status = "Confirmed"
        
        specific_product.save()
        return JsonResponse({"Success":True , "message":"This Product Has benn Approved"})

    else:
        return JsonResponse({'success':False,'message': 'This Product does not exist'})
        



@api_view(['POST',])
def merchant_calcceled(request,product_id):
    try:
        specific_product=Product.objects.get(id=product_id)
    
    except:
        specific_product = None

    if specific_product:
        print("condition a dokce")

        # print(specific_product.admin_approval)

        specific_product.product_admin_status = "Cancelled"
        
        specific_product.save()
        return JsonResponse({"Success":True , "message":"This Product Has benn Approved"})

    else:
        return JsonResponse({'success':False,'message': 'This Product does not exist'})


@api_view(['GET',])
def seller_list(request):

    #Find the seller ids 



    try:

        products = Product.objects.filter(is_deleted=False)

    except:

        products = None 


    if products:


        seller_ids = list(products.values_list('seller',flat=True).distinct())




        if -1 in seller_ids:

            seller_ids.remove(-1)


        print(seller_ids)


    else:

        seller_ids = []


    try:

        seller = User.objects.filter(id__in=seller_ids)


    except:

        seller = None 


    if seller:

        seller_serializer = SellerInfoSerializer(seller,many=True)

        return JsonResponse({'success':True,'message':'Data is displayed below','data':seller_serializer.data})

    else:

        return JsonResponse({'success':False,'message':'No data is there'})



@api_view(['GET',])
def seller_approved_products(request,user_id):


    try:

        product = Product.objects.filter(is_deleted=False,seller=user_id,product_admin_status="Confirmed")

    except:

        product = None 


    if product:

        product_serializer = SellerInfoProductSerializer(product,many=True)

        return JsonResponse({'success':True,'message':'The dats is shown','data':product_serializer.data})


    else:

        return JsonResponse({'success':False,'message':'The data is shown'})



@api_view(['GET',])
def seller_cancelled_products(request,user_id):


    try:

        product = Product.objects.filter(is_deleted=False,seller=user_id,product_admin_status="Cancelled")

    except:

        product = None 


    if product:

        product_serializer = SellerInfoProductSerializer(product,many=True)

        return JsonResponse({'success':True,'message':'The dats is shown','data':product_serializer.data})


    else:

        return JsonResponse({'success':False,'message':'The data is shown'})




@api_view(['GET',])
def seller_pending_products(request,user_id):


    try:

        product = Product.objects.filter(is_deleted=False,seller=user_id,product_admin_status="Processing")

    except:

        product = None 


    if product:

        product_serializer = SellerInfoProductSerializer(product,many=True)

        return JsonResponse({'success':True,'message':'The dats is shown','data':product_serializer.data})


    else:

        return JsonResponse({'success':False,'message':'The data is shown'})


        



@api_view(['POST',])
def share_product(request,product_id):

    try:

        product = Product.objects.get(id=product_id)

    except:

        product = None 

    if product:

        product.properties = True

        product.save()

        return JsonResponse({'success':True, 'message':'This product has been shared'})

    else:

        return JsonResponse({'success':False, 'message':'This product does not exist'})



@api_view(['POST',])
def publish_product(request,product_id):

    try:

        product = Product.objects.get(id=product_id)

    except:

        product = None 

    if product:

        product.product_status = "Published"

        product.save()

        return JsonResponse({'success':True, 'message':'This product has been shared'})

    else:

        return JsonResponse({'success':False, 'message':'This product does not exist'})


@api_view(['POST',])
def cancel_publish_product(request,product_id):

    try:

        product = Product.objects.get(id=product_id)

    except:

        product = None 

    if product:

        product.product_status = "Cancelled"

        product.save()

        return JsonResponse({'success':True, 'message':'This product has been shared'})

    else:

        return JsonResponse({'success':False, 'message':'This product does not exist'})






@api_view(['GET',])
def all_seller_approved_products(request):

    #Find the seller ids 



    try:

        products = Product.objects.filter(is_deleted=False)

    except:

        products = None 


    if products:


        seller_ids = list(products.values_list('seller',flat=True).distinct())




        if -1 in seller_ids:

            seller_ids.remove(-1)


        print(seller_ids)


    else:

        seller_ids = []



    try:

        approved_products = Product.objects.filter(seller__in=seller_ids,is_deleted=False,product_admin_status="Confirmed").order_by('-date')

    except:

        approved_products = None 

    if approved_products:

        product_serializer = ProductAdminSerializer1(approved_products,many=True)

        product_data = product_serializer.data

        return JsonResponse({'success':True,'message':'The products are shown as follows','data':product_data})

    else:

        product_data = []

        return JsonResponse({'success':False,'message':'The products are shown as follows','data':product_data})




@api_view(['GET',])
def all_seller_cancelled_products(request):

    #Find the seller ids 



    try:

        products = Product.objects.filter(is_deleted=False)

    except:

        products = None 


    if products:


        seller_ids = list(products.values_list('seller',flat=True).distinct())




        if -1 in seller_ids:

            seller_ids.remove(-1)


        print(seller_ids)


    else:

        seller_ids = []



    try:

        approved_products = Product.objects.filter(seller__in=seller_ids,is_deleted=False,product_admin_status="Cancelled").order_by('-date')

    except:

        approved_products = None 

    if approved_products:

        product_serializer = ProductAdminSerializer1(approved_products,many=True)

        product_data = product_serializer.data

        return JsonResponse({'success':True,'message':'The products are shown as follows','data':product_data})

    else:

        product_data = []

        return JsonResponse({'success':False,'message':'The products are shown as follows','data':product_data})





@api_view(['GET',])
def all_seller_pending_products(request):

    #Find the seller ids 



    try:

        products = Product.objects.filter(is_deleted=False)

    except:

        products = None 


    if products:


        seller_ids = list(products.values_list('seller',flat=True).distinct())




        if -1 in seller_ids:

            seller_ids.remove(-1)


        print(seller_ids)


    else:

        seller_ids = []



    try:

        approved_products = Product.objects.filter(seller__in=seller_ids,is_deleted=False,product_admin_status="Processing").order_by('-date')

    except:

        approved_products = None 

    if approved_products:

        product_serializer = ProductAdminSerializer1(approved_products,many=True)

        product_data = product_serializer.data

        return JsonResponse({'success':True,'message':'The products are shown as follows','data':product_data})

    else:

        product_data = []

        return JsonResponse({'success':False,'message':'The products are shown as follows','data':product_data})



# @api_view (["GET","POST"])
# def get_specific_barcodecode_values(request,specification_id):
#     '''
#         This api is for generating barcode values.
#     '''

#     if(request.method == "GET"):
#         try:
#             product_code= ""
#             try:
#                 queryset = ProductCode.objects.get(specification_id = specification_id)
#             except:
#                 queryset= None
            
#             if queryset:
#                 if queryset.manual_Barcode:
#                     product_code = queryset.manual_Barcode
#                 else:
#                     product_code= queryset.Barcode

#                 bar = barcode.get_barcode_class('code39')

#                 bar_value = bar(product_code, writer = ImageWriter())

#                 if not os.path.exists(settings.MEDIA_DIR+'/barcode/'):
#                     os.makedirs(settings.MEDIA_DIR+'/barcode/')

#                 if queryset.Barcode_img:
#                     os.remove(queryset.Barcode_img)
#                 bar_value.save(settings.MEDIA_DIR+'/barcode/'+product_code)
#                 url = settings.MEDIA_DIR+'/barcode/' +product_code+'.png'
#                 data_values  = {'Barcode_img' : url}
#                 code_serializer_value = ProductCodeSerializer (queryset, data= data_values)
#                 if(code_serializer_value.is_valid()):
#                     code_serializer_value.save()
#                 else:
#                     return Response ({"success": False, 'message': 'Something went wrong !!'})
#                 # resized = Image.open(queryset.Barcode_img) 
#                 # newSize = (width , height )
#                 # Getting barcode url and before retreiving it resizes the barcode as per the user specification
#                 # resized = resized.resize(newSize, resample=PIL.Image.NEAREST)
#                 # resized.save(settings.MEDIA_DIR+'/barcode/'+ str(product_id)+'.png')
#                 # url = settings.MEDIA_DIR+'/barcode/' + str(product_id)+'.png'
#                 query_values = ProductCode.objects.get(specification_id = specification_id)
#                 code_serializers = ProductCodeSerializer (query_values, many = False)
#                 return Response ({"success": True, 'message': 'Data has been retrived successfully', 'data': code_serializers.data})
#             else:
#                 return Response({"success": False,'message': 'There is no value to retrive'})
#         except:
#             return Response({"success": False,'message': 'Something went wrong !!'})


# @api_view (["GET","POST"])
# def get_specific_sku_values(request,specification_id):
#     '''
#         This api is for generating sku values.
#     '''

#     if(request.method == "GET"):
#         try:
#             product_code= ""
#             try:
#                 queryset = ProductCode.objects.get(specification_id = specification_id)
#             except:
#                 queryset= None
            
#             if queryset:
#                 if queryset.manual_SKU:
#                     product_code = queryset.manual_SKU
#                 else:
#                     product_code= queryset.SKU

#                 bar = barcode.get_barcode_class('code39')

#                 bar_value = bar(product_code, writer = ImageWriter())

#                 if not os.path.exists(settings.MEDIA_DIR+'/SKU/'):
#                     os.makedirs(settings.MEDIA_DIR+'/SKU/')

#                 if queryset.SKU_img:
#                     os.remove(queryset.SKU_img)
#                 bar_value.save(settings.MEDIA_DIR+'/SKU/'+product_code)
#                 url = settings.MEDIA_DIR+'/SKU/' +product_code+'.png'
#                 data_values  = {'SKU_img' : url}
#                 code_serializer_value = ProductCodeSerializer (queryset, data= data_values)
#                 if(code_serializer_value.is_valid()):
#                     code_serializer_value.save()
#                 else:
#                     return Response ({"success": False, 'message': 'Something went wrong !!'})
#                 # resized = Image.open(queryset.Barcode_img) 
#                 # newSize = (width , height )
#                 # Getting barcode url and before retreiving it resizes the barcode as per the user specification
#                 # resized = resized.resize(newSize, resample=PIL.Image.NEAREST)
#                 # resized.save(settings.MEDIA_DIR+'/barcode/'+ str(product_id)+'.png')
#                 # url = settings.MEDIA_DIR+'/barcode/' + str(product_id)+'.png'
#                 query_values = ProductCode.objects.get(specification_id = specification_id)
#                 code_serializers = ProductCodeSerializer (query_values, many = False)
#                 return Response ({"success": True, 'message': 'Data has been retrived successfully', 'data': code_serializers.data})
#             else:
#                 return Response({"success": False,'message': 'There is no value to retrive'})
#         except:
#             return Response({"success": False,'message': 'Something went wrong !!'})

# # @api_view (["GET","POST"])
# # def insert_specific_code_values(request):
# #     '''
# #     This is for creating barcode for a particular product and insert it into the database. Calling http://127.0.0.1:8000/code/insert_value/ will 
# #     cause to invoke this API. This api has just post response.

# #     POST Response:
# #         While performing post response this api requires just the product id. Based on that product id this api will generate the product code 
# #         and will save the code as an image data into the media folder. At a same time it will store the image url into database Barcode field.
    
# #     '''
# #     if request.method == "POST":
# #         # demo values
# #         values = request.data
# #         your_domain = Site.objects.get_current().domain
    
# #         bar = barcode.get_barcode_class('code39')
# #         bar_value = bar(your_domain+str(values['product_id']), writer = ImageWriter())
# #         if not os.path.exists(settings.MEDIA_DIR+'/barcode/'):
# #             os.makedirs(settings.MEDIA_DIR+'/barcode/')
# #         bar_value.save(settings.MEDIA_DIR+'/barcode/'+ str(values['product_id']))
# #         url = settings.MEDIA_DIR+'/barcode/' + str(values['product_id'])+'.png'

# #         data_values  = {'product_id' : values['product_id'], 'Barcode_img' : url, 'Barcode' : your_domain+str((values['product_id'])) }

# #         code_serializer_value = ProductCodeSerializer (data= data_values)
# #         if(code_serializer_value.is_valid()):
# #             code_serializer_value.save()
# #             return Response (code_serializer_value.data, status=status.HTTP_201_CREATED)
# #         return Response (code_serializer_value.errors)

# # @api_view (["GET","POST"])
# # def insert_specific_code_values(request):
# #     '''
# #     This is for creating barcode for a particular product and insert it into the database. Calling http://127.0.0.1:8000/code/insert_value/ will 
# #     cause to invoke this API. This api has just post response.

# #     POST Response:
# #         While performing post response this api requires just the product id. Based on that product id this api will generate the product code 
# #         and will save the code as an image data into the media folder. At a same time it will store the image url into database Barcode field.
    
# #     '''
# #     if request.method == "POST":
# #         # demo values
# #         values = request.data
# #         your_domain = Site.objects.get_current().domain

# #         bar = barcode.get_barcode_class('code39')
# #         bar_value = bar(str(values['product_id']), writer = ImageWriter())

# #         if not os.path.exists(settings.MEDIA_DIR+'/barcode/'):
# #             os.makedirs(settings.MEDIA_DIR+'/barcode/')
# #         bar_value.save(settings.MEDIA_DIR+'/barcode/'+ str(values['product_id']))
# #         url = settings.MEDIA_DIR+'/barcode/' + str(values['product_id'])+'.png'

# #         data_values  = {'product_id' : values['product_id'], 'Barcode_img' : url, 'Barcode' : str((values['product_id'])) }

# #         code_serializer_value = ProductCodeSerializer (data= data_values)
# #         if(code_serializer_value.is_valid()):
# #             code_serializer_value.save()
# #             return Response (code_serializer_value.data, status=status.HTTP_201_CREATED)
# #         return Response (code_serializer_value.errors)

# @api_view (["GET","POST"])
# def insert_specific_code_values(request):
#     '''
#     This is for creating barcode for a particular product and insert it into the database. Calling http://127.0.0.1:8000/code/insert_value/ will 
#     cause to invoke this API. This api has just post response.

#     POST Response:
#         While performing post response this api requires just the product id. Based on that product id this api will generate the product code 
#         and will save the code as an image data into the media folder. At a same time it will store the image url into database Barcode field.
    
#     '''
#     if request.method == "POST":
#         values = request.data
#         your_domain = Site.objects.get_current().domain
#         data_values  = {'product_id' : values['product_id'], 'specification_id': values['specification_id'],'Barcode' : your_domain+str((values['specification_id'])),'SKU' : your_domain+str((values['specification_id'])) }
#         code_serializer_value = ProductCodeSerializer (data= data_values)
#         if(code_serializer_value.is_valid()):
#             code_serializer_value.save()
#             return Response ({
#                 'success': True,
#                 'message': 'Data has been inserted successfully',
#                 'data':code_serializer_value.data}, status=status.HTTP_201_CREATED)
#         return Response ({
#             'success': False,
#             'message': 'Something went wrong !!',
#             'error': code_serializer_value.errors
#         })

# @api_view (["GET","POST"])
# def insert_manual_code_values(request, specification_id):
#     '''
#         This api is for generating manual barcode and sku.
#     '''
#     if request.method == "POST":
#         values = request.data
#         spec_data = ProductCode.objects.filter(specification_id=specification_id)
#         if spec_data.exists():
#             code_serializer_value = ProductCodeSerializer (spec_data[0], data= values)
#             if(code_serializer_value.is_valid()):
#                 code_serializer_value.save()
#                 return Response ({
#                     'success': True,
#                     'message': 'Data has been modified successfully',
#                     'data':code_serializer_value.data}, status=status.HTTP_201_CREATED)
#             return Response ({
#                 'success': False,
#                 'message': 'Something went wrong !!',
#                 'error': code_serializer_value.errors
#             })
            

# @api_view (["GET","POST"])
# def specific_code_delete(request,specification_id):
#     '''
#     This Api is for deleting a particular product value. While performing the delete operation it expects a particualr product id. 
#     Calling http://127.0.0.1:8000/code/delete_value/4/ will cause to invoke this API.
#     '''
#     #demo value

#     try:
#         specific_data = ProductCode.objects.get(specification_id = specification_id)
#     except :
#         return Response({'message': 'There is no value to delete'})
    
#     if request.method == "POST":
#         specific_data.delete()
#         if specific_data.Barcode_img or specific_data.SKU_img:
#             os.remove(specific_data.Barcode_img)
#         return Response({'success':True,'message': ' Value is successfully  deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view (["GET","POST"])
def get_specific_barcodecode_values(request,specification_id):
    '''
        This api is for generating barcode values.
    '''

    if(request.method == "GET"):
        try:
            product_code= ""
            try:
                queryset = ProductCode.objects.get(specification_id = specification_id)
            except:
                queryset= None
            
            if queryset:
                if queryset.manual_Barcode:
                    product_code = queryset.manual_Barcode
                else:
                    product_code= queryset.Barcode

                bar = barcode.get_barcode_class('code39')

                bar_value = bar(product_code, writer = ImageWriter())

                if not os.path.exists(settings.MEDIA_DIR+'/barcode/'):
                    os.makedirs(settings.MEDIA_DIR+'/barcode/')

                if queryset.Barcode_img:
                    os.remove(queryset.Barcode_img)
                bar_value.save(settings.MEDIA_DIR+'/barcode/'+product_code)
                url = settings.MEDIA_DIR+'/barcode/' +product_code+'.png'
                data_values  = {'Barcode_img' : url}
                code_serializer_value = ProductCodeSerializer (queryset, data= data_values)
                if(code_serializer_value.is_valid()):
                    code_serializer_value.save()
                else:
                    return Response ({"success": False, 'message': 'Something went wrong !!'})
                # resized = Image.open(queryset.Barcode_img) 
                # newSize = (width , height )
                # Getting barcode url and before retreiving it resizes the barcode as per the user specification
                # resized = resized.resize(newSize, resample=PIL.Image.NEAREST)
                # resized.save(settings.MEDIA_DIR+'/barcode/'+ str(product_id)+'.png')
                # url = settings.MEDIA_DIR+'/barcode/' + str(product_id)+'.png'
                query_values = ProductCode.objects.get(specification_id = specification_id)
                code_serializers = ProductCodeSerializer (query_values, many = False)
                return Response ({"success": True, 'message': 'Data has been retrived successfully', 'data': code_serializers.data})
            else:
                return Response({"success": False,'message': 'There is no value to retrive'})
        except:
            return Response({"success": False,'message': 'Something went wrong !!'})


@api_view (["GET","POST"])
def get_specific_sku_values(request,specification_id):
    '''
        This api is for generating sku values.
    '''

    if(request.method == "GET"):
        try:
            product_code= ""
            try:
                queryset = ProductCode.objects.get(specification_id = specification_id)
            except:
                queryset= None
            
            if queryset:
                if queryset.manual_SKU:
                    product_code = queryset.manual_SKU
                else:
                    product_code= queryset.SKU

                bar = barcode.get_barcode_class('code39')

                bar_value = bar(product_code, writer = ImageWriter())

                if not os.path.exists(settings.MEDIA_DIR+'/SKU/'):
                    os.makedirs(settings.MEDIA_DIR+'/SKU/')

                if queryset.SKU_img:
                    os.remove(queryset.SKU_img)
                bar_value.save(settings.MEDIA_DIR+'/SKU/'+product_code)
                url = settings.MEDIA_DIR+'/SKU/' +product_code+'.png'
                data_values  = {'SKU_img' : url}
                code_serializer_value = ProductCodeSerializer (queryset, data= data_values)
                if(code_serializer_value.is_valid()):
                    code_serializer_value.save()
                else:
                    return Response ({"success": False, 'message': 'Something went wrong !!'})
                # resized = Image.open(queryset.Barcode_img) 
                # newSize = (width , height )
                # Getting barcode url and before retreiving it resizes the barcode as per the user specification
                # resized = resized.resize(newSize, resample=PIL.Image.NEAREST)
                # resized.save(settings.MEDIA_DIR+'/barcode/'+ str(product_id)+'.png')
                # url = settings.MEDIA_DIR+'/barcode/' + str(product_id)+'.png'
                query_values = ProductCode.objects.get(specification_id = specification_id)
                code_serializers = ProductCodeSerializer (query_values, many = False)
                return Response ({"success": True, 'message': 'Data has been retrived successfully', 'data': code_serializers.data})
            else:
                return Response({"success": False,'message': 'There is no value to retrive'})
        except:
            return Response({"success": False,'message': 'Something went wrong !!'})

# @api_view (["GET","POST"])
# def insert_specific_code_values(request):
#     '''
#     This is for creating barcode for a particular product and insert it into the database. Calling http://127.0.0.1:8000/code/insert_value/ will 
#     cause to invoke this API. This api has just post response.

#     POST Response:
#         While performing post response this api requires just the product id. Based on that product id this api will generate the product code 
#         and will save the code as an image data into the media folder. At a same time it will store the image url into database Barcode field.
    
#     '''
#     if request.method == "POST":
#         # demo values
#         values = request.data
#         your_domain = Site.objects.get_current().domain
    
#         bar = barcode.get_barcode_class('code39')
#         bar_value = bar(your_domain+str(values['product_id']), writer = ImageWriter())
#         if not os.path.exists(settings.MEDIA_DIR+'/barcode/'):
#             os.makedirs(settings.MEDIA_DIR+'/barcode/')
#         bar_value.save(settings.MEDIA_DIR+'/barcode/'+ str(values['product_id']))
#         url = settings.MEDIA_DIR+'/barcode/' + str(values['product_id'])+'.png'

#         data_values  = {'product_id' : values['product_id'], 'Barcode_img' : url, 'Barcode' : your_domain+str((values['product_id'])) }

#         code_serializer_value = ProductCodeSerializer (data= data_values)
#         if(code_serializer_value.is_valid()):
#             code_serializer_value.save()
#             return Response (code_serializer_value.data, status=status.HTTP_201_CREATED)
#         return Response (code_serializer_value.errors)

# @api_view (["GET","POST"])
# def insert_specific_code_values(request):
#     '''
#     This is for creating barcode for a particular product and insert it into the database. Calling http://127.0.0.1:8000/code/insert_value/ will 
#     cause to invoke this API. This api has just post response.

#     POST Response:
#         While performing post response this api requires just the product id. Based on that product id this api will generate the product code 
#         and will save the code as an image data into the media folder. At a same time it will store the image url into database Barcode field.
    
#     '''
#     if request.method == "POST":
#         # demo values
#         values = request.data
#         your_domain = Site.objects.get_current().domain

#         bar = barcode.get_barcode_class('code39')
#         bar_value = bar(str(values['product_id']), writer = ImageWriter())

#         if not os.path.exists(settings.MEDIA_DIR+'/barcode/'):
#             os.makedirs(settings.MEDIA_DIR+'/barcode/')
#         bar_value.save(settings.MEDIA_DIR+'/barcode/'+ str(values['product_id']))
#         url = settings.MEDIA_DIR+'/barcode/' + str(values['product_id'])+'.png'

#         data_values  = {'product_id' : values['product_id'], 'Barcode_img' : url, 'Barcode' : str((values['product_id'])) }

#         code_serializer_value = ProductCodeSerializer (data= data_values)
#         if(code_serializer_value.is_valid()):
#             code_serializer_value.save()
#             return Response (code_serializer_value.data, status=status.HTTP_201_CREATED)
#         return Response (code_serializer_value.errors)

# @api_view (["GET","POST"])
# def insert_specific_code_values(request):
#     '''
#     This is for creating barcode for a particular product and insert it into the database. Calling http://127.0.0.1:8000/code/insert_value/ will 
#     cause to invoke this API. This api has just post response.

#     POST Response:
#         While performing post response this api requires just the product id. Based on that product id this api will generate the product code 
#         and will save the code as an image data into the media folder. At a same time it will store the image url into database Barcode field.
    
#     '''
#     if request.method == "POST":
#         values = request.data
#         your_domain = 'TSC'
#         site_values = CompanyInfo.objects.all()
#         # print("here is the site_values", site_values[0].site_identification)
#         spec_value = ProductCode.objects.filter(specification_id = values['specification_id'])
#         spec_val = spec_value[0]
#         site_identity = site_values[0].site_identification
#         data_values  = {'product_id' : values['product_id'], 'specification_id': values['specification_id'],'Barcode' : your_domain+"-"+site_identity +"-"+str((values['specification_id'])),'SKU' :  your_domain+"-"+site_identity +"-"+str((values['specification_id'])) }
#         code_serializer_value = ProductCodeSerializer (spec_val,data= data_values)
#         if(code_serializer_value.is_valid()):
#             code_serializer_value.save()
#             return Response ({
#                 'success': True,
#                 'message': 'Data has been inserted successfully',
#                 'data':code_serializer_value.data}, status=status.HTTP_201_CREATED)
#         return Response ({
#             'success': False,
#             'message': 'Something went wrong !!',
#             'error': code_serializer_value.errors
#         })


@api_view (["GET","POST"])
def insert_specific_code_values(request):
    '''
    This is for creating barcode for a particular product and insert it into the database. Calling http://127.0.0.1:8000/code/insert_value/ will 
    cause to invoke this API. This api has just post response.
    POST Response:
        While performing post response this api requires just the product id. Based on that product id this api will generate the product code 
        and will save the code as an image data into the media folder. At a same time it will store the image url into database Barcode field.
    '''
    if request.method == "POST":
        values = request.data
        your_domain = 'TSC'
        site_values = CompanyInfo.objects.all()
        # print("here is the site_values", site_values[0].site_identification)
        spec_value = ProductCode.objects.filter(specification_id = values['specification_id'])
        spec_val = spec_value[0]
        if site_values.exists():
            site_identity = site_values[0].site_identification
        else:
            site_identity= "0000"
        if len(values['manual_SKU']) == 4:
            pre_sku = 'M'
            post_sku = values['manual_SKU']
        else:
            pre_sku = 'A'
            post_sku=site_identity
        SKU_code = pre_sku+ "-"+ str(site_identity)+"-"+str(values['uid'])+"-"+str(values['product_id'])+"-"+str(values['specification_id'])+"-"+str(post_sku)
        data_values  = {
            'product_id' : values['product_id'], 
            'specification_id': values['specification_id'],
            'Barcode' : SKU_code,
            'SKU' :  SKU_code 
            }
        code_serializer_value = ProductCodeSerializer (spec_val,data= data_values)
        if(code_serializer_value.is_valid()):
            code_serializer_value.save()
            return Response ({
                'success': True,
                'message': 'Data has been inserted successfully',
                'data':code_serializer_value.data}, status=status.HTTP_201_CREATED)
        return Response ({
            'success': False,
            'message': 'Something went wrong !!',
            'error': code_serializer_value.errors
        })

@api_view (["GET","POST"])
def insert_manual_code_values(request, specification_id):
    '''
        This api is for generating manual barcode and sku.
    '''
    if request.method == "POST":
        values = request.data
        spec_data = ProductCode.objects.filter(specification_id=specification_id)
        if spec_data.exists():
            code_serializer_value = ProductCodeSerializer (spec_data[0], data= values)
            if(code_serializer_value.is_valid()):
                code_serializer_value.save()
                return Response ({
                    'success': True,
                    'message': 'Data has been modified successfully',
                    'data':code_serializer_value.data}, status=status.HTTP_201_CREATED)
            return Response ({
                'success': False,
                'message': 'Something went wrong !!',
                'error': code_serializer_value.errors
            })
            

@api_view (["GET","POST"])
def specific_code_delete(request,specification_id):
    '''
    This Api is for deleting a particular product value. While performing the delete operation it expects a particualr product id. 
    Calling http://127.0.0.1:8000/code/delete_value/4/ will cause to invoke this API.
    '''
    #demo value

    try:
        specific_data = ProductCode.objects.get(specification_id = specification_id)
    except :
        return Response({'message': 'There is no value to delete'})
    
    if request.method == "POST":
        specific_data.delete()
        if specific_data.Barcode_img or specific_data.SKU_img:
            os.remove(specific_data.Barcode_img)
        return Response({'success':True,'message': ' Value is successfully  deleted'}, status=status.HTTP_204_NO_CONTENT)





@api_view (["POST",])
def pos_products(request):

    API_key = request.data.get("API_key")
    count = 0 

    try:

        term = Terminal.objects.all()

    except:
        term = None 

    print(term)

    if term: 

        term_ids =  list(term.values_list('id',flat=True))
        term_count = len(term_ids)
        print(term_count)

        print(term_ids)

        for i in range(len(term_ids)):

            try:
                specific_term = Terminal.objects.get(id=term_ids[i])
            except:
                specific_term = None 
            print(specific_term)
            if specific_term:
                print(specific_term.API_key)
                if specific_term.API_key == API_key:
                    warehouse_id = specific_term.warehouse_id
                    shop_id = specific_term.shop_id
                    print("terminal er stock id")
                    print(warehouse_id)
                    print(shop_id)
                    get_id(warehouse_id,shop_id)


                    try:
                        products = Product.objects.all()

                    except:
                        products = None 

                    if products:

                        print("loop er bhitore")


                        product_serializer= ProductPOSSerializer1(products,many=True)

                        product_data = product_serializer.data

                        return JsonResponse({'success':True,'message':'Data is shown below','data':product_data})



                    else:

                        return JsonResponse({'success':False,'message':'No data is available','data': []})

                else:
                    count = count + 1
                    
                    # return JsonResponse({'success':False,'message':'The API keys dont match'})

            else:
                pass

        if count == term_count:
            return JsonResponse({"success":False,"message":"The API key provided does not match"})


    else:
        print("terminal ey dhuke nai")
        return JsonResponse({'success':False,'message':'There are no exisiting terminals'})


         



@api_view (["GET","POST"])
def edit_images(request,product_id):

    # old_images = [{
    #     'content': 'Good image',
    #     'id':36,
    #     'image_url':'asdasdsad' ,
    #     'product_id': 7,
    #     'product_image': 'fhwbfuwhfuwehf'
    #     },

    #     {
    #     'content': 'Good image',
    #     'id':37,
    #     'image_url':'asdasdsad' ,
    #     'product_id': 7,
    #     'product_image': 'fhwbfuwhfuwehf'
    #     }
    #     ]
    data = request.data
    print(data)
    old_images = data["oldImage"]
    images = data["images"]

    print(old_images)
    print(images)


    flag = 0 



    try:

        product = Product.objects.get(id=product_id)

    except:
        product = None 


    if product:

        #Fetching the product title

        product_title = product.title

        print(product_title)

        if int(len(old_images)) > 0:

            for i in range(len(old_images)):

                image_id = old_images[i]["id"]
                print(image_id)

                #Delete the product image
                try:
                    product_image = ProductImage.objects.get(id=image_id)
                except:
                    product_image = None 

                if product_image:

                    product_image.delete()
                    flag = 1
                    print("deleted")

                else:
                    flag = 0 
                    break


            if flag == 0:

                return JsonResponse({"success":False,"message":"The selected photos couild not be deleted"})

        else:
            flag = 0 

        print(flag)

            #Add the new images 

        # if int(len(images)) > 0:

        #     pass

        # else

        if int(len(images)) > 0:

            for i in range(int(len(images))):
                # print("dhuklam")
                #dataz = request.data
                #image_namez = dataz['title']

                try:
                    image_name = product_title + str(i) +".png"
                    # image = dataz['images['+str(i)+']']
                    image = images[i]
                    base_image=image.split(",")[1]
                    imgdata = base64.b64decode(str(base_image))
                    image = Image.open(io.BytesIO(imgdata))
                    width, height = image.size
                    # print(width,height)
                    # image_name = "file.png"
                    if width <= 475 and height <= 475:
                        # print("size thikase")
                        thumb_io = BytesIO() # create a BytesIO object
                        # print(type(image))
                        image.convert('RGB')
                        image.save(thumb_io, 'PNG', quality=85) # save image to BytesIO object
                        thumbnail = File(thumb_io, name=image_name)
                        image_data = {'product_image':image,'product_id':product_id}
                        product_image = ProductImage.objects.create(product_image=thumbnail,product_id=product_id)
                        product_image.save()
                        # print(product_image)
                    else:
                        thumb_io = BytesIO() # create a BytesIO object
                        # print(type(image))
                        image.convert('RGB')
                        # height,width = imz.size
                        imz=image.crop((0,0,width,height))
                        if height > 475:
                            top = (height - 475)/2
                            botom = 475+top
                            imz=image.crop((0,top,width,botom))
                        else:
                            imz=image.crop((0,0,width,height))
                        new_width,new_height = imz.size
                        # print("new height width", new_height, new_width)
                        if width > 475:
                            left = (new_width - 475)/2
                            right = 475+left
                            imz=imz.crop((left,0,right,new_height))
                        else:
                            imz=image.crop((0,0,new_width,new_height))
                        # print('width resize image before')
                        # imz.save("C://Users//K.M. FAIZULLAH\Desktop//Fuhad_all-works//09-11-2020//tango_ecomerce_child_backend//new_width_resize910.png")
                        # print("after width saving image")
                        # x_cordinate = int(width)/2
                        # y_corodinate = int(height)/2
                        # left = x_cordinate-237.5
                        # right = width-left
                        # top = height  - (y_corodinate+237.5)
                        # imz=image.crop(((x_cordinate- 237.5),(y_corodinate+ 237.5),(width- 237.5),(y_corodinate-237.5)))
                        height,width = imz.size
                        # print("after all resize", height,  width)
                        imz.save(thumb_io, 'PNG', quality=85) # save image to BytesIO object
                        thumbnail = File(thumb_io, name=image_name)
                        # print("here is the thumbnail", thumbnail)
                        # print("fihfgudsfhds")
                        # print(images)
                        # image_data = {'product_image':images,'product_id':product_id}
                        product_image = ProductImage.objects.create(product_image=thumbnail,product_id=product_id)
                        # print(product_image)
                        print(product_image)
                        product_image.save()
                        print("save hoise")


                except:
                    return JsonResponse({"success":False,"message":"The new images could not be uploaded"})




        else:
            pass


        return JsonResponse({"success":True,"message":"The selected photos are deleted and new photos are added"})


    else:

        return JsonResponse({"success":False,"message":"This product does not exist"})





@api_view (["GET",])
def nospecification_products(request):

    #Contains all the product ids

    try:
        all_products = Product.objects.all()

    except:
        all_products = None


    if all_products:

        product_ids = list(all_products.values_list('id',flat=True).distinct())

    else:
        product_ids = []

    #Constains all the product ids with specification
    try:
        all_prod_spec = ProductSpecification.objects.all()
    except:
        all_prod_spec = None 

    if all_prod_spec:

        prod_spec_ids = list(all_prod_spec.values_list('product_id',flat=True).distinct())

    else:
        prod_spec_ids = []

    #Removing those product ids with specification
    for i in range(len(prod_spec_ids)):

        if prod_spec_ids[i] in product_ids:
            product_ids.remove(prod_spec_ids[i])

    #Finding the products with no specifications
    try:
        prod_no_spec = Product.objects.filter(id__in=product_ids)

    except:
        prod_no_spec = None 


    if prod_no_spec:
        product_serializer = ProductPdfSerializer(prod_no_spec,many=True)
        return JsonResponse({"success":True,"message":"The data is shown.","data":product_serializer.data})

    else:
        return JsonResponse({"success":False,"message":"No data could be shown"})


        

#The products have specifications but no price
@api_view (["GET",])
def noprice_products(request):


    #Contains all the product ids

    try:
        all_products = Product.objects.all()

    except:
        all_products = None


    if all_products:

        product_ids = list(all_products.values_list('id',flat=True).distinct())

    else:
        product_ids = []

    #Contains all the specification ids

    try:
        all_prod_spec = ProductSpecification.objects.all()
    except:
        all_prod_spec = None 

    if all_prod_spec:

        specification_ids = list(all_prod_spec.values_list('id',flat=True).distinct())

    else:
        specification_ids = []


    #Contains all the specification ids that have prices
    try:
        spec_prices = ProductPrice.objects.all()
    except:
        spec_prices = None 

    if spec_prices:

        price_specification_ids = list(spec_prices.values_list('specification_id',flat=True).distinct())

    else:
        price_specification_ids = []

    #Removing the specification ids that have price

    for i in range(len(price_specification_ids)):
        if price_specification_ids[i] in specification_ids:
            specification_ids.remove(price_specification_ids[i])


    #Finding out the product ids that have specification but no price

    try:

        prod_specz = ProductSpecification.objects.filter(id__in = specification_ids)

    except:
        prod_specz = None 

    if prod_specz:

        specific_prod_ids = list(prod_specz.values_list('product_id',flat=True).distinct())

    else:
        specific_prod_ids = []


    #Finding out these specific product

    try:
        specific_prods = Product.objects.filter(id__in=specific_prod_ids)
    except:
        specific_prods = None 

    if specific_prods:

        product_serializer = ProductPdfSerializer(specific_prods,many=True)
        return JsonResponse({"success":True,"message":"The data is shown","data":product_serializer.data})

    else:
        return JsonResponse({"success":False,"message":"No data could be shown"})
        



@api_view(['GET',])
def publish_unpublish_specification(request,specification_id):

    try:

        product = ProductSpecification.objects.get(id=specification_id)

    except:

        product = None 

    if product:

        if product.specification_status == "Published":
            product.specification_status = "Pending"
            product.save()

        elif product.specification_status == "Pending":
            product.specification_status = "Published"
            product.save()



        return JsonResponse({'success':True, 'message':'This products status has been changed'})

    else:

        return JsonResponse({'success':False, 'message':'This product does not exist'})


@api_view(['GET',])
def publish_unpublish_product(request,product_id):

    try:

        product = Product.objects.get(id=product_id)

    except:

        product = None 

    if product:

        if product.product_status == "Published":
            product.product_status = "Pending"
            product.save()

        elif product.product_status == "Pending":
            product.product_status = "Published"
            product.save()



        return JsonResponse({'success':True, 'message':'This products status has been changed'})

    else:

        return JsonResponse({'success':False, 'message':'This product does not exist'})

    






    

