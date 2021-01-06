from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
import datetime
from difflib import SequenceMatcher
import json

from Intense.models import (
    Product, Order, Terminal,TerminalUsers,SpecificationPrice,subtraction_track,OrderDetails,CompanyInfo, ProductPrice, Userz,User,product_delivery_area,DeliveryLocation,DeliveryArea,
    BillingAddress, ProductPoint, ProductSpecification,ProductImage,SpecificationImage,
    user_relation, Cupons, Comment, CommentReply, Reviews,
    discount_product, Warehouse, Shop, WarehouseInfo, ShopInfo, WarehouseInfo,
    inventory_report, ProductBrand, ProductCode,DeliveryInfo,Invoice,Inventory_Price,inventory_report)
from Product_details.serializers import (DeliveryInfoSerializer,MotherSpecificationSerializer,MotherDeliveryInfoCreationSerializer,MaxMinSerializer,MaxMinSerializer1,MotherCodeCreationSerializer,MotherSpecificationCreationSerializer,MotherProductImageCreationSerializer, ChildProductCreationSerializer,MaxMinSerializer,ProductDeliveryAreaSerializer, TerminalSerializer,ProductPriceSerializer, ProductPointSerializer, ProductSpecificationSerializer,
                                         ProductSpecificationSerializerz,SSerializer,WSerializer,ProductDetailSerializer, ProductDetailSerializer1, ProductDetailSerializer2, CupponSerializer, ProductDiscountSerializer,
                                         WarehouseSerializer,ChildSpecificationPriceSerializer,SellerSpecificationSerializer,OwnSpecificationSerializer, ShopSerializer,InventoryReportSerializer, WarehouseInfoSerializer, ShopInfoSerializer, NewWarehouseInfoSerializer, AddBrandSerializer, ProductSpecificationSerializer1)
from Product.serializers import ProductCodeSerializer
from User_details.serializers import UserSerializerz
from Cart.serializers import OrderDetailsSerializer, OrderSerializer,InvoiceSerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from Intense.Integral_apis import (
    create_product_code,category1_data_upload
)
from datetime import datetime
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from django.utils import timezone
import requests
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
from colour import Color
from rest_framework.response import Response
from django.contrib.sites.models import Site
from datetime import date
from Intense.Integral_apis import create_user_balance,create_user_profile
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from PIL import Image
import requests
from io import BytesIO
# import urllib2
from PIL import Image, ImageFile    


site_path = "http://127.0.0.1:7000/"

own_site_path = "http://127.0.0.1:8000/"
#site_path = "https://eshoppingmall.com.bd/"
#site_path = "http://188.166.240.77:8080/"

current = date.today()
@api_view(['POST', ])
def get_colors(request, product_id):

    variant = request.data.get('variant')

    try:

        product = Product.objects.get(id=product_id)

    except:

        product = None

    if product:

        print("product ase")

        try:

            product_spec = ProductSpecification.objects.filter(
                product_id=product_id, weight_unit=variant,specification_status="Published")

        except:

            product_spec = None

        if product_spec:

            print("speciifcation ase")

            product_colors = list(product_spec.values_list(
                'color', flat=True).distinct())

        else:

            product_colors = []

    else:

        product_colors = []

    return JsonResponse({'success': True, 'colors': product_colors})


@api_view(['POST', ])
def get_sizes(request, product_id):

    variant = request.data.get('variant')
    color = request.data.get('color')

    try:

        product = Product.objects.get(id=product_id)

    except:

        product = None

    if product:

        print("product ase")

        try:

            product_spec = ProductSpecification.objects.filter(
                product_id=product_id, weight_unit=variant, color=color,specification_status="Published")

        except:

            product_spec = None

        if product_spec:

            print("speciifcation ase")

            product_colors = list(product_spec.values_list(
                'size', flat=True).distinct())

        else:

            product_colors = []

    else:

        product_colors = []

    return JsonResponse({'success': True, 'sizes': product_colors})


# @api_view(['POST', ])
# def get_spec_info(request, product_id):

#     variant = request.data.get('variant')
#     color = request.data.get('color')
#     size = request.data.get('size')

#     print(variant)
#     print(color)
#     print(size)

#     try:

#         product = Product.objects.get(id=product_id)

#     except:

#         product = None

#     if product:

#         print("product ase")

#         try:

#             product_spec = ProductSpecification.objects.filter(
#                 product_id=product_id, weight_unit=variant, color=color, size=size,specification_status="Published").first()




#         except:

#             product_spec = None


#         print(product_spec)

#         if product_spec:

#             print("speciifcation ase")

#             spec_serializer = ProductSpecificationSerializer1(
#                 product_spec, many=False)
#             prod_data = spec_serializer.data

#         else:

#             prod_data = {}

#     else:

#         prod_data = {}

#     return JsonResponse({'success': True, 'specification': prod_data})


@api_view(['POST', ])
def get_spec_info(request, product_id):

    variant = request.data.get('variant')
    color = request.data.get('color')
    size = request.data.get('size')

    print(variant)
    print(color)
    print(size)

    try:

        product = Product.objects.get(id=product_id)

    except:

        product = None

    if product:

        print("product ase")

        try:

            product_spec = ProductSpecification.objects.filter(
                product_id=product_id, weight_unit=variant, color=color, size=size,specification_status="Published").first()




        except:

            product_spec = None


        print(product_spec)

        if product_spec:

            specification_id = product_spec.id

            print("speciifcation ase")
            print(product_spec.is_own)

            if product_spec.is_own == True:

                print("amar nijer product")

                spec_serializer = ProductSpecificationSerializer1(
                    product_spec, many=False)
                prod_data = spec_serializer.data

            else:
                spec_serializer = ProductSpecificationSerializer1(
                    product_spec, many=False)
                prod_data = spec_serializer.data
                print("fbdwsufbdufbdufbgdu")
                print(prod_data)

                url = own_site_path + "productdetails/not_own_quantity_check/" +str(specification_id)+ "/"
                own_response = requests.get(url = url)
                own_response = own_response.json()
                print(own_response)
                if own_response["success"] == True:
                    #update the quantity
                    prod_data["quantity"] = own_response["quantity"]

                url2 = own_site_path + "productdetails/check_price/" +str(specification_id)+ "/"
                own_response2 = requests.get(url = url2)
                own_response2 = own_response2.json()
                print(own_response2)
                if own_response2["success"] == False:
                    product_spec.on_hold = True
                    product_spec.save()
                    prod_data["on_hold"] = True
                    




        else:

            prod_data = {}

    else:

        prod_data = {}

    return JsonResponse({'success': True, 'specification': prod_data})



@api_view(['POST', ])
def color_size(request, product_id):

    try:

        product = Product.objects.get(id=product_id)

    except:

        product = None

    if product:

        product_spec = ProductSpecification.objects.filter(
            product_id=product_id) & ProductSpecification.objects.filter(quantity__gte=1)

        product_colors = list(product_spec.values_list(
            'color', flat=True).distinct())

        return JsonResponse({'success': True, 'message': 'The colors are shown', 'colors': product_colors})

    else:

        product_colors = []

        return JsonResponse({'success': False, 'message': 'The colors are not shown', 'colors': product_colors})


@api_view(['POST', ])
def available_sizes(request, product_id):

    color = request.data.get("color")

    try:

        product = Product.objects.get(id=product_id)

    except:

        product = None

    if product:

        product_spec = ProductSpecification.objects.filter(product_id=product_id) & ProductSpecification.objects.filter(
            color=color) & ProductSpecification.objects.filter(quantity__gte=1)

        product_sizes = list(product_spec.values_list(
            'size', flat=True).distinct())

        product_quantities = list(
            product_spec.values_list('quantity', flat=True))

        dic = {}

        for i in range(len(product_sizes)):

            item = {product_sizes[i]: product_quantities[i]}

            dic.update(item)

        return JsonResponse({'success': True, 'message': 'The colors are shown', 'sizes': product_sizes, 'quantities': dic})

    else:

        product_sizes = []

        return JsonResponse({'success': False, 'message': 'The colors are not shown', 'sizes': product_sizes})


@api_view(['POST', ])
def add_points(request):

    if request.method == 'POST':
        pointserializer = ProductPointSerializer(data=request.data)
        if pointserializer.is_valid():
            pointserializer.save()
            return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(pointserializer.errors)


# This updates the product points
@api_view(['POST', ])
def update_points(request, product_id):

    try:
        product = ProductPoint.objects.filter(product_id=product_id).last()

        if request.method == 'POST':
            pointserializer = ProductPointSerializer(
                product, data=request.data)
            if pointserializer.is_valid():
                pointserializer.save()
                return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(pointserializer.errors)

    except ProductPoint.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)


# This updates the product points
@api_view(['POST', ])
def delete_points(request, product_id):

    try:
        product = ProductPoint.objects.filter(product_id=product_id)

        if request.method == 'POST':
            product.delete()

            return JsonResponse({'message': 'The product points have been deleted'})

    except ProductPoint.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)


# This adds the current product price
@api_view(['POST', ])
def add_price(request):

    if request.method == 'POST':
        pointserializer = ProductPriceSerializer(data=request.data)
        if pointserializer.is_valid():
            pointserializer.save()
            return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(pointserializer.errors)


# This updates the current product price
@api_view(['POST', ])
def update_price(request, product_id):

    try:
        product = ProductPrice.objects.filter(product_id=product_id).last()

        if request.method == 'POST':
            pointserializer = ProductPriceSerializer(
                product, data=request.data)
            if pointserializer.is_valid():
                pointserializer.save()
                return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(pointserializer.errors)

    except ProductPrice.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)


# This updates the product points
@api_view(['POST', ])
def delete_price(request, product_id):

    try:
        product = ProductPrice.objects.filter(product_id=product_id)

        if request.method == 'POST':
            product.delete()

            return JsonResponse({'message': 'The product prices have been deleted'})

    except ProductPoint.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)


# This adds product points
@api_view(['POST', ])
def add_specification(request):

    if request.method == 'POST':
        pointserializer = ProductSpecificationSerializer(data=request.data)

        if pointserializer.is_valid():
            pointserializer.save()
            return JsonResponse({'success': True, 'message': 'Data is shown below', 'data': pointserializer.data}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'success': False, 'message': 'Data could not be inserted', 'data': {}})


# This updates the latest product specification
@api_view(['POST', ])
def update_specification(request, product_id):

    try:
        product = ProductSpecification.objects.filter(
            product_id=product_id).last()

        if request.method == 'POST':
            pointserializer = ProductSpecificationSerializer(
                product, data=request.data)
            if pointserializer.is_valid():
                pointserializer.save()
                return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
            return Response(pointserializer.errors)

    except ProductPoint.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)


# This deletes the product specification
@api_view(['POST', ])
def delete_specification(request, product_id):

    try:
        product = ProductSpecification.objects.filter(product_id=product_id)

        if request.method == 'POST':
            product.delete()

            return JsonResponse({'message': 'The product specification have been deleted'})

    except ProductPoint.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', ])
def show_specification(request, product_id):

    try:
        title = Product.objects.get(id=product_id)
    except:
        title = None
    if title:
        product_title = title.title
    else:
        product_title = ''

    try:

        product = ProductSpecification.objects.filter(product_id=product_id,admin_status="Confirmed")

    except:

        product = None

    if product:

        productserializer = ProductSpecificationSerializer1(product, many=True)
        data = productserializer.data

    else:

        data = {}

    return JsonResponse({
        'success': True,
        'message': 'Data is shown below',
        'product_title': product_title,
        'data': data

    })



@api_view(['GET', ])
def show_seller_specification(request, product_id):

    try:
        title = Product.objects.get(id=product_id)
    except:
        title = None
    if title:
        product_title = title.title
    else:
        product_title = ''

    try:

        product = ProductSpecification.objects.filter(product_id=product_id)

    except:

        product = None

    if product:

        productserializer = ProductSpecificationSerializer1(product, many=True)
        data = productserializer.data

    else:

        data = {}

    return JsonResponse({
        'success': True,
        'message': 'Data is shown below',
        'product_title': product_title,
        'data': data

    })


# @api_view(['POST',])
# def add_spec(request,product_id):


#     specification_data_value ={

#             'product_id': product_id,
#             'color': request.data.get("color"),
#             'size': request.data.get("size"),
#             'weight': request.data.get("weight"),
#             'warranty':request.data.get("warranty"),
#             'warranty_unit':request.data.get("warranty_unit"),
#             'unit':request.data.get("product_unit"),

#         }

#     product_price ={
#         'product_id': product_id,
#         'price' : request.data.get("price"),
#         'purchase_price': request.data.get("purchase_price"),
#         #'currency_id': request.data.get('currency_id')
#     }

#     product_discount ={

#         'product_id': product_id,
#         'amount': request.data.get("discount_amount"),
#         'discount_type': request.data.get("discount_type"),
#         #'start_date' : '2020-09-05',
#         #'end_date' : data['discount_end_date']
#         'start_date': request.data.get("discount_start_date"),
#         'end_date': request.data.get("discount_end_date")
#     }

#     product_point ={
#         'product_id': product_id,
#         'point': request.data.get("point_amount"),
#         # 'end_date': data['point_end_date']
#         'start_date': request.data.get("point_start_date"),
#         'end_date': request.data.get("point_end_date")
#     }

#     delivery_info = {
#         'height': request.data.get("delivery_height"),
#         'width': request.data.get("delivery_width"),
#         'length': request.data.get("delivery_length"),
#         'weight': request.data.get("delivery_weight"),
#         'measument_unit': request.data.get("delivery_product_unit"),
#         'charge_inside': request.data.get("delivery_inside_city_charge"),
#         'charge_outside': request.data.get("delivery_outside_city_charge"),
#     }

#     print("delivery Info", delivery_info)
#     if request.method == 'POST':
#         flag = 0
#         spec={}
#         price={}
#         discount= {}
#         point={}
#         delivery={}
#         try:
#             product_spec= ProductSpecificationSerializer(data=specification_data_value)
#             if product_spec.is_valid():
#                 product_spec.save()
#                 spec.update(product_spec.data)

#             else:
#                 flag= flag+1

#             product_price.update({'specification_id':spec['id']})
#             product_price=ProductPriceSerializer (data = product_price)
#             if product_price.is_valid():
#                 product_price.save()
#                 price.update(product_price.data)
#             else:
#                 flag= flag+1

#             if product_discount['discount_type'] is None:
#                 discount={}
#             else:
#                 product_discount.update({'specification_id':spec['id']})
#                 product_dis = ProductDiscountSerializer (data = product_discount)
#                 if product_dis.is_valid():
#                     product_dis.save()
#                     discount.update(product_dis.data)
#                 else:
#                     flag= flag+1

#             product_point.update({'specification_id':spec['id']})
#             product_point_value= ProductPointSerializer (data=product_point)
#             if product_point_value.is_valid():
#                 product_point_value.save()
#                 point.update(product_point_value.data)
#             else:
#                 flag= flag+1


#             delivery_info.update({'specification_id':spec['id']})
#             delivery_value= DeliveryInfoSerializer (data=delivery_info)
#             if delivery_value.is_valid():
#                 delivery_value.save()
#                 delivery.update(delivery_value.data)
#             else:
#                 flag= flag+1


#             if flag>0:
#                 return JsonResponse ({
#                         "success": False,
#                         "message": "Something went wrong !!",
#                     })
#             else:
#                 return JsonResponse ({
#                         "success": True,
#                         "message": "Specification data has been inserted Successfully",
#                         "specification": spec,
#                         "price":price,
#                         "discount": discount,
#                         "point": point,
#                         "delivery": delivery
#                     })

#         except:
#             return JsonResponse ({
#                 "success": False,
#                 "message": "Something went wrong !!"
#             })

# @api_view(['POST', 'GET'])
# def edit_spec(request, specification_id):
    
#     current_date = date.today()

#     print("current_date")
#     print(current_date)
#     current_date = str(current_date)

#     print(request.data)

#     print(specification_id)

#     try:
#         product_spec = ProductSpecification.objects.get(id=specification_id)
#     except:

#         product_spec = None

#     if product_spec:

#         product_id = product_spec.product_id

#     else:
#         product_id = 0

#     print(product_id)

#     if request.method == 'POST':

#         vat = request.data.get("vat")
#         if vat == "":

#             vat = 0.00

#         specification_data_value = {

#             'product_id': product_id,
#             'color': request.data.get("color"),
#             'size': request.data.get("size"),
#             'weight': request.data.get("weight"),
#             'warranty': request.data.get("warranty"),
#             'warranty_unit': request.data.get("warranty_unit"),
#             'unit': request.data.get("product_unit"),
#             'vat': vat,

#         }

#         # price = request.data.get("price")

#         # if price == "":
#         #     price = 0.00

#         # purchase_price = request.data.get("purchase_price")

#         # if purchase_price == "":
#         #     purchase_price = 0.00

#         # product_price = {
#         #     'product_id': product_id,
#         #     'price': price,
#         #     'specification_id': specification_id,
#         #     'purchase_price': purchase_price
#         #     # 'currency_id': request.data.get('currency_id')
#         # }

#         discount_type = request.data.get("discount_type")

#         if discount_type == "none":

#             print("dhbfdufbrewyfbrewyfgryfregfbyrefbreyfbryfb")

#             product_discount = {

#                 'product_id': product_id,
#                 'specification_id': specification_id,
#                 'amount': 0.00,
#                 'discount_type': discount_type,
#                 # 'start_date' : '2020-09-05',
#                 # 'end_date' : data['discount_end_date']
#                 'start_date': current_date,
#                 'end_date': current_date
#             }

#             print(product_discount)

#         else:

#             discount_amount = request.data.get("discount_amount")
#             if discount_amount == "":
#                 discount_amount = 0.00

#             discount_end_date = request.data.get("discount_end_date")
#             if discount_end_date == "":

#                 discount_end_date = current_date


#             print(discount_end_date)

#             discount_start_date = request.data.get("discount_start_date")
#             if discount_start_date == "":
#                 discount_start_date = current_date

#             print(discount_start_date)

#             product_discount = {

#                 'product_id': product_id,
#                 'amount': discount_amount,
#                 'discount_type': discount_type,
#                 # 'start_date' : '2020-09-05',
#                 # 'end_date' : data['discount_end_date']
#                 'start_date': discount_start_date,
#                 'specification_id': specification_id,
#                 'end_date': discount_end_date
#             }

#             print("discounttt")

#             print(product_discount)

#         point_amount = request.data.get("point_amount")
#         if point_amount == "":
#             point_amount = 0.00

#         point_end_date = request.data.get("point_end_date")
#         if point_end_date == "":
#             point_end_date = current_date

#         point_start_date = request.data.get("point_start_date")
#         if point_start_date == "":
#             point_start_date = current_date

#         product_point = {
#             'product_id': product_id,
#             'point': point_amount,
#             # 'end_date': data['point_end_date']
#             'start_date': point_start_date,
#             'specification_id': specification_id,
#             'end_date': point_end_date
#         }

#         delivery_height = request.data.get("delivery_height")
#         if delivery_height == "":
#             delivery_height = 0.0

#         delivery_width = request.data.get("delivery_width")
#         if delivery_width == "":
#             delivery_width = 0.0

#         delivery_length = request.data.get("delivery_length")
#         if delivery_length == "":
#             delivery_length = 0.0

#         delivery_weight = request.data.get("delivery_weight")
#         if delivery_weight == "":
#             delivery_weight = 0.0

#         delivery_inside = request.data.get("delivery_inside_city_charge")
#         if delivery_inside == "":
#             delivery_inside = 0

#         delivery_outside = request.data.get("delivery_outside_city_charge")
#         if delivery_outside == "":
#             delivery_outside = 0

#         delivery_info = {
#             'height': delivery_height,
#             'width': delivery_width,
#             'length': delivery_length,
#             'weight': delivery_weight,
#             'measument_unit': request.data.get("delivery_product_unit"),
#             'charge_inside': delivery_inside,
#             'specification_id': specification_id,
#             'charge_outside': delivery_outside
#         }

#         try:

#             try:

#                 spec = ProductSpecification.objects.get(id=specification_id)

#             except:
#                 spec = None

#             if spec:
#                 specification_serializer = ProductSpecificationSerializer(
#                     spec, data=specification_data_value)
#                 if specification_serializer.is_valid():
#                     print("spec save hochche")
#                     specification_serializer.save()
#                     values = specification_serializer.data
#             else:
#                 return Response({'success': False, 'message': 'Product Specification could not be updated'})

#             # try:
#             #     price = ProductPrice.objects.get(
#             #         specification_id=specification_id)
#             # except:
#             #     price = None

#             # if price:
#             #     price_serializer = ProductPriceSerializer(
#             #         price, data=product_price)

#             #     if price_serializer.is_valid():
#             #         price_serializer.save()
#             #         print("price save hochche")
#             #         price_data = price_serializer.data

#             # else:
#             #     return Response({'success': False, 'message': 'Product Price could not be updated'})

#             try:
#                 points = ProductPoint.objects.get(
#                     specification_id=specification_id)
#             except:
#                 points = None


#             print(points)

#             if points:
#                 point_serial = ProductPointSerializer(
#                     points, data=product_point)
#                 if point_serial.is_valid():
#                     print("pOINT SAVE HOCHCHE")
#                     point_serial.save()
#                     point_data = point_serial.data

#                 else:
#                     print(point_serial.errors)

#             else:
#                 point_serial = ProductPointSerializer(data=product_point)
#                 if point_serial.is_valid():
#                     print("pOINT SAVE HOCHCHE")
#                     point_serial.save()
#                     point_data = point_serial.data
#                 else:
#                     print(point_serial.errors)

#             try:
#                 delivery = DeliveryInfo.objects.get(
#                     specification_id=specification_id)
#             except:
#                 delivery = None

#             if delivery:
#                 delivery_serial = DeliveryInfoSerializer(
#                     delivery, data=delivery_info)

#                 if delivery_serial.is_valid():

#                     delivery_serial.save()
#                     print("delivery hocchche")
#                     delivery_data = delivery_serial.data
#                 else:
#                     delivery_serial = DeliveryInfoSerializer(
#                         data=delivery_info)

#                     if delivery_serial.is_valid():

#                         delivery_serial.save()
#                         print("delivery hocchche")
#                         delivery_data = delivery_serial.data

#             try:
#                 discount = discount_product.objects.get(
#                     specification_id=specification_id)
#             except:
#                 discount = None

#             if discount:
#                 discount_serializer = ProductDiscountSerializer(
#                     discount, data=product_discount)
#                 if discount_serializer.is_valid():
#                     print("discount save hochche")
#                     discount_serializer.save()
#                     discount_data = discount_serializer.data
#             else:
#                 discount_serializer = ProductDiscountSerializer(
#                     data=product_discount)
#                 if discount_serializer.is_valid():
#                     print("discount save hochche")
#                     discount_serializer.save()
#                     discount_data = discount_serializer.data

#             return Response({'success': True, 'message': 'Edit is successful'})

#         except:
#             return Response({'success': False, 'message': 'Something went wrong !!'})



@api_view(['POST', 'GET'])
def edit_spec(request, specification_id):
    
    current_date = date.today()

    print("current_date")
    print(current_date)
    current_date = str(current_date)

    print(request.data)

    print(specification_id)

    try:
        product_spec = ProductSpecification.objects.get(id=specification_id)
    except:

        product_spec = None

    if product_spec:

        product_id = product_spec.product_id

    else:
        product_id = 0

    print(product_id)

    if request.method == 'POST':

        vat = request.data.get("vat")
        if vat == "":

            vat = 0.00

        specification_data_value = {

            'product_id': product_id,
            'color': request.data.get("color"),
            'size': request.data.get("size"),
            'weight': request.data.get("weight"),
            'warranty': request.data.get("warranty"),
            'warranty_unit': request.data.get("warranty_unit"),
            'unit': request.data.get("product_unit"),
            'vat': vat,
            'is_own' :True

        }

        # price = request.data.get("price")

        # if price == "":
        #     price = 0.00

        # purchase_price = request.data.get("purchase_price")

        # if purchase_price == "":
        #     purchase_price = 0.00

        # product_price = {
        #     'product_id': product_id,
        #     'price': price,
        #     'specification_id': specification_id,
        #     'purchase_price': purchase_price
        #     # 'currency_id': request.data.get('currency_id')
        # }

        discount_type = request.data.get("discount_type")

        if discount_type == "none":

            

            product_discount = {

                'product_id': product_id,
                'specification_id': specification_id,
                'amount': 0.00,
                'discount_type': discount_type,
                # 'start_date' : '2020-09-05',
                # 'end_date' : data['discount_end_date']
                'start_date': current_date,
                'end_date': current_date
            }

           

        else:

            discount_amount = request.data.get("discount_amount")
            if discount_amount == "":
                discount_amount = 0.00
                
            if discount_amount == None:
                discount_amount = 0.00

            discount_end_date = request.data.get("discount_end_date")
            if discount_end_date == "":
                discount_end_date = current_date
                
            if discount_end_date == None:
                discount_end_date = current_date
                
            



            discount_start_date = request.data.get("discount_start_date")
            if discount_start_date == "":
                discount_start_date = current_date
                
                
            if discount_start_date == None:
                discount_start_date = current_date
                
                


            product_discount = {

                'product_id': product_id,
                'amount': discount_amount,
                'discount_type': discount_type,
                # 'start_date' : '2020-09-05',
                # 'end_date' : data['discount_end_date']
                'start_date': discount_start_date,
                'specification_id': specification_id,
                'end_date': discount_end_date
            }



        point_amount = request.data.get("point_amount")
        if point_amount == "":
            point_amount = 0.00
            
        if point_amount == None:
            point_amount = 0.00

        point_end_date = request.data.get("point_end_date")
        if point_end_date == "":
            point_end_date = current_date
            
        if point_end_date == None:
            point_end_date = current_date
            
        

        point_start_date = request.data.get("point_start_date")
        if point_start_date == "":
            point_start_date = current_date
            
        if point_start_date == None:
            point_start_date = current_date

        product_point = {
            'product_id': product_id,
            'point': point_amount,
            # 'end_date': data['point_end_date']
            'start_date': point_start_date,
            'specification_id': specification_id,
            'end_date': point_end_date
        }
    

        delivery_height = request.data.get("delivery_height")
        if delivery_height == "":
            delivery_height = 0.0

        delivery_width = request.data.get("delivery_width")
        if delivery_width == "":
            delivery_width = 0.0

        delivery_length = request.data.get("delivery_length")
        if delivery_length == "":
            delivery_length = 0.0

        delivery_weight = request.data.get("delivery_weight")
        if delivery_weight == "":
            delivery_weight = 0.0

        # delivery_inside = request.data.get("delivery_inside_city_charge")
        # if delivery_inside == "":
        #     delivery_inside = 0

        # delivery_outside = request.data.get("delivery_outside_city_charge")
        # if delivery_outside == "":
        #     delivery_outside = 0

        # delivery_info = {
        #     'height': delivery_height,
        #     'width': delivery_width,
        #     'length': delivery_length,
        #     'weight': delivery_weight,
        #     'measument_unit': request.data.get("delivery_product_unit"),
        #     'charge_inside': delivery_inside,
        #     'specification_id': specification_id,
        #     'charge_outside': delivery_outside
        # }
        
        delivery_info = {
        'height': request.data.get("delivery_height"),
        'width': request.data.get("delivery_width"),
        'length': request.data.get("delivery_length"),
        'weight': request.data.get("delivery_weight"),
        'measument_unit': request.data.get("delivery_product_unit"),
        'delivery_free': request.data.get("delivery_free"),
        }

        try:

            try:

                spec = ProductSpecification.objects.get(id=specification_id)

            except:
                spec = None

            if spec:
                specification_serializer = ProductSpecificationSerializer(
                    spec, data=specification_data_value)
                if specification_serializer.is_valid():
                    print("spec save hochche")
                    specification_serializer.save()
                    values = specification_serializer.data
            else:
                return Response({'success': False, 'message': 'Product Specification could not be updated'})

            # try:
            #     price = ProductPrice.objects.get(
            #         specification_id=specification_id)
            # except:
            #     price = None

            # if price:
            #     price_serializer = ProductPriceSerializer(
            #         price, data=product_price)

            #     if price_serializer.is_valid():
            #         price_serializer.save()
            #         print("price save hochche")
            #         price_data = price_serializer.data

            # else:
            #     return Response({'success': False, 'message': 'Product Price could not be updated'})

            try:
                points = ProductPoint.objects.get(
                    specification_id=specification_id)
            except:
                points = None


            

            if points:
                point_serial = ProductPointSerializer(
                    points, data=product_point)
                if point_serial.is_valid():
                    
                    point_serial.save()
                    point_data = point_serial.data

                else:
                    pass
              

            else:
                point_serial = ProductPointSerializer(data=product_point)
                if point_serial.is_valid():
                    
                    point_serial.save()
                    point_data = point_serial.data
                else:
                    print("point2")
                    print(point_serial.errors)

            try:
                delivery = DeliveryInfo.objects.get(
                    specification_id=specification_id)
            except:
                delivery = None

            if delivery:
                delivery_serial = DeliveryInfoSerializer(
                    delivery, data=delivery_info)

                if delivery_serial.is_valid():

                    delivery_serial.save()
                    
                    delivery_data = delivery_serial.data
                else:
                    delivery_serial = DeliveryInfoSerializer(
                        data=delivery_info)

                    if delivery_serial.is_valid():

                        delivery_serial.save()
                        
                        delivery_data = delivery_serial.data

            try:
                discount = discount_product.objects.get(
                    specification_id=specification_id)
            except:
                discount = None

            if discount:
                discount_serializer = ProductDiscountSerializer(
                    discount, data=product_discount)
                if discount_serializer.is_valid():
                    
                    discount_serializer.save()
                    discount_data = discount_serializer.data
            else:
                discount_serializer = ProductDiscountSerializer(
                    data=product_discount)
                if discount_serializer.is_valid():
                    
                    discount_serializer.save()
                    discount_data = discount_serializer.data
                    
                    
            data_val = {
                'option' : request.data.get("delivery_option"),
                'spec': specification_id,
                # 'arrayForDelivery': [
                #     {
                #         'selectedDistrict': 'Dhaka',
                #         'selectedThana':[
                #             'Banani',
                #             'Gulshan',
                #             'Rampura',
                #             'Dhanmondi'
                #         ]
                #     },
                #     {
                #         'selectedDistrict': 'Barishal',
                #         'selectedThana':[
                #             'Hizla',
                #             'Muladi',
                #             'Borguna',
                #             'Betagi'
                #         ]
                #     }
                # ]
                'arrayForDelivery': request.data.get("arrayForDelivery")
                    
            }
            
            print("values for specification")
            
            print(data_val)

            # print("before calling method")
            value = add_delivery_data1(data_val)
            print(value)

            return Response({'success': True, 'message': 'Edit is successful'})

        except:
            return Response({'success': False, 'message': 'Something went wrong !!'})

# @api_view(['POST',])
# def edit_spec(request,specification_id):


#     try:

#         spec = ProductSpecification.objects.get(id=specification_id)

#     except:
#         spec = None

#     if spec:
#         pointserializer = ProductSpecificationSerializer(spec,data=request.data)

#         if pointserializer.is_valid():
#             pointserializer.save()
#             return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
#         return Response (pointserializer.errors)


# @api_view(['POST', 'GET'])
# def delete_spec(request, specification_id):
#     if request.method == 'POST':
#         try:
#             product_price = ProductPrice.objects.filter(
#                 specification_id=specification_id)
#             if product_price.exists():

#                 product_price.delete()

#             product_discount = discount_product.objects.filter(
#                 specification_id=specification_id)
#             if product_discount.exists():
#                 product_discount.delete()

#             product_point = ProductPoint.objects.filter(
#                 specification_id=specification_id)
#             if product_point.exists():
#                 product_point.delete()

#             Delivery_info = DeliveryInfo.objects.filter(
#                 specification_id=specification_id)
#             if Delivery_info.exists():
#                 Delivery_info.delete()

#             spec = ProductSpecification.objects.filter(id=specification_id)
#             if spec.exists():
#                 spec.delete()
#             return JsonResponse({
#                 'success': True,
#                 'message': 'The product specification have been deleted'})
#         except:
#             return JsonResponse({
#                 'success': False,
#                 'message': 'The product specification could not be deleted'})

@api_view(['POST', 'GET'])
def delete_spec(request, specification_id):
    if(request.method == "POST"):
        try:
            price = ProductPrice.objects.filter(specification_id= specification_id)
            price.delete()
            points = ProductPoint.objects.filter(specification_id=specification_id)
            points.delete()
            discount = discount_product.objects.filter(specification_id=specification_id)
            discount.delete()
            code = ProductCode.objects.filter(specification_id = specification_id)
            code.delete()
            invenprice = Inventory_Price.objects.filter(specification_id=specification_id)
            invenprice.delete()
            warehouseinfo = WarehouseInfo.objects.filter(specification_id=specification_id)
            warehouseinfo.delete()
            shopinfo = ShopInfo.objects.filter(specification_id=specification_id)
            shopinfo.delete()
            invenrep = inventory_report.objects.filter(specification_id=specification_id)
            invenrep.delete()
            deliveryinfo = DeliveryInfo.objects.filter(specification_id=specification_id)
            deliveryinfo.delete()
            subtract = subtraction_track.objects.filter(specification_id=specification_id)
            subtract.delete()
            deliveryarea = product_delivery_area.objects.filter(specification_id=specification_id)
            deliveryarea.delete()
            specimage = SpecificationImage.objects.filter(specification_id=specification_id)
            specimage.delete()
            orderdetail = OrderDetails.objects.filter(specification_id=specification_id)
            orderdetail.delete()
            prospec = ProductSpecification.objects.filter(id=specification_id)
            prospec.delete()
            return Response({
                'success': True,
                'message': 'data has been deleted successfully !!'
            })
        except:
            return Response({
                'success':False,
                'Message': 'Some internal problem occurs while deleting the value'
                })

@api_view(['GET', ])
def show(request, product_id):

    #url = reverse('product_price_point_specification:showspec',args=[product_id])
    #data= requests.get(url)
    #url= reverse('product_price_point_specification:showspec',args=[product_id])
    #main = str(settings.BASE_DIR) + url
    # print(main)
    #data = requests.get(main)
    url = request.build_absolute_uri(
        reverse('product_price_point_specification:showspec', args=[product_id]))
    # print("------")
    # print(url)
    data = requests.get(url)
    return HttpResponse(data)


# This changes the comments,replies,reviews and order tables
@api_view(['POST', ])
def transfer(request, user_id):
    # Here userid provided is the newly verified userid
    try:

        existing_user = user_relation.objects.filter(
            verified_user_id=user_id).last()
        print(existing_user)

    except:
        existing_user = None

    if existing_user is not None:
        # Change the ids in the certain table

        # print(type(existing_user.verified_user_id))
        # print(existing_user.non_verified_user_id)
        user_id = existing_user.verified_user_id
        non_verified_user_id = existing_user.non_verified_user_id

        # Update all the order tables

        orders = Order.objects.filter(non_verified_user_id=non_verified_user_id).update(
            user_id=user_id, non_verified_user_id=None)

        # Update the Billing address

        billing_address = BillingAddress.objects.filter(
            non_verified_user_id=non_verified_user_id).update(user_id=user_id, non_verified_user_id=None)

        # Update the comment,reply and review tables

        comments = Comment.objects.filter(non_verified_user_id=non_verified_user_id).update(
            user_id=user_id, non_verified_user_id=None)
        reply = CommentReply.objects.filter(non_verified_user_id=non_verified_user_id).update(
            user_id=user_id, non_verified_user_id=None)
        reviews = Reviews.objects.filter(non_verified_user_id=non_verified_user_id).update(
            user_id=user_id, non_verified_user_id=None)

        return JsonResponse({'message': 'The user does exist'})

    else:
        return JsonResponse({'message': 'The user does not exist'})


@api_view(['GET', ])
def product_detail(request, product_id):

    try:
        product = Product.objects.filter(id=product_id).last()

    except:
        product = None

    if product is not None:

        product_serializer = ProductDetailSerializer2(product, many=False)
        return JsonResponse({'success': True, 'message': 'The data is shown below', 'data': product_serializer.data}, safe=False)

    else:
        return JsonResponse({'success': False, 'message': 'This product does not exist', 'data':{}})


# --------------------------------- Product Cupon -------------------------------

@api_view(["GET", "POST"])
def insert_cupon(request):
    '''
    This is for inserting cupon code into the databse. Admin will set the cupon code and it will apear to the users while buying a product.
    Calling http://127.0.0.1:8000/cupons/create_cupon/ will cause to invoke this Api. This Api just have Post response.

    Post Response:
        cupon_code : This is a character field. This will be cupon named after the inserting name value.
        amount : This will be the amount which will be deducted from the user payable balance.
        start_from: This is DateField. It will be created automatically upon the creation of a cupon.
        valid_to: This is another DateField. While creating a cupon admin will set the date.
        is_active : This is a BooleanField. This will indicate wheather the cupon is active or not. Using this data, cupon can be deactivated before ending
                    the validation time. 

    '''
    if(request.method == "POST"):
        serializers = CupponSerializer(data=request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors)


@api_view(["GET", "POST"])
def get_all_cupons(request):
    '''
    This is for getting all the cupons. Calling http://127.0.0.1:8000/cupons/all_cupon/ will cause to invoke this Api. 
    The Get Response will return following structured datas.

    Get Response:
        [
            {
                "id": 2,
                "cupon_code": "30% Off",
                "amount": 50.0,
                "start_from": "2020-08-27",
                "valid_to": "2020-09-30",
                "is_active": false
            },
            {
                "id": 3,
                "cupon_code": "25 Taka Off",
                "amount": 25.0,
                "start_from": "2020-08-27",
                "valid_to": "2020-10-27",
                "is_active": false
            }
        ]
    '''
    if(request.method == "GET"):
        queryset = Cupons.objects.all()
        serializers = CupponSerializer(queryset, many=True)
        return Response(serializers.data)


@api_view(["GET", "POST"])
def update_specific_cupons(request, cupon_id):
    '''
    This is for updating a particular cupon. Calling http://127.0.0.1:8000/cupons/update_cupon/4/ will cause to invoke this Api.
    While calling this Api, as parameters cupon id must need to be sent.

    After updating expected Post Response:
        {
            "id": 4,
            "cupon_code": "25 Taka Off",
            "amount": 25.0,
            "start_from": "2020-08-27",
            "valid_to": "2020-10-27",
            "is_active": true
        }
    '''

    try:
        cupon = Cupons.objects.get(pk=cupon_id)
    except:
        return Response({'Message': 'Check wheather requested data exists or not'})

    if(request.method == "GET"):
        cupon_serializer = CupponSerializer(cupon, many=False)
        return Response(cupon_serializer.data)

    elif(request.method == "POST"):
        Cupon_serializers = CupponSerializer(cupon, data=request.data)
        if(Cupon_serializers.is_valid()):
            Cupon_serializers.save()
            return Response(Cupon_serializers.data, status=status.HTTP_201_CREATED)
        return Response(Cupon_serializers.errors)


@api_view(["GET", "POST"])
def delete_specific_cupons(request, cupon_id):
    '''
    This is for deleting a particular cupon value. Calling 127.0.0.1:8000/cupons/delete_cupon/4/ will cause to invoke this Api.
    After performing delete operation successfully this api will provide following response.

    Successful Post Response:
        [
            "Cupon has been deleted successfully"
        ]
    Unsuccessful Post Response:
        {
            "Message": "Some internal problem occurs while deleting the value"
        }
    '''

    try:
        cupon = Cupons.objects.get(pk=cupon_id)
    except:
        return Response({'Message': 'Some internal problem occurs while deleting the value'})

    if(request.method == "POST"):
        cupon.delete()
        return Response({'Cupon has been deleted successfully'})

    # --------------------------- Product Discount -----------------------


@api_view(["GET", "POST"])
def get_all_discount_value(request):
    '''
    This api is for getting all the discount related information. Calling http://127.0.0.1:8000/discount/all_discount/ will invoke
    this API. This API just have get response.

    GET Response:
        discount_type (This will be a Chartype data. This will return the type of discount like Flat, Flash, Wholesale etc.)
        amount (This will return the amount which will be apply where discount is applicable.)
        start_date (This is the discount start date. From this date discount will be started.)
        end_date  (This is discount end date. On this date, discount will be end.)
        max_amount (Sometimes, admin can restrict the highest level of amount for discount. This value represents that highest amount value.) 
    '''

    if(request.method == "GET"):
        queryset = discount_product.objects.all()
        discount_serializers = ProductDiscountSerializer(queryset, many=True)
        return Response(discount_serializers.data)


@api_view(["GET", "POST"])
def insert_specific_discount_value(request):
    '''
    This Api is for just inserting the particular discount value corresponding to a product. It has just Post response. Calling 
    http://127.0.0.1:8000/discount/insert_specific/ cause to invoke this api.

    POST Response:
        Following values field this api expects while performing post response.
        Discount (It will be type of discount, simply a name.)
        amount (This will be a float value. This amount value will be used to calculate the discount value)
        start_date ( This is the date from when the discount will be started.)
        end_date (On this date, the discount will end)
        max_amount (Admin can set the highest amount of discount. Something like 30% discount upto 50 taka. Here, max amount 50 taka.)
        product_id or group_product_id ( product_id or group_product_id, on which the discount will be performed must need to provide.)
    '''
    if(request.method == "POST"):
        discount_serializers = ProductDiscountSerializer(data=request.data)
        if(discount_serializers.is_valid()):
            discount_serializers.save()
            return Response(discount_serializers.data, status=status.HTTP_201_CREATED)
        return Response(discount_serializers.errors)


@api_view(["GET", "POST"])
def get_update_specific_value(request, product_id):
    '''
    This Api is for getting a particular discount value. This will need to update a particular information. Admin may change the end date of discount or 
    may increase the amount value. Calling http://127.0.0.1:8000/discount/specific_value/3/ will cause to invoke this API. This Api has both 
    Post and Get response.
    prams : Product_id
    Get Response:
        discount_type (This will be a Chartype data. This will return the type of discount like Flat, Flash, Wholesale etc.)
        amount (This will return the amount which will be apply where discount is applicable.)
        start_date (This is the discount start date. From this date discount will be started.)
        end_date  (This is discount end date. On this date, discount will be end.)
        max_amount (Sometimes, admin can restrict the highest level of amount for discount. This value represents that highest amount value.) 

    POST Response:
        Following values field this api expects while performing post response.
        Discount (It will be type of discount, simply a name.)
        amount (This will be a float value. This amount value will be used to calculate the discount value)
        start_date ( This is the date from when the discount will be started.)
        end_date (On this date, the discount will end)
        max_amount (Admin can set the highest amount of discount. Something like 30% discount upto 50 taka. Here, max amount 50 taka.)
        product_id or group_product_id ( product_id or group_product_id, on which the discount will be performed must need to provide.)


    '''
    # Demo Values
    try:
        specific_values = discount_product.objects.get(product_id=product_id)
    except:
        return Response({'message': 'This value does not exist'})

    if(request.method == "GET"):
        discount_serializer_value = ProductDiscountSerializer(
            specific_values, many=False)
        return Response(discount_serializer_value.data)

    elif(request.method == "POST"):
        try:
            discount_serializer_value = ProductDiscountSerializer(
                specific_values, data=request.data)
            if(discount_serializer_value.is_valid()):
                discount_serializer_value.save()
                return Response(discount_serializer_value.data, status=status.HTTP_201_CREATED)
            return Response(discount_serializer_value.errors)
        except:
            return Response({'message': 'Discount value could not be updated'})


@api_view(['POST', 'GET'])
def delete_discount_value(request, product_id):
    '''
    This Api is for deleting a particular discount value. Based on the provided product_id or group_product_id this will delet the discount value.
    Calling http://127.0.0.1:8000/discount/discount_delete/4 will cause to invoke this api. After deleting the value, in response this api will 
    send a successful message. If it can not delete then it will provide an error message.

    prams : product_id
    '''

    try:
        specific_values = discount_product.objects.get(product_id=product_id)
    except:
        return Response({'message': 'There is no value to delete'})

    if request.method == 'POST':
        specific_values.delete()
        return Response({'message': ' Value is successfully  deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def get_product_lists(request, order_id):

    if(request.method == "GET"):

        try:
            ware_house = []
            shops = []
            order_info = OrderDetails.objects.filter(order_id=order_id)
            print(order_info)

            for orders in order_info:
                all_specification = ProductSpecification.objects.get(
                    product_id=orders.product_id, size=orders.product_size, color=orders.product_color)
                print(all_specification)
                ware_house_info = Warehouse.objects.filter(
                    specification_id=all_specification.id)
                if ware_house_info:
                    ware_house_data = WareHouseSerializer(
                        ware_house_info, many=True)
                    ware_house.append(ware_house_data.data)
                shop_info = Shop.objects.filter(
                    specification_id=all_specification.id)
                if shop_info.exists():
                    shop_data = ShopSerializer(shop_info, many=True)
                    shops.append(shop_data.data)
        except:
            return Response({'Message': 'Check whether requested data exists or not'})

        return Response({
            "success": True,
            "Message": "Data is shown bellow",
            "warehouse": ware_house,
            "Shop": shops
        })


@api_view(["GET", ])
def get_inventory_lists(request, order_details_id):

    try:

        product = OrderDetails.objects.get(id=order_details_id)

    except:

        product = None

    if product:

        product_id = product.product_id
        product_size = product.product_size
        product_color = product.product_color

        try:

            spec = ProductSpecification.objects.get(
                product_id=product_id, size=product_size, color=product_color)

        except:

            spec = None

        if spec:

            specification_id = spec.id

            try:

                warehouses = Warehouse.objects.filter(
                    specification_id=specification_id)

            except:

                warehouses = None

            if warehouses:

                warehouses_serializer = WareHouseSerializer(
                    warehouses, many=True)
                warehouse_data = warehouses_serializer.data

            else:

                warehouse_data = []

            try:

                warehouses = Shop.objects.filter(
                    specification_id=specification_id)

            except:

                warehouses = None

            if warehouses:

                warehouses_serializer = ShopSerializer(warehouses, many=True)
                shop_data = warehouses_serializer.data

            else:

                shop_data = []

        else:
            warehouse_data = []
            shop_data = []

    else:
        warehouse_data = []
        shop_data = []

    return JsonResponse({'success': True, 'message': 'Data is shown below', 'warehouse_data': warehouse_data, 'shop_data': shop_data})


@api_view(["POST", ])
def subtract_quantity(request, order_details_id):

    warehouse_id = request.data.get("warehouse_id")
    shop_id = request.data.get("shop_id")
    quantity = request.data.get("quantity")
    quantity = int(quantity)

    if warehouse_id is None:

        inventory_id = shop_id

        try:

            product = OrderDetails.objects.get(id=order_details_id)

        except:

            product = None

        if product:

            item_quantity = product.total_quantity
            item_remaining = product.remaining

            if item_remaining > 0:

                # make the subtraction

                check = item_remaining - int(quantity)

                if check >= 0:

                    print("quantity thik dise")

                    product.remaining -= quantity
                    product.save()
                    item_remaining = product.remaining
                    item_quantity = product.quantity

                    try:
                        shop = Shop.objects.get(id=shop_id)

                    except:

                        shop = None

                    if shop:

                        shop.product_quantity -= quantity
                        shop.save()
                        shop_serializer = ShopSerializer(shop, many=False)
                        shop_data = shop_serializer.data

                    else:

                        shop_data = {}

                    return JsonResponse({'success': True, 'message': 'The amount has been subtracted', 'remaining': item_remaining, 'quantity': item_quantity, 'shop_data': shop_data})

                else:

                    print("quantity thik dey nai")

                    return JsonResponse({'success': False, 'message': 'Enter the correct quantity', 'remaining': item_remaining, 'quantity': item_quantity})

            else:

                print("item nai ar")

                return JsonResponse({'success': False, 'message': 'The items quantity has already been subtracted'})

        else:
            print("product nai")

            return JsonResponse({'success': False, 'message': 'The item does not exist'})

    elif shop_id is None:

        print("warehouse ase")

        inventory_id = warehouse_id

        print(inventory_id)

        try:

            product = OrderDetails.objects.get(id=order_details_id)

        except:

            product = None

        if product:

            item_quantity = product.total_quantity
            item_remaining = product.remaining

            if item_remaining > 0:

                # make the subtraction

                check = item_remaining - quantity

                if check >= 0:

                    print("quantity thik dise")

                    product.remaining -= quantity
                    product.save()
                    item_remaining = product.remaining
                    item_quantity = product.quantity

                    try:
                        warehouse = Warehouse.objects.get(id=warehouse_id)

                    except:

                        warehouse = None

                    if warehouse:

                        warehouse.product_quantity -= quantity
                        warehouse.save()
                        warehouse_serializer = WareHouseSerializer(
                            warehouse, many=False)
                        warehouse_data = warehouse_serializer.data

                    else:

                        warehouse_data = {}

                    return JsonResponse({'success': True, 'message': 'The amount has been subtracted', 'remaining': item_remaining, 'quantity': item_quantity, 'warehouse_data': warehouse_data})

                else:
                    print("quantity thik dey nai")

                    return JsonResponse({'success': False, 'message': 'Enter the correct quantity', 'remaining': item_remaining, 'quantity': item_quantity})

            else:

                print("product er item nai")

                return JsonResponse({'success': False, 'message': 'The items quantity has already been subtracted'})

        else:
            print("item tai nai")

            return JsonResponse({'success': False, 'message': 'The item does not exist'})


@api_view(["POST", ])
def subtract_items(request, order_details_id):


    # data= {"warehouse": [
    #         {
    #             "id": 1,
    #             "name": "WarehouseA",
    #             "location": "Dhanmondi",
    #             "subtract": 10
    #         },
    #         {
    #             "id": 2,
    #             "name": "WarehouseB",
    #             "location": "Gulshan",
    #             "subtract": 10
    #         }
    #     ],
    #     "shop": [
    #         {
    #             "id": 1,
    #             "name": "ShopB",
    #             "location": "gulshan",
    #             "subtract": 10
    #         },
    #         {
    #             "id": 2,
    #             "name": "ShopA",
    #             "location": "Banani",
    #             "subtract": 10
    #         }
    #     ]
    # }






    data = request.data
    current_date = date.today()

    print(data)

    # print(data["warehouse"])
    # print(len(data["warehouse"]))
    # print(data["shop"])
    # print(len(data["warehouse"]))
    # print(data["warehouse"][0]["warehouse_id"])

    warehouse_data = data["warehouse"]
    shop_data = data["shop"]
    # print(warehouse_data)
    # print(len(warehouse_data))
    # print(warehouse_data[1]["warehouse_id"])

    # This is for the warehouse data

    try:

        item = OrderDetails.objects.get(id=order_details_id)

    except:

        item = None

    if item:

        # Checking if any item has been subtracted from the warehouse

        item_remaining = item.remaining
        item_product_id = item.product_id
        item_color = item.product_color
        item_size = item.product_size
        item_weight = item.product_weight 
        item_unit = item.product_unit
        product_id = item.product_id
        specification_id = item.specification_id
        order_id = item.order_id
        print(item_remaining)

        try:

            spec = ProductSpecification.objects.get(id=specification_id)

        except:

            spec = None

        if spec:

            specification_id = spec.id

        else:

            specification_id = 0


        #Fetching the purchase price and selling price 

        try:
            price = ProductPrice.objects.filter(specification_id=specification_id).last()

        except:

            price = None 


        print(price)

        if price: 

            if price.price:
                selling_price = price.price

            else:
                selling_price = 0.0

            if price.purchase_price:
                purchase_price = price.purchase_price 

            else:
                purchase_price = 0.0


        else:

            selling_price = 0.0
            purchase_price = 0.0


        print(purchase_price)
        print(selling_price)


        if int(len(warehouse_data)) > 0:

            # looping through the warehouse items

            for i in range(int(len(warehouse_data))):

                if item_remaining > 0:

                    # fetch the warehouseinfo

                    warehouse_id = warehouse_data[i]["id"]

                    subtract = int(warehouse_data[i]["subtract"])

                    try:

                        warehouse_info = WarehouseInfo.objects.filter(
                            warehouse_id=warehouse_id, specification_id=specification_id).last()

                    except:

                        warehouse_info = None

                    if warehouse_info:

                        if warehouse_info.quantity >= subtract:

                            warehouse_info.quantity -= subtract
                            warehouse_info.save()
                            item.remaining -= subtract
                            item.save()

                            item_remaining = item.remaining

                            #make the entries in the tracking table 

                            tracking_table = subtraction_track.objects.create(specification_id=specification_id,order_id=order_id,warehouse_id=warehouse_id,debit_quantity=subtract,date=current_date)
                            tracking_table.save()

                            #make the transaction entries

                            # try:

                            #     report = inventory_report.objects.get(product_id= product_id,specification_id= specification_id,warehouse_id=warehouse_id,date=current_date)

                            # except:

                            #     report = None 


                            # if report:

                            #     #Update the existing report

                            #     report.requested += subtract
                            #     report.save()


                            # else:
                            #     #Create a new row

                            new_report = inventory_report.objects.create(product_id= product_id,specification_id= specification_id,warehouse_id=warehouse_id,date=current_date,requested=subtract,purchase_price=purchase_price,selling_price=selling_price)
                            new_report.save()






                            if item_remaining == 0:

                                item.admin_status = "Approved"
                                item.save()

                                item_serializer = OrderDetailsSerializer(
                                    item, many=False)
                                data = item_serializer.data

                                return JsonResponse({"success": True, "message": "This product is approved", "data": data})

                        else:
                            return JsonResponse({"success": False, "message": "The warehouse does not have enough of this item"})

                    else:
                        return JsonResponse({"success": False, "message": "The warehouse does not have enough of this item"})

                # elif item_remaining==0:

                #     return JsonResponse({"success":True,"message":"This product is approved"})

                else:
                    return JsonResponse({"success": False, "message": "These many items dont exist in this order"})

        else:

            pass

        if int(len(shop_data)) > 0:

            # looping through the warehouse items

            for i in range(int(len(shop_data))):

                print("loop er moddhe dhuklam")

                if item_remaining > 0:

                    print("shop item_remaining ase")

                    # fetch the warehouseinfo

                    shop_id = shop_data[i]["id"]

                    subtract = int(shop_data[i]["subtract"])

                    try:

                        shop_info = ShopInfo.objects.filter(
                            shop_id=shop_id, specification_id=specification_id).last()

                    except:

                        shop_info = None

                    if shop_info:

                        if shop_info.quantity >= subtract:

                            shop_info.quantity -= subtract
                            shop_info.save()

                            print("shoper aager")

                            print(item_remaining)

                            item.remaining -= subtract
                            item.save()
                            item_remaining = item.remaining

                            print("shop er porer")

                            print(item_remaining)


                            #Inserting the track infos 


                            tracking_table = subtraction_track.objects.create(specification_id=specification_id,order_id=order_id,shop_id=shop_id,debit_quantity=subtract,date=current_date)
                            tracking_table.save()

                            #make the transaction entries

                            # try:

                            #     report = inventory_report.objects.get(product_id= product_id,specification_id= specification_id,shop_id=shop_id,date=current_date)

                            # except:

                            #     report = None 


                            # if report:

                            #     #Update the existing report

                            #     report.requested += subtract
                            #     report.save()


                            # else:
                            #     #Create a new row

                            new_report = inventory_report.objects.create(product_id= product_id,specification_id= specification_id,shop_id=shop_id,date=current_date,requested=subtract,purchase_price=purchase_price,selling_price=selling_price)
                            new_report.save()

                            if item_remaining == 0:

                                item.admin_status = "Approved"
                                item.save()

                                item_serializer = OrderDetailsSerializer(
                                    item, many=False)
                                data = item_serializer.data

                                return JsonResponse({"success": True, "message": "This product is approved", "data": data})

                                return JsonResponse({"success": True, "message": "This product is approved"})

                        else:
                            return JsonResponse({"success": False, "message": "The shop does not have enough of this item"})

                    else:
                        return JsonResponse({"success": False, "message": "The shop does not have enough of this item"})

                # elif item_remaining==0:

                #     return JsonResponse({"success":True,"message":"This product is approved"})

                else:
                    return JsonResponse({"success": False, "message": "These many items dont exist in this order"})

        else:

            pass

    else:

        JsonResponse(
            {"success": False, "message": "The item is not in that order"})




@api_view(["POST", ])
def subtract_spec_quantity(request, specification_id):


    print("specification_id")

    print(specification_id)

#     data= {"warehouse": [
#         {
#             "warehouse_id": 1,
#             "name": "WarehouseA",
#             "location": "Dhanmondi",
#             "subtract": 5
#         },
#         {
#             "warehouse_id": 2,
#             "name": "WarehouseB",
#             "location": "Gulshan",
#             "subtract": 3
#         }
#     ],
#     "shop": [
#         {
#             "shop_id": 1,
#             "name": "ShopB",
#             "location": "gulshan",
#             "subtract": 2
#         },
#         {
#             "shop_id": 2,
#             "name": "ShopA",
#             "location": "Banani",
#             "subtract": 1
#         }
#     ]
# }



    data = request.data
    current_date = date.today()

    print(data)

    # print(data["warehouse"])
    # print(len(data["warehouse"]))
    # print(data["shop"])
    # print(len(data["warehouse"]))
    # print(data["warehouse"][0]["warehouse_id"])

    warehouse_data = data["warehouse"]
    shop_data = data["shop"]
    # print(warehouse_data)
    # print(len(warehouse_data))
    # print(warehouse_data[1]["warehouse_id"])

    # This is for the warehouse data

    try:

        item = ProductSpecification.objects.get(id=specification_id)

    except:

        item = None

    print('item')
    print(item)
    print(item.id)
    print(item.remaining)

    if item:

        # Checking if any item has been subtracted from the warehouse

        item_remaining = item.remaining
        # item_product_id = item.product_id
        # item_color = item.product_color
        # item_size = item.product_size
        # item_weight = item.product_weight 
        # item_unit = item.product_unit
        product_id = item.product_id
        # specification_id = item.specification_id

        # try:

        #     spec = ProductSpecification.objects.get(id=specification_id)

        # except:

        #     spec = None

        # if spec:

        #     specification_id = spec.id

        # else:

        #     specification_id = 0

        print(item_remaining)

        if int(len(warehouse_data)) > 0:

            # looping through the warehouse items

            for i in range(int(len(warehouse_data))):

                if item_remaining > 0:

                    # fetch the warehouseinfo

                    warehouse_id = warehouse_data[i]["warehouse_id"]

                    subtract = int(warehouse_data[i]["subtract"])

                    #Checking if warehouse exists

                    try:

                        warehouse_info = WarehouseInfo.objects.get(
                            warehouse_id=warehouse_id, specification_id=specification_id)

                    except:

                        warehouse_info = None

                    if warehouse_info:

                        

                        warehouse_info.quantity += subtract
                        warehouse_info.save()
                        item.remaining -= subtract
                        item.save()

                        item_remaining = item.remaining

                        #make the transaction entries

                        # try:

                        #     report = inventory_report.objects.get(product_id= product_id,specification_id= specification_id,warehouse_id=warehouse_id,date=current_date)

                        # except:

                        #     report = None 


                        # if report:

                        #     #Update the existing report

                        #     report.debit += subtract
                        #     report.save()


                        # else:
                        #     #Create a new row

                        new_report = inventory_report.objects.create(product_id= product_id,specification_id= specification_id,warehouse_id=warehouse_id,date=current_date,credit=subtract)
                        new_report.save()






                        if item_remaining == 0:

                            # item.admin_status = "Approved"
                            # item.save()

                            item_serializer = ProductSpecificationSerializer1(
                                item, many=False)
                            data = item_serializer.data

                            return JsonResponse({"success": True, "message": "All the quantities have been subtracted", "data": data})



                    else:

                        #Create a new warehouse

                        warehouse_info = WarehouseInfo.objects.create(product_id=product_id,warehouse_id=warehouse_id,specification_id=specification_id,quantity=subtract)
                        warehouse_info.save()

                        item.remaining -= subtract
                        item.save()

                        item_remaining = item.remaining

                        # try:

                        #     report = inventory_report.objects.get(product_id= product_id,specification_id= specification_id,warehouse_id=warehouse_id,date=current_date)

                        # except:

                        #     report = None 


                        # if report:

                        #     #Update the existing report

                        #     report.debit += subtract
                        #     report.save()


                        # else:
                        #     #Create a new row

                        new_report = inventory_report.objects.create(product_id= product_id,specification_id= specification_id,warehouse_id=warehouse_id,date=current_date,credit=subtract)
                        new_report.save()






                        if item_remaining == 0:

                            # item.admin_status = "Approved"
                            # item.save()

                            item_serializer = ProductSpecificationSerializer1(
                                item, many=False)
                            data = item_serializer.data

                            return JsonResponse({"success": True, "message": "All the quantities have been added", "data": data})
                        

                # elif item_remaining==0:

                #     return JsonResponse({"success":True,"message":"This product is approved"})

                else:
                    return JsonResponse({"success": False, "message": "These many items dont exist"})

        else:

            pass


        if int(len(shop_data)) > 0:

            # looping through the warehouse items

            for i in range(int(len(shop_data))):

                if item_remaining > 0:

                    # fetch the warehouseinfo

                    shop_id = shop_data[i]["shop_id"]

                    subtract = int(shop_data[i]["subtract"])

                    #Checking if warehouse exists

                    try:

                        shop_info = ShopInfo.objects.get(
                            shop_id=shop_id, specification_id=specification_id)

                    except:

                        shop_info = None

                    if shop_info:

                        

                        shop_info.quantity += subtract
                        shop_info.save()
                        item.remaining -= subtract
                        item.save()

                        item_remaining = item.remaining

                        #make the transaction entries

                        # try:

                        #     report = inventory_report.objects.get(product_id= product_id,specification_id= specification_id,shop_id=shop_id,date=current_date)

                        # except:

                        #     report = None 


                        # if report:

                        #     #Update the existing report

                        #     report.debit += subtract
                        #     report.save()


                        # else:
                        #     #Create a new row

                        new_report = inventory_report.objects.create(product_id= product_id,specification_id= specification_id,shop_id=warehouse_id,date=current_date,credit=subtract)
                        new_report.save()






                        if item_remaining == 0:

                            # item.admin_status = "Approved"
                            # item.save()

                            item_serializer = ProductSpecificationSerializer1(
                                item, many=False)
                            data = item_serializer.data

                            return JsonResponse({"success": True, "message": "All the quantities have been subtracted", "data": data})



                    else:

                        #Create a new warehouse

                        warehouse_info = ShopInfo.objects.create(product_id=product_id,shop_id=shop_id,specification_id=specification_id,quantity=subtract)
                        warehouse_info.save()

                        item.remaining -= subtract
                        item.save()

                        item_remaining = item.remaining

                        # try:

                        #     report = inventory_report.objects.get(product_id= product_id,specification_id= specification_id,shop_id=shop_id,date=current_date)

                        # except:

                        #     report = None 


                        # if report:

                        #     #Update the existing report

                        #     report.debit += subtract
                        #     report.save()


                        # else:
                        #     #Create a new row

                        new_report = inventory_report.objects.create(product_id= product_id,specification_id= specification_id,shop_id=warehouse_id,date=current_date,credit=subtract)
                        new_report.save()






                        if item_remaining == 0:

                            # item.admin_status = "Approved"
                            # item.save()

                            item_serializer = ProductSpecificationSerializer1(
                                item, many=False)
                            data = item_serializer.data

                            return JsonResponse({"success": True, "message": "All the quantities have been added", "data": data})
                        

                # elif item_remaining==0:

                #     return JsonResponse({"success":True,"message":"This product is approved"})

                else:
                    return JsonResponse({"success": False, "message": "These many items dont exist"})

        else:

            pass




# @api_view(["POST", ])
# def admin_approval(request, order_id):

#     flag = 0

#     try:

#         specific_order = Order.objects.get(id=order_id)

#     except:

#         specific_order = None

#     if specific_order:

#         orderid = specific_order.id

#         order_details = OrderDetails.objects.filter(order_id=orderid)
#         order_details_ids = list(
#             order_details.values_list('id', flat=True).distinct())
#         print(order_details_ids)

#         for i in range(len(order_details_ids)):

#             print("ashtese")

#             try:
#                 specific_order_details = OrderDetails.objects.get(
#                     id=order_details_ids[i])
#             except:
#                 specific_order_details = None

#             if specific_order_details:

#                 remaining_items = specific_order_details.remaining

#                 if remaining_items != 0:

#                     flag = 1
#                     break

#                 else:

#                     flag = 0

#         if flag == 0:

#             specific_order.admin_status = "Confirmed"
#             specific_order.save()
#             # Create a invoice
#             data = {'order_id': order_id}
#             invoice_serializer = InvoiceSerializer(data=data)
#             if invoice_serializer.is_valid():
#                 invoice_serializer.save()


#             return JsonResponse({'success': True, 'message': 'The order has been approved'})

#         else:

#             return JsonResponse({'success': False, 'message': 'Please ensure where to remove the items from'})

#     else:

#         return JsonResponse({'success': False, 'message': 'The order does not exist'})


# @api_view(["POST",])
# def admin_approval(request,order_id):

#     flag = 0


#     try:

#         specific_order = Order.objects.get(id=order_id)

#     except:

#         specific_order = None

#     if specific_order:

#         orderid = specific_order.id

#         order_details = OrderDetails.objects.filter(order_id=orderid)
#         order_details_ids = list(order_details.values_list('id',flat=True).distinct())
#         print(order_details_ids)

#         for i in range(len(order_details_ids)):

#             print("ashtese")

#             try:
#                 specific_order_details = OrderDetails.objects.get(id=order_details_ids[i])
#             except:
#                 specific_order_details = None

#             if specific_order_details:

#                 remaining_items = specific_order_details.remaining

#                 if remaining_items != 0 :

#                     flag = 1
#                     break

#                 else:

#                     flag = 0


#         if flag == 0:

#             specific_order.admin_status = "Confirmed"
#             specific_order.save()

#             return JsonResponse({'success':True,'message':'The order has been approved'})

#         else:

#             return JsonResponse({'success':False,'message':'Please ensure where to remove the items from'})


#     else:

#         return JsonResponse({'success':False,'message':'The order does not exist'})

# @api_view(["GET", ])
# def admin_approval(request, order_id):

#     try:

#         specific_order = Order.objects.get(id=order_id)

#     except:

#         specific_order = None

#     if specific_order:

#         specific_order.admin_status = "Confirmed"

#         specific_order.save()

#         order_serializer = OrderSerializer(specific_order, many=False)

#         data = order_serializer.data

#         # Create a invoice
#         data = {'order_id':order_id, 'ref_invoice':0, 'is_active':True}
#         invoice_serializer = InvoiceSerializer(data=data)
#         if invoice_serializer.is_valid():
#             invoice_serializer.save()

#         return JsonResponse({"success": True, "message": "The order has been approved", "data": data})

#     else:

#         return JsonResponse({"success": False, "message": "This order does not exist"})



@api_view(["GET", ])
def admin_approval(request, order_id):
    approval_flag = True

    try:
        company= CompanyInfo.objects.all()
    except:
        company = None 

    if company:
        company = company[0]
        site_id = company.site_identification
    else:
        site_id = ""


    print("site_ud")
    print(site_id)

    try:

        specific_order = Order.objects.get(id=order_id)

    except:

        specific_order = None

    if specific_order:

        is_mother = specific_order.is_mother

        if is_mother == True:

            print("mother er product")


            specific_order.admin_status = "Confirmed"

            specific_order.save()

            order_serializer = OrderSerializer(specific_order, many=False)

            order_data = order_serializer.data
            main_data = {"order_data":order_data,"site_id":site_id}
            print("MAIN DATA")
            print(main_data)

            # Create a selling invoice
            data = {'order_id':order_id, 'ref_invoice':0, 'is_active':True}
            invoice_serializer = InvoiceSerializer(data=data)
            if invoice_serializer.is_valid():
                invoice_serializer.save()
                invoice_id = invoice_serializer.data["id"]
                #Create a purchase invoice
                spec_dataz = json.dumps(main_data)
    
                url = site_path + "Cart/create_childsite_orders_purchase_invoice/"
                headers = {'Content-Type': 'application/json',}
                dataz = requests.post(url = url, headers=headers,data = spec_dataz)
                data_response = str(dataz)
                if data_response == "<Response [200]>":
                    dataz = dataz.json()
                    print("JANI NAAAAA")
                    print(dataz["success"])
                    print(dataz["message"])
                    if dataz["success"] == True:
                        return JsonResponse({"success":True,'message':'Order has been approved.Mother site response was successful.Invoice has been created'})
                    else:
                        try:
                            specific_invoice = Invoice.objects.get(id=invoice_id)
                        except:
                            specific_invoice = None 
                        if specific_invoice:
                            specific_invoice.delete()
                        specific_order.admin_status = "Pending"
                        specific_order.save()
                        return JsonResponse({"success": False,'message':'Order could not be approved.Mother site response was insuccessful.'})

                else:
                    try:
                        specific_invoice = Invoice.objects.get(id=invoice_id)
                    except:
                        specific_invoice = None 
                    if specific_invoice:
                        specific_invoice.delete()
                    specific_order.admin_status = "Pending"
                    specific_order.save()
                    return JsonResponse({"success": False,'message':'Order could not be approved.Mother site did not respond.'})
                    

            else:
                specific_order.admin_status = "Pending"

                specific_order.save()

                return JsonResponse({"success":False, "message":"The order could not be approved since invoice could not be created"})
                


            
        

        else:

            try:
                order_details = OrderDetails.objects.filter(order_id = order_id)
            except:
                order_details = None 

            if order_details:

                order_details_ids = list(order_details.values_list('id',flat=True))
                is_owns = list(order_details.values_list('is_own',flat=True))
                admin_statuses = list(order_details.values_list('admin_status',flat=True))
                for i in range (len(order_details_ids)):
                    if is_owns[i] == True:
                        if admin_statuses[i] == "Pending":
                            approval_flag = False
                            break
                        else:
                            pass
                    else:
                        pass

                if approval_flag == True:

                    specific_order.admin_status = "Confirmed"

                    specific_order.save()

                    order_serializer = OrderSerializer(specific_order, many=False)

                    data = order_serializer.data

                    # Create a invoice
                    data = {'order_id':order_id, 'ref_invoice':0, 'is_active':True}
                    invoice_serializer = InvoiceSerializer(data=data)
                    if invoice_serializer.is_valid():
                        invoice_serializer.save()

                    else:
                        specific_order.admin_status = "Processing"

                        specific_order.save()

                        return JsonResponse({"success":False, "message":"The order could not be approved since invoice could not be created"})

                    return JsonResponse({"success": True, "message": "The order has been approved", "data": data})




                else:
                    return JsonResponse({"success":False,"message":"The order cannot be approved.There are still pending items in the order."})


            else:
                return JsonResponse({"success":False,"message":"The order cannot be approved.There are no items in this order"})

    else:

        return JsonResponse({"success": False, "message": "This order does not exist"})


@api_view(["GET", ])
def admin_cancellation(request, order_id):

    try:

        specific_order = Order.objects.get(id=order_id)

    except:

        specific_order = None

    if specific_order:

        specific_order.admin_status = "Cancelled"

        specific_order.save()
               
        order_id = specific_order.id
        try:
            items = OrderDetails.objects.filter(order_id=order_id)
        except:
            items = None
        if items:
            
            item_ids = list(items.values_list('id',flat=True).distinct())

            for k in range(len(item_ids)):
                try:
                    specific_item = OrderDetails.objects.get(id=item_ids[k])
                except:
                    specific_item = None 

                if specific_item:
                    specific_item.admin_status = "Cancelled"
                    specific_item.order_status = "Cancelled"
                    specific_item.delivery_status = "Cancelled"
                    specific_item.save()

                    

                else:
                    pass

        order_serializer = OrderSerializer(specific_order, many=False)

        data = order_serializer.data

        return JsonResponse({"success": True, "message": "The order has been approved", "data": data})

    else:

        return JsonResponse({"success": False, "message": "This order does not exist"})


@api_view(["GET", ])
def item_cancellation(request, order_details_id):

    try:

        item = OrderDetails.objects.get(id=order_details_id)

    except:

        item = None

    if item:

        item.admin_status = "Cancelled"
        item.save()
        item_serializer = OrderDetailsSerializer(item, many=False)
        data = item_serializer.data
        return JsonResponse({"success": True, "message": "The status has been changed", "data": data})

    else:
        return JsonResponse({"success": False, "message": "This item does not exist"})


# @api_view(['POST', ])
# def add_spec(request, product_id):

#     current_date = date.today()

#     specification_data_value = {

#         'product_id': product_id,
#         'color': request.data.get("color"),
#         'size': request.data.get("size"),
#         'weight': request.data.get("weight"),
#         'warranty': request.data.get("warranty"),
#         'warranty_unit': request.data.get("warranty_unit"),
#         'unit': request.data.get("product_unit"),
#         'vat': request.data.get("vat"),

#     }

#     product_price = {
#         'product_id': product_id,
#         'price': request.data.get("price"),
#         'purchase_price': request.data.get("purchase_price"),
#         # 'currency_id': request.data.get('currency_id')
#     }

#     product_code = {
#         'product_id': product_id
#     }

#     discount_type = request.data.get("discount_type")
#     discount_amount = request.data.get("discount_amount")
#     discount_start_date = request.data.get("discount_start_date")
#     discount_end_date = request.data.get("discount_end_date")
#     point_amount = request.data.get("point_amount")
#     point_start_date = request.data.get("point_start_date")
#     point_end_date = request.data.get("point_end_date")

#     if discount_type == "none" or discount_amount == "" or discount_start_date == "" or discount_end_date == "":
#         discount_flag = False

#     else:

#         discount_flag = True

#     if point_amount == "" or point_start_date == "" or point_end_date == "":

#         point_flag = False

#     else:

#         point_flag = True

#     product_discount = {

#         'product_id': product_id,
#         'amount': request.data.get("discount_amount"),
#         'discount_type': request.data.get("discount_type"),
#         'start_date': request.data.get("discount_start_date"),
#         # 'end_date' : data['discount_end_date']
#         'end_date': request.data.get("discount_end_date")
#     }

#     product_point = {
#         'product_id': product_id,
#         'point': request.data.get("point_amount"),
#         # 'end_date': data['point_end_date']
#         'start_date': request.data.get("point_start_date"),
#         'end_date': request.data.get("point_end_date")
#     }

#     delivery_info = {
#         'height': request.data.get("delivery_height"),
#         'width': request.data.get("delivery_width"),
#         'length': request.data.get("delivery_length"),
#         'weight': request.data.get("delivery_weight"),
#         'measument_unit': request.data.get("delivery_product_unit"),
#         'charge_inside': request.data.get("delivery_inside_city_charge"),
#         'charge_outside': request.data.get("delivery_outside_city_charge"),
#     }

#     if request.method == 'POST':
#         delivery_id = 0
#         discount_id = 0
#         point_id = 0
#         price_id = 0
#         specification_id = 0
#         flag = 0
#         spec = {}
#         price = {}
#         discount = {}
#         point = {}
#         delivery = {}
#         code = {}
#         try:
#             product_spec = ProductSpecificationSerializerz(
#                 data=specification_data_value)
#             if product_spec.is_valid():
#                 product_spec.save()
#                 print("spec save hoise")
#                 spec.update(product_spec.data)
#                 print("Specification_id")
#                 specification_id = spec["id"]

#             else:
#                 # print(product_spec.errors)
#                 specification_id = 0
#                 flag = flag+1

#             product_price.update({'specification_id': spec['id']})
#             print("fbwhefygbfywegbfwgfb")
#             print(product_price)
#             product_price = ProductPriceSerializer(data=product_price)
#             if product_price.is_valid():
#                 product_price.save()
#                 print("price save hochche")
#                 price.update(product_price.data)
#                 price_id = price["id"]
#             else:
#                 price_id = 0

#                 flag = flag+1

#             if discount_flag == False:
#                 discount = {}
#             else:
#                 product_discount.update({'specification_id': spec['id']})
#                 print("product_discount")
#                 print(product_discount)
#                 product_dis = ProductDiscountSerializer(data=product_discount)
#                 if product_dis.is_valid():
#                     product_dis.save()
#                     print("savwe hochche")
#                     discount.update(product_dis.data)
#                     discount_id = discount["id"]

#                 else:

#                     discount_id = 0

#                     flag = flag+1

#             if point_flag == False:

#                 point = {}

#             else:

#                 product_point.update({'specification_id': spec['id']})
#                 product_point_value = ProductPointSerializer(
#                     data=product_point)
#                 if product_point_value.is_valid():
#                     product_point_value.save()
#                     print("point save")
#                     point.update(product_point_value.data)
#                     point_id = point["id"]
#                 else:

#                     point_id = 0

#                     print(product_point_value.errors)
#                     flag = flag+1

#             delivery_info.update({'specification_id': spec['id']})
#             # print("here delivery",delivery_info )
#             delivery_value = DeliveryInfoSerializer(data=delivery_info)
#             # print("serializer",delivery_value)
#             if delivery_value.is_valid():
#                 # print("here")
#                 delivery_value.save()
#                 delivery.update(delivery_value.data)
#                 delivery_id = delivery["id"]
#             else:
#                 delivery_id = 0
#                 print(delivery_value.errors)

#                 flag = flag+1


#             product_code.update({'specification_id':spec['id']})
#             print("product point",product_code )
#             product_code_value= ProductCodeSerializer (data=product_code)
#             if product_code_value.is_valid():
#                 product_code_value.save()
#                 print("code is saved")
#                 code.update(product_code_value.data)
#                 code_id = code["id"]
            
#             else:
#                 print("code error", product_code_value.errors)
#                 flag= flag+1

#             if flag > 0:
#                 print("xxxxxxxxxxxxxxx")
#                 return JsonResponse({
#                     "success": False,
#                     "message": "Something went wrong !!",
#                 })
#             else:
#                 return JsonResponse({
#                     "success": True,
#                     "message": "Specification data has been inserted Successfully",
#                     "specification": spec,
#                     "price": price,
#                     "discount": discount,
#                     "point": point,
#                     "delivery": delivery
#                 })

#         except:
#             print("yyyyyyyyyyyyyyyyyyy")
#             try:
#                 spe = ProductSpecification.objects.get(id=specification_id)
#             except:
#                 spe = None

#             if spe:
#                 spe.delete()

#             try:
#                 pri = ProductPrice.objects.get(id=price_id)
#             except:
#                 pri = None
#             if pri:
#                 pri.delete()

#             try:
#                 poi = ProductPoint.objects.get(id=point_id)

#             except:

#                 poi = None

#             if poi:

#                 poi.delete()

#             try:
#                 dis = discount_product.objects.get(id=discount_id)

#             except:
#                 dis = None

#             if dis:

#                 dis.delete()

#             try:
#                 deli = DeliveryInfo.objects.get(id=delivery_id)

#             except:
#                 deli = None

#             if deli:

#                 deli.delete()


#             try:
#                 deli = ProductCode.objects.get(id=delivery_id)

#             except:
#                 deli = None

#             if deli:

#                 deli.delete()


#             return JsonResponse({
#                 "success": False,
#                 "message": "Something went wrong !!"
#             })


# @api_view(['POST', ])
# def add_spec(request, product_id):
#     current_date = date.today()
#     print(request.data)
#     specification_data_value = {
#         'product_id': product_id,
#         'color': request.data.get("color"),
#         'size': request.data.get("size"),
#         'weight': request.data.get("weight"),
#         'warranty': request.data.get("warranty"),
#         'warranty_unit': request.data.get("warranty_unit"),
#         'unit': request.data.get("product_unit"),
#         'vat': request.data.get("vat"),
#         # 'seller_quantity': request.data.get("seller_quantity"),
#         # 'remaining': request.data.get("seller_quantity"),
#         'manufacture_date': request.data.get("manufacture_date"),
#         'expire': request.data.get("expire")
#     }
#     product_price = {
#         'product_id': product_id,
#         'price': request.data.get("price"),
#         'purchase_price': request.data.get("purchase_price"),
#         # 'currency_id': request.data.get('currency_id')
#     }
#     discount_type = request.data.get("discount_type")
#     discount_amount = request.data.get("discount_amount")
#     discount_start_date = request.data.get("discount_start_date")
#     discount_end_date = request.data.get("discount_end_date")
#     point_amount = request.data.get("point_amount")
#     point_start_date = request.data.get("point_start_date")
#     point_end_date = request.data.get("point_end_date")
#     if discount_type == "none" or discount_amount == "" or discount_start_date == "" or discount_end_date == "":
#         discount_flag = False
#     else:
#         discount_flag = True
#     if point_amount == "" or point_start_date == "" or point_end_date == "":
#         point_flag = False
#     else:
#         point_flag = True
#     product_discount = {
#         'product_id': product_id,
#         'amount': request.data.get("discount_amount"),
#         'discount_type': request.data.get("discount_type"),
#         'start_date': request.data.get("discount_start_date"),
#         # 'end_date' : data['discount_end_date']
#         'end_date': request.data.get("discount_end_date")
#     }
#     product_point = {
#         'product_id': product_id,
#         'point': request.data.get("point_amount"),
#         # 'end_date': data['point_end_date']
#         'start_date': request.data.get("point_start_date"),
#         'end_date': request.data.get("point_end_date")
#     }
#     delivery_info = {
#         'height': request.data.get("delivery_height"),
#         'width': request.data.get("delivery_width"),
#         'length': request.data.get("delivery_length"),
#         'weight': request.data.get("delivery_weight"),
#         'measument_unit': request.data.get("delivery_product_unit"),
#         'charge_inside': request.data.get("delivery_inside_city_charge"),
#         'charge_outside': request.data.get("delivery_outside_city_charge"),
#     }
#     product_code = {
#         'product_id': product_id,
#         'manual_SKU' : request.data.get("sku")
#     }
#     if request.method == 'POST':
#         delivery_id = 0
#         discount_id = 0
#         point_id = 0
#         price_id = 0
#         specification_id = 0
#         flag = 0
#         spec = {}
#         price = {}
#         discount = {}
#         point = {}
#         delivery = {}
#         code={}
#         try:
#             product_spec = ProductSpecificationSerializerz(
#                 data=specification_data_value)
#             if product_spec.is_valid():
#                 product_spec.save()
#                 # print("888888888888888888  spec save hoise")
#                 spec.update(product_spec.data)
#                 # print("Specification_id", spec["id"])
#                 specification_id = spec["id"]
#             else:
#                 # print(product_spec.errors)
#                 specification_id = 0
#                 flag = flag+1
#             product_price.update({'specification_id': spec['id']})
#             product_price = ProductPriceSerializer(data=product_price)
#             if product_price.is_valid():
#                 product_price.save()
#                 # print("price save hochche")
#                 price.update(product_price.data)
#                 price_id = price["id"]
#             else:
#                 price_id = 0
#                 flag = flag+1
#             if discount_flag == False:
#                 discount = {}
#             else:
#                 product_discount.update({'specification_id': spec['id']})
#                 # print("product_discount")
#                 # print(product_discount)
#                 product_dis = ProductDiscountSerializer(data=product_discount)
#                 if product_dis.is_valid():
#                     product_dis.save()
#                     # print("savwe hochche")
#                     discount.update(product_dis.data)
#                     discount_id = discount["id"]
#                 else:
#                     discount_id = 0
#                     flag = flag+1
#             if point_flag == False:
#                 point = {}
#             else:
#                 product_point.update({'specification_id': spec['id']})
#                 product_point_value = ProductPointSerializer(
#                     data=product_point)
#                 if product_point_value.is_valid():
#                     product_point_value.save()
#                     # print("point save")
#                     point.update(product_point_value.data)
#                     point_id = point["id"]
#                 else:
#                     point_id = 0
#                     # print(product_point_value.errors)
#                     flag = flag+1
#             delivery_info.update({'specification_id': spec['id']})
#             # print("here delivery",delivery_info )
#             delivery_value = DeliveryInfoSerializer(data=delivery_info)
#             # print("serializer",delivery_value)
#             if delivery_value.is_valid():
#                 # print("Inside the delivery ")
#                 delivery_value.save()
#                 # print("delivery is saved")
#                 delivery.update(delivery_value.data)
#                 delivery_id = delivery["id"]
#             else:
#                 delivery_id = 0
#                 # print("errors delivery " ,delivery_value.errors)
#                 flag = flag+1
#             product_code.update({'specification_id':spec['id']})
#             # print("product point",product_code )
#             product_code_value= ProductCodeSerializer (data=product_code)
#             # print("product code serial", product_code_value)
#             # print("before validation")
#             if product_code_value.is_valid():
#                 # print("inside validation")
#                 product_code_value.save()
#                 # print("code is saved", product_code_value.data)
#                 code.update(product_code_value.data)
#                 # print("update code info",code )
#                 code_id = code["id"]
#                 # print("code id", code_id)
#             else:
#                 # print("code error", product_code_value.errors)
#                 flag= flag+1
#             if flag > 0:
#                 # print("xxxxxxxxxxxxxxx")
#                 return JsonResponse({
#                     "success": False,
#                     "message": "Something went wrong !!",
#                 })
#             else:
#                 return JsonResponse({
#                     "success": True,
#                     "message": "Specification data has been inserted Successfully",
#                     "specification": spec,
#                     "price": price,
#                     "discount": discount,
#                     "point": point,
#                     "delivery": delivery
#                 })
#         except:
#             try:
#                 spe = ProductSpecification.objects.get(id=specification_id)
#             except:
#                 spe = None
#             if spe:
#                 spe.delete()
#             try:
#                 pri = ProductPrice.objects.get(id=price_id)
#             except:
#                 pri = None
#             if pri:
#                 pri.delete()
#             try:
#                 poi = ProductPoint.objects.get(id=point_id)
#             except:
#                 poi = None
#             if poi:
#                 poi.delete()
#             try:
#                 dis = discount_product.objects.get(id=discount_id)
#             except:
#                 dis = None
#             if dis:
#                 dis.delete()
#             try:
#                 deli = DeliveryInfo.objects.get(id=delivery_id)
#             except:
#                 deli = None
#             if deli:
#                 deli.delete()
#             try:
#                 deli = ProductCode.objects.get(id=code_id)
#             except:
#                 deli = None
#             if deli:
#                 deli.delete()
#             return JsonResponse({
#                 "success": False,
#                 "message": "Something went wrong !!"
#             })

# 


# @api_view(['POST', ])
# def add_spec(request, product_id):
#     current_date = date.today()
#     specification_data_value = {
#         'product_id': product_id,
#         'color': request.data.get("color"),
#         'size': request.data.get("size"),
#         'weight': request.data.get("weight"),
#         'warranty': request.data.get("warranty"),
#         'warranty_unit': request.data.get("warranty_unit"),
#         'unit': request.data.get("product_unit"),
#         'vat': request.data.get("vat"),
#         # 'seller_quantity': request.data.get("seller_quantity"),
#         # 'remaining': request.data.get("seller_quantity"),
#         'manufacture_date': request.data.get("manufacture_date"),
#         'expire': request.data.get("expire")
#     }
#     product_price = {
#         'product_id': product_id,
#         'price': request.data.get("price"),
#         'purchase_price': request.data.get("purchase_price"),
#         # 'currency_id': request.data.get('currency_id')
#     }
#     discount_type = request.data.get("discount_type")
#     discount_amount = request.data.get("discount_amount")
#     discount_start_date = request.data.get("discount_start_date")
#     discount_end_date = request.data.get("discount_end_date")
#     point_amount = request.data.get("point_amount")
#     point_start_date = request.data.get("point_start_date")
#     point_end_date = request.data.get("point_end_date")
#     if discount_type == "none" or discount_amount == "" or discount_start_date == "" or discount_end_date == "":
#         discount_flag = False
#     else:
#         discount_flag = True
#     if point_amount == "" or point_start_date == "" or point_end_date == "":
#         point_flag = False
#     else:
#         point_flag = True
#     product_discount = {
#         'product_id': product_id,
#         'amount': request.data.get("discount_amount"),
#         'discount_type': request.data.get("discount_type"),
#         'start_date': request.data.get("discount_start_date"),
#         # 'end_date' : data['discount_end_date']
#         'end_date': request.data.get("discount_end_date")
#     }
#     product_point = {
#         'product_id': product_id,
#         'point': request.data.get("point_amount"),
#         # 'end_date': data['point_end_date']
#         'start_date': request.data.get("point_start_date"),
#         'end_date': request.data.get("point_end_date")
#     }
#     delivery_info = {
#         'height': request.data.get("delivery_height"),
#         'width': request.data.get("delivery_width"),
#         'length': request.data.get("delivery_length"),
#         'weight': request.data.get("delivery_weight"),
#         'measument_unit': request.data.get("delivery_product_unit"),
#         'charge_inside': request.data.get("delivery_inside_city_charge"),
#         'charge_outside': request.data.get("delivery_outside_city_charge"),
#     }
#     product_code = {
#         'product_id': product_id,
#         'manual_SKU' : request.data.get("SKU"),
#         'uid': request.data.get("uid"),
#     }
#     if request.method == 'POST':
#         delivery_id = 0
#         discount_id = 0
#         point_id = 0
#         price_id = 0
#         specification_id = 0
#         flag = 0
#         spec = {}
#         price = {}
#         discount = {}
#         point = {}
#         delivery = {}
#         code={}
#         try:
#             product_spec = ProductSpecificationSerializerz(
#                 data=specification_data_value)
#             if product_spec.is_valid():
#                 product_spec.save()
#                 # print("888888888888888888  spec save hoise")
#                 spec.update(product_spec.data)
#                 # print("Specification_id", spec["id"])
#                 specification_id = spec["id"]
#             else:
#                 # print(product_spec.errors)
#                 specification_id = 0
#                 flag = flag+1
#             product_price.update({'specification_id': spec['id']})
#             product_price = ProductPriceSerializer(data=product_price)
#             if product_price.is_valid():
#                 product_price.save()
#                 # print("price save hochche")
#                 price.update(product_price.data)
#                 price_id = price["id"]
#             else:
#                 price_id = 0
#                 flag = flag+1
#             if discount_flag == False:
#                 discount = {}
#             else:
#                 product_discount.update({'specification_id': spec['id']})
#                 # print("product_discount")
#                 # print(product_discount)
#                 product_dis = ProductDiscountSerializer(data=product_discount)
#                 if product_dis.is_valid():
#                     product_dis.save()
#                     # print("savwe hochche")
#                     discount.update(product_dis.data)
#                     discount_id = discount["id"]
#                 else:
#                     discount_id = 0
#                     flag = flag+1
#             if point_flag == False:
#                 point = {}
#             else:
#                 product_point.update({'specification_id': spec['id']})
#                 product_point_value = ProductPointSerializer(
#                     data=product_point)
#                 if product_point_value.is_valid():
#                     product_point_value.save()
#                     # print("point save")
#                     point.update(product_point_value.data)
#                     point_id = point["id"]
#                 else:
#                     point_id = 0
#                     # print(product_point_value.errors)
#                     flag = flag+1
#             delivery_info.update({'specification_id': spec['id']})
#             # print("here delivery",delivery_info )
#             delivery_value = DeliveryInfoSerializer(data=delivery_info)
#             # print("serializer",delivery_value)
#             if delivery_value.is_valid():
#                 # print("Inside the delivery ")
#                 delivery_value.save()
#                 # print("delivery is saved")
#                 delivery.update(delivery_value.data)
#                 delivery_id = delivery["id"]
#             else:
#                 delivery_id = 0
#                 # print("errors delivery " ,delivery_value.errors)
#                 flag = flag+1
#             product_code.update({'specification_id':spec['id']})
#             # print("product point",product_code )
#             product_code_value= ProductCodeSerializer (data=product_code)
#             # print("product code serial", product_code_value)
#             # print("before validation")
#             if product_code_value.is_valid():
#                 # print("inside validation")
#                 product_code_value.save()
#                 # print("code is saved", product_code_value.data)
#                 code.update(product_code_value.data)
#                 create_product_code(product_code)
#                 code_id = code["id"]
#                 # print("code id", code_id)
#             else:
#                 # print("code error", product_code_value.errors)
#                 flag= flag+1
#             if flag > 0:
#                 # print("xxxxxxxxxxxxxxx")
#                 return JsonResponse({
#                     "success": False,
#                     "message": "Something went wrong !!",
#                 })
#             else:
#                 return JsonResponse({
#                     "success": True,
#                     "message": "Specification data has been inserted Successfully",
#                     "specification": spec,
#                     "price": price,
#                     "discount": discount,
#                     "point": point,
#                     "delivery": delivery
#                 })
#         except:
#             try:
#                 spe = ProductSpecification.objects.get(id=specification_id)
#             except:
#                 spe = None
#             if spe:
#                 spe.delete()
#             try:
#                 pri = ProductPrice.objects.get(id=price_id)
#             except:
#                 pri = None
#             if pri:
#                 pri.delete()
#             try:
#                 poi = ProductPoint.objects.get(id=point_id)
#             except:
#                 poi = None
#             if poi:
#                 poi.delete()
#             try:
#                 dis = discount_product.objects.get(id=discount_id)
#             except:
#                 dis = None
#             if dis:
#                 dis.delete()
#             try:
#                 deli = DeliveryInfo.objects.get(id=delivery_id)
#             except:
#                 deli = None
#             if deli:
#                 deli.delete()
#             try:
#                 deli = ProductCode.objects.get(id=code_id)
#             except:
#                 deli = None
#             if deli:
#                 deli.delete()
#             return JsonResponse({
#                 "success": False,
#                 "message": "Something went wrong !!"
#             })



@api_view(['POST', ])
def add_spec2(request, product_id):

    current_date = date.today()

    specification_data_value = {
        'product_id': product_id,
        'color': request.data.get("color"),
        'size': request.data.get("size"),
        'weight': request.data.get("weight"),
        'warranty': request.data.get("warranty"),
        'warranty_unit': request.data.get("warranty_unit"),
        'unit': request.data.get("product_unit"),
        'vat': request.data.get("vat"),
        'seller_quantity': request.data.get("seller_quantity"),
        'remaining': request.data.get("seller_quantity"),
        'manufacture_date': request.data.get("manufacture_date"),
        'expire': request.data.get("expire"),
        'is_own' :True
    }

  
    product_price = {
        'product_id': product_id,
        'price': request.data.get("price"),
        'purchase_price': request.data.get("purchase_price"),
        # 'currency_id': request.data.get('currency_id')
    }


    discount_type = request.data.get("discount_type")
    discount_amount = request.data.get("discount_amount")
    discount_start_date = request.data.get("discount_start_date")
    discount_end_date = request.data.get("discount_end_date")
    point_amount = request.data.get("point_amount")
    point_start_date = request.data.get("point_start_date")
    point_end_date = request.data.get("point_end_date")

    if discount_type == "none" or discount_amount == "" or discount_start_date == "" or discount_end_date == "":
        discount_flag = False
    else:
        discount_flag = True
    if point_amount == "" or point_start_date == "" or point_end_date == "":
        point_flag = False
    else:
        point_flag = True

    product_discount = {
        'product_id': product_id,
        'amount': request.data.get("discount_amount"),
        'discount_type': request.data.get("discount_type"),
        'start_date': request.data.get("discount_start_date"),
        # 'end_date' : data['discount_end_date']
        'end_date': request.data.get("discount_end_date")
    }


    product_point = {
        'product_id': product_id,
        'point': request.data.get("point_amount"),
        # 'end_date': data['point_end_date']
        'start_date': request.data.get("point_start_date"),
        'end_date': request.data.get("point_end_date")
    }


    delivery_info = {
        'height': request.data.get("delivery_height"),
        'width': request.data.get("delivery_width"),
        'length': request.data.get("delivery_length"),
        'weight': request.data.get("delivery_weight"),
        'measument_unit': request.data.get("delivery_product_unit"),
        'charge_inside': request.data.get("delivery_inside_city_charge"),
        'charge_outside': request.data.get("delivery_outside_city_charge"),
    }


    product_code = {
        'product_id': product_id,
        'manual_SKU' : request.data.get("SKU")
    }

    if request.method == 'POST':
        delivery_id = 0
        discount_id = 0
        point_id = 0
        price_id = 0
        specification_id = 0
        flag = 0
        spec = {}
        price = {}
        discount = {}
        point = {}
        delivery = {}
        code={}
        try:
            product_spec = ProductSpecificationSerializerz(
                data=specification_data_value)
            if product_spec.is_valid():
                product_spec.save()
                # print("888888888888888888  spec save hoise")
                spec.update(product_spec.data)
                # print("Specification_id", spec["id"])
                specification_id = spec["id"]
            else:
                # print(product_spec.errors)
                specification_id = 0
                flag = flag+1

            product_price.update({'specification_id': spec['id']})
            product_price = ProductPriceSerializer(data=product_price)
            if product_price.is_valid():
                product_price.save()
                # print("price save hochche")
                price.update(product_price.data)
                price_id = price["id"]
            else:
                price_id = 0
                flag = flag+1

            if discount_flag == False:
                discount = {}
            else:
                product_discount.update({'specification_id': spec['id']})
                # print("product_discount")
                # print(product_discount)
                product_dis = ProductDiscountSerializer(data=product_discount)
                if product_dis.is_valid():
                    product_dis.save()
                    # print("savwe hochche")
                    discount.update(product_dis.data)
                    discount_id = discount["id"]
                else:
                    discount_id = 0
                    flag = flag+1

            if point_flag == False:
                point = {}
            else:
                product_point.update({'specification_id': spec['id']})
                product_point_value = ProductPointSerializer(
                    data=product_point)
                if product_point_value.is_valid():
                    product_point_value.save()
                    # print("point save")
                    point.update(product_point_value.data)
                    point_id = point["id"]
                else:
                    point_id = 0
                    # print(product_point_value.errors)
                    flag = flag+1


            delivery_info.update({'specification_id': spec['id']})
            # print("here delivery",delivery_info )
            delivery_value = DeliveryInfoSerializer(data=delivery_info)
            # print("serializer",delivery_value)
            if delivery_value.is_valid():
                # print("Inside the delivery ")
                delivery_value.save()
                # print("delivery is saved")
                delivery.update(delivery_value.data)
                delivery_id = delivery["id"]
            else:
                delivery_id = 0
                # print("errors delivery " ,delivery_value.errors)
                flag = flag+1


            product_code.update({'specification_id':spec['id']})
            # print("product point",product_code )
            product_code_value= ProductCodeSerializer (data=product_code)
            # print("product code serial", product_code_value)
            # print("before validation")
            if product_code_value.is_valid():
                # print("inside validation")
                product_code_value.save()
                # print("code is saved", product_code_value.data)
                code.update(product_code_value.data)
                # print("update code info",code )
                create_product_code(product_code)
                code_id = code["id"]
                # print("code id", code_id)
            else:
                # print("code error", product_code_value.errors)
                flag= flag+1

            if flag > 0:
                # print("xxxxxxxxxxxxxxx")
                return JsonResponse({
                    "success": False,
                    "message": "Something went wrong !!",
                })
            else:
                return JsonResponse({
                    "success": True,
                    "message": "Specification data has been inserted Successfully",
                    "specification": spec,
                    "price": price,
                    "discount": discount,
                    "point": point,
                    "delivery": delivery
                })
        except:
            
            try:
                spe = ProductSpecification.objects.get(id=specification_id)
            except:
                spe = None
            if spe:
                spe.delete()
            try:
                pri = ProductPrice.objects.get(id=price_id)
            except:
                pri = None
            if pri:
                pri.delete()
            try:
                poi = ProductPoint.objects.get(id=point_id)
            except:
                poi = None
            if poi:
                poi.delete()
            try:
                dis = discount_product.objects.get(id=discount_id)
            except:
                dis = None
            if dis:
                dis.delete()
            try:
                deli = DeliveryInfo.objects.get(id=delivery_id)
            except:
                deli = None
            if deli:
                deli.delete()
            try:
                deli = ProductCode.objects.get(id=code_id)
            except:
                deli = None
            if deli:
                deli.delete()
            return JsonResponse({
                "success": False,
                "message": "Something went wrong !!"
            })



# @api_view(['POST', ])
# def add_spec2(request, product_id):
#     current_date = date.today()
#     print(request.data)
#     specification_data_value = {
#         'product_id': product_id,
#         'color': request.data.get("color"),
#         'size': request.data.get("size"),
#         'weight': request.data.get("weight"),
#         'warranty': request.data.get("warranty"),
#         'warranty_unit': request.data.get("warranty_unit"),
#         'unit': request.data.get("product_unit"),
#         'vat': request.data.get("vat"),
#         'seller_quantity': request.data.get("seller_quantity"),
#         'remaining': request.data.get("seller_quantity"),
#         'manufacture_date': request.data.get("manufacture_date"),
#         'expire': request.data.get("expire")
#     }
#     product_price = {
#         'product_id': product_id,
#         'price': request.data.get("price"),
#         'purchase_price': request.data.get("purchase_price"),
#         # 'currency_id': request.data.get('currency_id')
#     }
#     discount_type = request.data.get("discount_type")
#     discount_amount = request.data.get("discount_amount")
#     discount_start_date = request.data.get("discount_start_date")
#     discount_end_date = request.data.get("discount_end_date")
#     point_amount = request.data.get("point_amount")
#     point_start_date = request.data.get("point_start_date")
#     point_end_date = request.data.get("point_end_date")
#     if discount_type == "none" or discount_amount == "" or discount_start_date == "" or discount_end_date == "":
#         discount_flag = False
#     else:
#         discount_flag = True
#     if point_amount == "" or point_start_date == "" or point_end_date == "":
#         point_flag = False
#     else:
#         point_flag = True
#     product_discount = {
#         'product_id': product_id,
#         'amount': request.data.get("discount_amount"),
#         'discount_type': request.data.get("discount_type"),
#         'start_date': request.data.get("discount_start_date"),
#         # 'end_date' : data['discount_end_date']
#         'end_date': request.data.get("discount_end_date")
#     }
#     product_point = {
#         'product_id': product_id,
#         'point': request.data.get("point_amount"),
#         # 'end_date': data['point_end_date']
#         'start_date': request.data.get("point_start_date"),
#         'end_date': request.data.get("point_end_date")
#     }
#     delivery_info = {
#         'height': request.data.get("delivery_height"),
#         'width': request.data.get("delivery_width"),
#         'length': request.data.get("delivery_length"),
#         'weight': request.data.get("delivery_weight"),
#         'measument_unit': request.data.get("delivery_product_unit"),
#         'charge_inside': request.data.get("delivery_inside_city_charge"),
#         'charge_outside': request.data.get("delivery_outside_city_charge"),
#     }
#     product_code = {
#         'product_id': product_id,
#         'manual_SKU' : request.data.get("sku")
#     }
#     if request.method == 'POST':
#         delivery_id = 0
#         discount_id = 0
#         point_id = 0
#         price_id = 0
#         specification_id = 0
#         flag = 0
#         spec = {}
#         price = {}
#         discount = {}
#         point = {}
#         delivery = {}
#         code={}
#         try:
#             product_spec = ProductSpecificationSerializerz(
#                 data=specification_data_value)
#             if product_spec.is_valid():
#                 product_spec.save()
#                 # print("888888888888888888  spec save hoise")
#                 spec.update(product_spec.data)
#                 # print("Specification_id", spec["id"])
#                 specification_id = spec["id"]
#             else:
#                 # print(product_spec.errors)
#                 specification_id = 0
#                 flag = flag+1
#             product_price.update({'specification_id': spec['id']})
#             product_price = ProductPriceSerializer(data=product_price)
#             if product_price.is_valid():
#                 product_price.save()
#                 # print("price save hochche")
#                 price.update(product_price.data)
#                 price_id = price["id"]
#             else:
#                 price_id = 0
#                 flag = flag+1
#             if discount_flag == False:
#                 discount = {}
#             else:
#                 product_discount.update({'specification_id': spec['id']})
#                 # print("product_discount")
#                 # print(product_discount)
#                 product_dis = ProductDiscountSerializer(data=product_discount)
#                 if product_dis.is_valid():
#                     product_dis.save()
#                     # print("savwe hochche")
#                     discount.update(product_dis.data)
#                     discount_id = discount["id"]
#                 else:
#                     discount_id = 0
#                     flag = flag+1
#             if point_flag == False:
#                 point = {}
#             else:
#                 product_point.update({'specification_id': spec['id']})
#                 product_point_value = ProductPointSerializer(
#                     data=product_point)
#                 if product_point_value.is_valid():
#                     product_point_value.save()
#                     # print("point save")
#                     point.update(product_point_value.data)
#                     point_id = point["id"]
#                 else:
#                     point_id = 0
#                     # print(product_point_value.errors)
#                     flag = flag+1
#             delivery_info.update({'specification_id': spec['id']})
#             # print("here delivery",delivery_info )
#             delivery_value = DeliveryInfoSerializer(data=delivery_info)
#             # print("serializer",delivery_value)
#             if delivery_value.is_valid():
#                 # print("Inside the delivery ")
#                 delivery_value.save()
#                 # print("delivery is saved")
#                 delivery.update(delivery_value.data)
#                 delivery_id = delivery["id"]
#             else:
#                 delivery_id = 0
#                 # print("errors delivery " ,delivery_value.errors)
#                 flag = flag+1
#             product_code.update({'specification_id':spec['id']})
#             # print("product point",product_code )
#             product_code_value= ProductCodeSerializer (data=product_code)
#             # print("product code serial", product_code_value)
#             # print("before validation")
#             if product_code_value.is_valid():
#                 # print("inside validation")
#                 product_code_value.save()
#                 # print("code is saved", product_code_value.data)
#                 code.update(product_code_value.data)
#                 # print("update code info",code )
#                 code_id = code["id"]
#                 # print("code id", code_id)
#             else:
#                 # print("code error", product_code_value.errors)
#                 flag= flag+1
#             if flag > 0:
#                 # print("xxxxxxxxxxxxxxx")
#                 return JsonResponse({
#                     "success": False,
#                     "message": "Something went wrong !!",
#                 })
#             else:
#                 return JsonResponse({
#                     "success": True,
#                     "message": "Specification data has been inserted Successfully",
#                     "specification": spec,
#                     "price": price,
#                     "discount": discount,
#                     "point": point,
#                     "delivery": delivery
#                 })
#         except:
#             try:
#                 spe = ProductSpecification.objects.get(id=specification_id)
#             except:
#                 spe = None
#             if spe:
#                 spe.delete()
#             try:
#                 pri = ProductPrice.objects.get(id=price_id)
#             except:
#                 pri = None
#             if pri:
#                 pri.delete()
#             try:
#                 poi = ProductPoint.objects.get(id=point_id)
#             except:
#                 poi = None
#             if poi:
#                 poi.delete()
#             try:
#                 dis = discount_product.objects.get(id=discount_id)
#             except:
#                 dis = None
#             if dis:
#                 dis.delete()
#             try:
#                 deli = DeliveryInfo.objects.get(id=delivery_id)
#             except:
#                 deli = None
#             if deli:
#                 deli.delete()
#             try:
#                 deli = ProductCode.objects.get(id=code_id)
#             except:
#                 deli = None
#             if deli:
#                 deli.delete()
#             return JsonResponse({
#                 "success": False,
#                 "message": "Something went wrong !!"
#             })


@api_view(["GET", "POST"])
def confirm_products(request):
    values = {
        "order_id": 1,
        "quantity": 2000000,
        "store": "warehouse",
        "ware_name": "sheba.xyz",
        "ware_house_id": 1
    }

    if(request.method == "POST"):

        ware_house = []
        shops = []
        flag = 0
        reminder = -1

        try:

            order_info = OrderDetails.objects.filter(
                order_id=values['order_id'])
            for orders in order_info:
                all_quantity_data = OrderDetails.objects.get(
                    product_id=orders.product_id, product_size=orders.product_size, product_color=orders.product_color)
                specific_quantity = all_quantity_data.total_quantity
                if(values['quantity'] > specific_quantity):
                    flag = flag+1
                else:
                    print("specific quantity", specific_quantity)
                    if (values['store'] == "warehouse"):
                        ware_house_info = Warehouse.objects.get(
                            id=values['ware_house_id'])
                        quantity = ware_house_info.product_quantity
                        if(values['quantity'] > quantity):
                            flag = flag+1
                        else:
                            print("before add", ware_house_info.product_quantity)
                            ware_house_info.product_quantity = (
                                quantity - values['quantity'])
                            ware_house_info.save()
                            print("after add", ware_house_info.product_quantity)
                            reminder = specific_quantity-values['quantity']

                    elif (values['store'] == "shop"):
                        shop_house_info = Shop.objects.get(
                            id=values['ware_house_id'])
                        quantity = shop_house_info.product_quantity
                        if(values['quantity'] > quantity):
                            flag = flag+1
                        else:
                            shop_house_info.product_quantity = (
                                quantity - values['quantity'])
                            shop_house_info.save()
                            reminder = specific_quantity-values['quantity']

            if(reminder < 0):
                reminder = 0

        except:
            return Response({'Message': 'Check whether requested data exists or not'})

        if (flag > 0):
            return Response({
                "success": False,
                "Message": "You set wrong values !!"
            })
        else:
            return Response({
                "success": True,
                "Message": "Information has been updated",
                "reminder": reminder
            })


@api_view(["POST", ])
def create_warehouse(request):

    serializer = WarehouseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Warehouse has been created", "data": serializer.data})

    else:

        return Response({"success": True, "message": "Warehouse could not be created"})


@api_view(["POST", ])
def create_shop(request):

    serializer = ShopSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Shop has been created", "data": serializer.data})

    else:

        return Response({"success": True, "message": "Shop could not be created"})


@api_view(["POST", ])
def update_shop(request, shop_id):

    try:

        shop = Shop.objects.get(id=shop_id)

    except:

        shop = None

    if shop:

        serializer = ShopSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Shop data has been updated", "data": serializer.data})

        else:

            return Response({"success": True, "message": "Shop data could not be updated"})

    else:

        return Response({"success": True, "message": "Shop does not exist"})


@api_view(["POST", ])
def update_warehouse(request, warehouse_id):

    try:

        warehouse = Warehouse.objects.get(id=warehouse_id)

    except:

        warehouse = None

    if warehouse:

        serializer = WarehouseSerializer(warehouse, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Warehouse data has been updated", "data": serializer.data})

        else:

            return Response({"success": True, "message": "Warehouse data could not be updated"})

    else:

        return Response({"success": True, "message": "Warehouse does not exist"})


@api_view(["GET", ])
def show_all_warehouses(request):

    try:

        warehouse = Warehouse.objects.all()

    except:

        warehouse = None

    if warehouse:

        serializer = WarehouseSerializer(warehouse, many=True)
        return Response({"success": True, "message": "Data is shown", "data": serializer.data})

    else:

        return Response({"success": False, "message": "No data could be retrieved", "data": []})


@api_view(["GET", ])
def show_all_shops(request):

    try:

        warehouse = Shop.objects.all()

    except:

        warehouse = None

    if warehouse:

        serializer = ShopSerializer(warehouse, many=True)
        return Response({"success": True, "message": "Data is shown", "data": serializer.data})

    else:

        return Response({"success": False, "message": "No data could be retrieved", "data": []})


def delete_warehouse(request, warehouse_id):

    try:

        warehouse = Warehouse.objects.get(id=warehouse_id)

    except:

        warehouse = None

    if warehouse:

        warehouse.delete()
        return JsonResponse({"success": True, "message": "Warehouse has been deleted"})

    else:
        return JsonResponse({"success": False, "message": "Warehouse does not exist"})


def delete_shop(request, shop_id):

    try:

        warehouse = Shop.objects.get(id=shop_id)

    except:

        warehouse = None

    if warehouse:

        warehouse.delete()
        return JsonResponse({"success": True, "message": "Shop has been deleted"})

    else:
        return JsonResponse({"success": False, "message": "Shop does not exist"})


@api_view(["GET", ])
def inventory_lists(request, order_details_id):

    try:

        product = OrderDetails.objects.get(id=order_details_id)

    except:

        product = None
        
    print(product)

    if product:

        product_id = product.product_id
        product_size = product.product_size
        product_color = product.product_color
        product_specification_id = product.specification_id

        try:

            spec = ProductSpecification.objects.get(id=product_specification_id)

        except:

            spec = None

        if spec:

            specification_id = spec.id
            print(specification_id)

            try:

                warehouses = WarehouseInfo.objects.filter(
                    specification_id=specification_id)

            except:

                warehouses = None

            print(warehouses)

            warehouse_infos = []

            if warehouses:

                warehouse_ids = list(
                    warehouses.values_list('warehouse_id', flat=True))
                warehouse_quantities = list(
                    warehouses.values_list('quantity', flat=True))

                for i in range(len(warehouse_ids)):

                    try:
                        warehouse = Warehouse.objects.get(id=warehouse_ids[i])
                    except:
                        warehouse = None

                    if warehouse:

                        name = warehouse.warehouse_name
                        location = warehouse.warehouse_location
                        quantity = warehouse_quantities[i]

                        warehouse_data = {
                            "id": warehouse_ids[i], "name": name, "location": location, "quantity": quantity}

                    else:

                        warehouse_data = {}

                    warehouse_infos.append(warehouse_data)

            else:

                warehouse_infos = []

            try:

                shops = ShopInfo.objects.filter(
                    specification_id=specification_id)

            except:

                shops = None

            shop_infos = []

            if shops:

                shop_ids = list(shops.values_list('shop_id', flat=True))
                shop_quantities = list(
                    shops.values_list('quantity', flat=True))

                for i in range(len(shop_ids)):

                    try:
                        shop = Shop.objects.get(id=shop_ids[i])
                    except:
                        shop = None

                    if warehouse:

                        name = shop.shop_name
                        location = shop.shop_location
                        quantity = shop_quantities[i]

                        shop_data = {
                            "id": shop_ids[i], "name": name, "location": location, "quantity": quantity}

                    else:

                        shop_data = {}

                    shop_infos.append(shop_data)

            else:

                shop_infos = []

        else:
            warehouse_infos = []
            shop_infos = []

    return JsonResponse({'success': True, 'message': 'Data is shown below', 'warehouse': warehouse_infos, 'shop': shop_infos})


@api_view(["GET", ])
def warehouse_products(request, warehouse_id):

    try:

        products = Warehouse.objects.get(id=warehouse_id)

    except:

        products = None

    if products:

        warehouse_serializer = WarehouseSerializer(products, many=False)
        warehouse_data = warehouse_serializer.data
        return JsonResponse({'success': True, 'message': 'Here is the data', 'data': warehouse_data})

    else:

        warehouse_data = {}
        return JsonResponse({'success': False, 'message': 'Here is the data', 'data': warehouse_data})


@api_view(["GET", ])
def shop_products(request, shop_id):

    try:

        products = Shop.objects.get(id=shop_id)

    except:

        products = None

    if products:

        warehouse_serializer = ShopSerializer(products, many=False)
        warehouse_data = warehouse_serializer.data
        return JsonResponse({'success': True, 'message': 'Here is the data', 'data': warehouse_data})

    else:

        warehouse_data = {}
        return JsonResponse({'success': False, 'message': 'Here is the data', 'data': warehouse_data})

# ----------------------------------- quantity store in different shop/inventory ------------------------


@api_view(["GET", "POST"])
def insert_product_quantity(request):

    # demo values
    # api_values = {
    #     'product_id':35,
    #     'specification_id':34,
    #     'purchase_price': 100,
    #     'selling_price': 120,
    #     'warehouse': [
    #         {
    #             'warehouse_id': 1,
    #             'quantity': 200

    #         },
    #         {
    #             'warehouse_id': 2,
    #             'quantity': 200

    #         }
    #     ],

    #      'shop': [
    #         {
    #             'shop_id': 3,
    #             'quantity': 200

    #         },
    #         {
    #             'shop_id': 2,
    #             'quantity': 200

    #         },
    #         {
    #             'shop_id': 1,
    #             'quantity': 200

    #         }


    #     ]

    #     }

    api_values = request.data
    current_date = date.today()

    if request.method == 'POST':

        #Insert the purchase price and selling price for that object:

        try:

            price_data = {"product_id":api_values["product_id"],"specification_id":api_values["specification_id"],"price":api_values["selling_price"],"purchase_price":api_values["purchase_price"]}

            #Inserting the price

            product_price_serializer = ProductPriceSerializer(data = price_data)
            if product_price_serializer.is_valid():
                product_price_serializer.save()


        except:

            return JsonResponse({"success":False,"message":"The price could not be inserted"})



        try:
            #Fetching the product price 

            prod_price = ProductPrice.objects.filter(specification_id=api_values["specification_id"]).last()

        except:

            prod_price = None 

        if prod_price:

            purchase_price = prod_price.purchase_price
            selling_price = prod_price.price

        else:

            return JsonResponse({"success":False,"message":"Price does not exist for this product"})


        try:

            # checking is there any warehouse data exists or not
            if len(api_values['warehouse']) > 0:
                for wareh in api_values['warehouse']:
                    try:
                        # getting the previous data if there is any in the similar name. If exists update the new value. if does not create new records.
                        wareh_query = WarehouseInfo.objects.filter(
                            warehouse_id=wareh['warehouse_id'], specification_id=api_values['specification_id']).last()

                        print("quertresult")
                        print(wareh_query)

                        if wareh_query:
                            # quantity_val = wareh_query[0].quantity
                            # new_quantity = quantity_val + wareh['quantity']
                            # wareh_query.update(quantity=new_quantity)
                            # wareh_query.save()
                            print("existing warehouse")
                            print(type(wareh['quantity']))
                            print(wareh_query.quantity)

                            warehouse_quantity =  wareh_query.quantity

                            print(warehouse_quantity)

                            new_quantity =  warehouse_quantity + int(wareh['quantity'])

                            print(new_quantity)

                            wareh_query.quantity = new_quantity
                            print(wareh_query.quantity)
                            wareh_query.save()
                            print(wareh_query.quantity)

                            try:
                                product_spec = ProductSpecification.objects.get(id=api_values['specification_id'])

                            except:
                                product_spec = None 

                            if product_spec:

                                product_spec.save()




                        else:
                            print("else ey dhuktese")
                            wareh_data = WarehouseInfo.objects.create(specification_id=api_values['specification_id'], product_id=api_values['product_id'], warehouse_id=wareh['warehouse_id'],
                                                       quantity=int(wareh['quantity']))
                            wareh_data.save()

                            try:
                                product_spec = ProductSpecification.objects.get(id=api_values['specification_id'])

                            except:
                                product_spec = None 

                            if product_spec:

                                product_spec.save()

                        # updating the inventory report credit records for each ware house quantity. It will help to keep the records in future.
                        # report_data = inventory_report(
                        #     product_id=api_values['product_id'], credit=wareh['quantity'], warehouse_id=wareh['warehouse_id'])
                        # report_data.save()
                        #Check to see if there are any inventory_reports
                        # try:

                        #     report = inventory_report.objects.filter(product_id=api_values['product_id'],specification_id=api_values['specification_id'],warehouse_id=wareh['warehouse_id'],date=current_date).last()

                        # except:

                        #     report = None 


                        # if report:

                        #     #Update the existing report

                        #     report.credit += int(wareh['quantity'])
                        #     report.save()




                        new_report = inventory_report.objects.create(product_id=api_values['product_id'],specification_id=api_values['specification_id'],warehouse_id=wareh['warehouse_id'],credit=int(wareh['quantity']),date=current_date,purchase_price=purchase_price,selling_price=selling_price)
                        new_report.save()



                    except:
                        pass

            if len(api_values['shop']) > 0:
                for shops in api_values['shop']:
                    try:
                        # getting the existing shop values if is there any.
                        print(shops['shop_id'])
                        shop_query = ShopInfo.objects.filter(
                            shop_id=shops['shop_id'], specification_id=api_values['specification_id']).last()
                        print(shop_query)
                        if shop_query:
                            print("shop ase")
                            quantity_val = shop_query.quantity
                            new_quantity = quantity_val + int(shops['quantity'])
                            # shop_query.update(quantity=new_quantity)
                            shop_query.quantity = new_quantity
                            shop_query.save()

                            try:
                                product_spec = ProductSpecification.objects.get(id=api_values['specification_id'])

                            except:
                                product_spec = None 

                            if product_spec:

                                product_spec.save()
                        else:
                            print("shop nai")
                            shop_data = ShopInfo.objects.create(specification_id=api_values['specification_id'], product_id=api_values['product_id'], shop_id=shops['shop_id'],
                                                 quantity=int(shops['quantity']))
                            shop_data.save()
                        # Updating the report table after being inserted the quantity corresponding to credit coloumn for each shop.
                        # report_data = inventory_report(
                        #     product_id=api_values['product_id'], credit=shops['quantity'], shop_id=shops['shop_id'])
                        # report_data.save()

                            try:
                                product_spec = ProductSpecification.objects.get(id=api_values['specification_id'])

                            except:
                                product_spec = None 

                            if product_spec:

                                product_spec.save()
                            







                        new_report = inventory_report.objects.create(product_id=api_values['product_id'],specification_id=api_values['specification_id'],shop_id=shops['shop_id'],credit=int(shops['quantity']),date=current_date,purchase_price=purchase_price,selling_price=selling_price)
                        new_report.save()

                    except:
                        pass

            return Response({
                "success": True,
                "message": "Data has been added successfully"
            })
        except:
            return Response({
                "success": False,
                "message": "Something went wrong !!"
            })


@api_view(["GET", "POST"])
def get_all_quantity_list(request, specification_id):

    if request.method == 'GET':

        try:
            warehouse_values = []
            shop_values = []
            warehouse_ids = []
            shop_ids = []
            warehouse_query = WarehouseInfo.objects.filter(
                specification_id=specification_id)
            print(warehouse_query)
            wh_name = Warehouse.objects.all()
            print(wh_name)
            for wq in warehouse_query:
                print(wq.warehouse_id)
                warehouse_data = Warehouse.objects.get(id=wq.warehouse_id)
                wh_data = {"warehouse_id": warehouse_data.id, "previous_quantity": wq.quantity,
                           "warehouse_name": warehouse_data.warehouse_name}
                print(wh_data)
                warehouse_values.append(wh_data)
                warehouse_ids.append(wq.warehouse_id)

            print(warehouse_values)
            for warehouse in wh_name:
                if warehouse.id not in warehouse_ids:
                    wh_data = {"warehouse_id": warehouse.id, "previous_quantity": 0,
                               "warehouse_name": warehouse.warehouse_name}
                    warehouse_values.append(wh_data)

            print(warehouse_values)

            shopinfo_query = ShopInfo.objects.filter(
                specification_id=specification_id)
            all_shops = Shop.objects.all()
            print(shopinfo_query)
            print(all_shops)
            for shop in shopinfo_query:
                shop_data = Shop.objects.get(id=shop.shop_id)
                datas = {"shop_id": shop_data.id, "previous_quantity": shop.quantity,
                         "shop_name": shop_data.shop_name}
                shop_values.append(datas)
                shop_ids.append(shop.shop_id)

            for shops in all_shops:
                if shops.id not in shop_ids:
                    datas = {"shop_id": shops.id, "previous_quantity": 0,
                             "shop_name": shops.shop_name}
                    shop_values.append(datas)

            return JsonResponse({
                "success": True,
                "message": "Data has been retrieved successfully",
                "data": {
                    "warehouse": warehouse_values,
                    "shop": shop_values
                }
            })
        except:
            return JsonResponse({
                "success": False,
                "message": "Something went wrong"
            })



# @api_view(["GET", "POST"])
# def get_all_quantity_list_and_price(request, specification_id):

#     if request.method == 'GET':


#         purchase_price = 0 
#         selling_price = 0 

#         try:
#             spec_price = SpecificationPrice.objects.filter(specification_id = specification_id,status="Single").last()
#         except:
#             spec_price = None


#         if spec_price:
#             purchase_price = spec_price.purchase_price
#             selling_price = spec_price.mrp


        


#         try:
#             warehouse_values = []
#             shop_values = []
#             warehouse_ids = []
#             shop_ids = []
#             warehouse_query = WarehouseInfo.objects.filter(
#                 specification_id=specification_id)
#             print(warehouse_query)
#             wh_name = Warehouse.objects.all()
#             print(wh_name)
#             for wq in warehouse_query:
#                 print(wq.warehouse_id)
#                 warehouse_data = Warehouse.objects.get(id=wq.warehouse_id)
#                 wh_data = {"warehouse_id": warehouse_data.id, "previous_quantity": wq.quantity,
#                            "warehouse_name": warehouse_data.warehouse_name}
#                 print(wh_data)
#                 warehouse_values.append(wh_data)
#                 warehouse_ids.append(wq.warehouse_id)

#             print(warehouse_values)
#             for warehouse in wh_name:
#                 if warehouse.id not in warehouse_ids:
#                     wh_data = {"warehouse_id": warehouse.id, "previous_quantity": 0,
#                                "warehouse_name": warehouse.warehouse_name}
#                     warehouse_values.append(wh_data)

#             print(warehouse_values)

#             shopinfo_query = ShopInfo.objects.filter(
#                 specification_id=specification_id)
#             all_shops = Shop.objects.all()
#             print(shopinfo_query)
#             print(all_shops)
#             for shop in shopinfo_query:
#                 shop_data = Shop.objects.get(id=shop.shop_id)
#                 datas = {"shop_id": shop_data.id, "previous_quantity": shop.quantity,
#                          "shop_name": shop_data.shop_name}
#                 shop_values.append(datas)
#                 shop_ids.append(shop.shop_id)

#             for shops in all_shops:
#                 if shops.id not in shop_ids:
#                     datas = {"shop_id": shops.id, "previous_quantity": 0,
#                              "shop_name": shops.shop_name}
#                     shop_values.append(datas)

#             return JsonResponse({
#                 "success": True,
#                 "message": "Data has been retrieved successfully",
#                 "data": {
#                     "warehouse": warehouse_values,
#                     "shop": shop_values ,
#                     "purchase_price": purchase_price,
#                     "selling_price" : selling_price

#                 }
#             })
#         except:
#             return JsonResponse({
#                 "success": False,
#                 "message": "Something went wrong"
#             })

@api_view(["GET", "POST"])
def create_all_brand(request):

    brand_name = request.data.get("Brand_name")
    brand_owner = request.data.get("Brand_owner")
    brand_country = request.data.get("Brand_country")

    brand_name = brand_name.capitalize()
    print(brand_name)

    data = {'Brand_name':brand_name,'Brand_country':brand_country,'Brand_owner':brand_owner}

    try:

        brands = ProductBrand.objects.all()

    except:

        brands = None 


    flag = 0 


    if brands:

        brand_list=list(brands.values_list('Brand_name',flat=True))
        brand_ids=list(brands.values_list('id',flat=True))

        for i in range(len(brand_list)):

            brand_upper = brand_list[i].upper()
            # print(brand_upper)

            brand_lower = brand_list[i].lower()
            # print(brand_lower)



            if brand_name == brand_list[i]:
                brand_name = brand_list[i]
                brand_id = brand_ids[i]
                flag = 1 
                break

            # elif brand_name == brand_upper:

            #     brand_name = brand_upper
            #     flag = 1 
            #     break

            # elif brand_name == brand_lower:

            #     brand_name = brand_lower 
            #     flag = 1 

            #     break 


        message = "The brand " + brand_name + " already exists."
        print(message)


        if flag == 1: 

            return JsonResponse({'success':False,'message': message,'brand_id':brand_id})

        else:

            serializer = AddBrandSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    "success": True,
                    "message": "Brand has been inserted successfully",
                    "data": serializer.data
                })

    else:

        serializer = AddBrandSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "success": True,
                "message": "Brand has been inserted successfully",
                "data": serializer.data
            })

    












@api_view(["GET", "POST"])
def get_all_brand(request):

    if request.method == 'GET':
        try:
            brand_query = ProductBrand.objects.all()
            brand_serializers = AddBrandSerializer(brand_query, many=True)
            return JsonResponse({
                "success": True,
                "message": "Brand has been retrived successfully",
                "data": brand_serializers.data
            })
        except:
            return JsonResponse({
                "success": False,
                "message": "SSomething Went wrong"
            })


@api_view(["GET", "POST"])
def delete_specific_brand(request, brand_id):
    if request.method == 'POST':
        try:
            product_brand = ProductBrand.objects.get(id=brand_id)
        except:
            product_brand = None
        if product_brand:
            if product_brand.Brand_name == "Individual":
                return JsonResponse({
                    "success": False,
                    "message": "You are not allowed to delete Individual Brand"})
            else:
                product_brand.delete()
                return JsonResponse({
                    "success": True,
                    "message": "Desired Brand has been deleted successfully"})
        else:
            return JsonResponse({
                "success": False,
                "message": "Desired Brand does not exist"
            })


@api_view(["GET", "POST"])
def update_specific_brand(request, brand_id):
    if request.method == 'POST':
        try:
            product_brand = ProductBrand.objects.get(id=brand_id)
        except:
            product_brand = None
        if product_brand:
            if product_brand.Brand_name == "Individual":
                return JsonResponse({
                    "success": False,
                    "message": "You are not allowed to modify Individual Brand"})
            else:
                brand_serializers = AddBrandSerializer(
                    product_brand, data=request.data)
                if brand_serializers.is_valid():
                    brand_serializers.save()
                    return JsonResponse({
                        "success": True,
                        "message": "Desired Brand has been modified successfully",
                        "data": brand_serializers.data})
        else:
            return JsonResponse({
                "success": False,
                "message": "Desired Brand does not exist"
            })




# def warehouse
@api_view(["GET",])
def warehouse_report(request):


    try:

        report = inventory_report.objects.filter(shop_id = -1)

    except:

        report = None 

    print(report)


    if report:

        report_serializer = InventoryReportSerializer(report,many=True)
        return JsonResponse({'success':True,'message':'Data is shown','data':report_serializer.data})



    else:

        return JsonResponse({'success':False,'message':'Data is not shown'})





# def warehouse
@api_view(["GET",])
def shop_report(request):


    try:

        report = inventory_report.objects.filter(warehouse_id = -1)

    except:

        report = None 


    if report:

        report_serializer = InventoryReportSerializer(report,many=True)
        return JsonResponse({'success':True,'message':'Data is shown','data':report_serializer.data})



    else:

        return JsonResponse({'success':False,'message':'Data is not shown'})




@api_view(["GET", "POST"])
def get_subtracted_value(request, order_id,specification_id):
    if request.method == "GET":
        try:
            values=[]
            all_info=[]
            spec_value={}
            all_ware=[]
            all_shop=[]
            tracking_values = subtraction_track.objects.filter(order_id = order_id)
            for track in tracking_values:
                values.append(track.specification_id)
            values = set(values)
            data_values = subtraction_track.objects.filter(order_id = order_id, specification_id = specification_id)
            for itenary in data_values:
                ware_house={}
                shop_house ={}
                if itenary.warehouse_id != -1:
                    try:
                        ware_info = Warehouse.objects.get(id = itenary.warehouse_id)
                        ware_name = ware_info.warehouse_name
                    except:
                        ware_name = None
                    ware_house.update({'warehouse_id': itenary.warehouse_id, 'warehouse_name':ware_name , 'added_quantity':itenary.debit_quantity, 'date': itenary.date})
                    all_ware.append(ware_house)
                if itenary.shop_id != -1:
                    try:
                        shop_info = Shop.objects.get(id = itenary.shop_id )
                        shop_name = shop_info.shop_name
                    except:
                        shop_name = None
                    shop_house.update({'shop_id': itenary.shop_id,'shop_name':shop_name, 'added_quantity':itenary.debit_quantity, 'date': itenary.date})
                    all_shop.append(shop_house)
            allshops = Shop.objects.all()
            shopinfos = []
            for shp in all_shop:
                shopinfos.append(shp['shop_id'])
            for shop_val in allshops:
                shop_house ={}
                if shop_val.id not in shopinfos:
                    shop_house.update({'shop_id': shop_val.id,'shop_name':shop_val.shop_name, 'added_quantity':0, 'date': ''})
                    all_shop.append(shop_house)
            allware = Warehouse.objects.all()
            wareinfos = []
            for wre in all_ware:
                wareinfos.append(wre['warehouse_id'])
            for ware_val in allware:
                ware_house ={}
                if ware_val.id not in wareinfos:
                    ware_house.update({'warehouse_id': ware_val.id, 'warehouse_name':ware_val.warehouse_name , 'added_quantity':0, 'date': ''})
                    all_ware.append(ware_house)
            spec_value.update({'specification_id':specification_id,'ware_house':all_ware, 'shop_house': all_shop })
            all_info.append(spec_value)
            return JsonResponse({
                'success':True, 
                'message': 'Data has been retrieved successfully',
                'data': all_info
                })
        except:
            return JsonResponse({
                'success':False, 
                'message': 'Something went wrong!! Data could not retrived successfully',
                })





# def warehouse
@api_view(["GET",])
def purchase_reports(request):





    try:

        report = inventory_report.objects.all()

    except:

        report = None 

    print("report")
    print(report)


    #Finding out the individual dates

    if report:


        main_data = []


        specification_ids = list(report.values_list('specification_id',flat=True).distinct())

        print(specification_ids)


    

        for i in range(len(specification_ids)):


            try:
                #Finding out the entries for that specification_id

                reports = inventory_report.objects.filter(specification_id=specification_ids[i])

            except:

                reports = None 


            print(reports)

            if reports:

                #Finding out different purchase prices for that specification

                different_prices = []

                different_purchase_prices = list(reports.values_list('purchase_price',flat=True).distinct())
                
                print("different purchase price")
                print(different_purchase_prices)

                for j in range(len(different_purchase_prices)):

                    try:

                        specific_rows = inventory_report.objects.filter(purchase_price=different_purchase_prices[j],specification_id=specification_ids[i])

                    except:

                        specific_rows = None 
                        
                    print("specificrows",specific_rows)

                    if specific_rows:

                        debit_sum_list = list(specific_rows.values_list('requested', flat=True))
                        credit_sum_list = list(specific_rows.values_list('credit', flat=True))
                        selling_prices = list(specific_rows.values_list('selling_price', flat=True))

                        inventory_ids = list(specific_rows.values_list('id', flat=True))
                        debit_sum = int(sum(debit_sum_list))
                        credit_sum = int(sum(credit_sum_list))
                        if selling_prices[0] == None:
                            selling_prices[0] = 0
                        selling_price  = int(selling_prices[0])
                        purchase_price = different_purchase_prices[j]

                        try:

                            specific_inventory = inventory_report.objects.get(id=inventory_ids[0])

                        except:

                            specific_inventory = None 


                        if specific_inventory:

                            inventory_serializer = InventoryReportSerializer(specific_inventory,many=False)
                            inventory_data = inventory_serializer.data

                            product_name = inventory_data["product_name"]
                            product_brand = inventory_data["product_brand"]
                            product_sku = inventory_data["product_sku"]
                            product_barcode = inventory_data["product_barcode"]
                            product_id = inventory_data["product_id"]
                            specification_id = inventory_data["specification_id"]


                            response_data = {"product_id":product_id,"specification_id":specification_id,"product_name":product_name,"product_sku":product_sku,"product_barcode":product_barcode,"product_brand":product_brand,"purchase_price":purchase_price,"selling_price":selling_price,"debit_sum":debit_sum,"credit_sum":credit_sum}
                            different_prices.append(response_data)


                            

                        else:

                            pass


                    else:
                        pass
                        

            else:

                pass


            main_data.append(different_prices)


        return JsonResponse({"success":True,"message":"The data is shown below","data":main_data})




    else:

        return JsonResponse({"success":False,"message":"The products dont exist"})

def add_delivery_data(value):

    #  'arrayForDelivery': [
    #                 {
    #                     'selectedDistrict': 'Dhaka',
    #                     'selectedThana':[
    #                         'Banani',
    #                         'Gulshan',
    #                         'Rampura',
    #                         'Dhanmondi'
    #                     ]
    #                 },
    #                 {
    #                     'selectedDistrict': 'Barishal',
    #                     'selectedThana':[
    #                         'Hizla',
    #                         'Muladi',
    #                         'Borguna',
    #                         'Betagi'
    #                     ]
    #                 }
    #             ]
    try:
        option_data = value
        option = option_data['option']
        spec_id = option_data['spec']
        arrayForDelivery = option_data['arrayForDelivery']
        delivery_saving_data = {}
        if option == "all":
            delivery_saving_data.update({'specification_id':spec_id })
            info_serializer = ProductDeliveryAreaSerializer (data = delivery_saving_data)
            if info_serializer.is_valid():
                info_serializer.save()
                return "saved"
            else:
                return "error"
        elif option == "manual":
            for del_area in arrayForDelivery:
                district = del_area['selectedDistrict']
                all_thanas= del_area['selectedThana']
                thanas_id=[]
                for thana in all_thanas:
                    try:
                        location_info = DeliveryLocation.objects.get(location_name = thana)
                        location_id = location_info.id
                        thanas_id.append(location_id)
                    except:
                        location_id = -1
                try:
                    area_info = DeliveryArea.objects.get(Area_name = district)
                    area_id = area_info.id
                except:
                    area_id = -1

                delivery_saving_data.update({
                    'specification_id':spec_id,
                    'is_Bangladesh': False,
                    'delivery_area_id': area_id,
                    'delivery_location_ids': thanas_id

                })
                info_serializer = ProductDeliveryAreaSerializer (data = delivery_saving_data)
                if info_serializer.is_valid():
                    info_serializer.save()
        return option_data
    except:
        return "error"
    
    
def add_delivery_data1(value):
     # 'arrayForDelivery': [
                #     {
                #         'selectedDistrict': 'Dhaka',
                #         'selectedThana':[
                #             'Banani',
                #             'Gulshan',
                #             'Rampura',
                #             'Dhanmondi'
                #         ]
                #     },
                #     {
                #         'selectedDistrict': 'Barishal',
                #         'selectedThana':[
                #             'Hizla',
                #             'Muladi',
                #             'Borguna',
                #             'Betagi'
                #         ]
                #     }
                # ]
    try:
        print("dhuktese")
        option_data = value
        option = option_data['option']
        spec_id = option_data['spec']
        try:
            previous_entry = product_delivery_area.objects.filter(specification_id=spec_id)
            
            print(previous_entry)
            
        except:
            previous_entry = None 
        if previous_entry:
            previous_entry.delete()
        else:
            pass
        arrayForDelivery = option_data['arrayForDelivery']
        delivery_saving_data = {}
        if option == "all":
            delivery_saving_data.update({'specification_id':spec_id })
            info_serializer = ProductDeliveryAreaSerializer (data = delivery_saving_data)
            if info_serializer.is_valid():
                info_serializer.save()
                return "saved"
            else:
                return "error"
        elif option == "manual":
            for del_area in arrayForDelivery:
                district = del_area['selectedDistrict']
                all_thanas= del_area['selectedThana']
                thanas_id=[]
                for thana in all_thanas:
                    try:
                        location_info = DeliveryLocation.objects.get(location_name = thana)
                        location_id = location_info.id
                        thanas_id.append(location_id)
                    except:
                        location_id = -1
                try:
                    area_info = DeliveryArea.objects.get(Area_name = district)
                    area_id = area_info.id
                except:
                    area_id = -1

                delivery_saving_data.update({
                    'specification_id':spec_id,
                    'is_Bangladesh': False,
                    'delivery_area_id': area_id,
                    'delivery_location_ids': thanas_id

                })
                info_serializer = ProductDeliveryAreaSerializer (data = delivery_saving_data)
                if info_serializer.is_valid():
                    info_serializer.save()
        return option_data
    except:
        return "error"



@api_view(['POST', ])
def add_spec(request, product_id):
    current_date = date.today()
    # print(request.data)
    # print("user_id")
    # print(request.data.get("uid"))
    # print("lalalalalala")
    product_status = request.data.get("publish")
    if product_status:

        if product_status == "Published":
            product_status = "Published"

        elif product_status == "Pending":
            product_status = "Pending"

    else:
        product_status = "Published"
    manufacture_date = request.data.get("manufacture_date")
    expire_date = request.data.get("expire")
    if manufacture_date == "" or expire_date == "":

        specification_data_value = {
            'product_id': product_id,
            'color': request.data.get("color"),
            'size': request.data.get("size"),
            'weight': request.data.get("weight"),
            'warranty': request.data.get("warranty"),
            'warranty_unit': request.data.get("warranty_unit"),
            'unit': request.data.get("product_unit"),
            'vat': request.data.get("vat"),
            # 'seller_quantity': request.data.get("seller_quantity"),
            # 'remaining': request.data.get("seller_quantity"),
            # 'manufacture_date': request.data.get("manufacture_date"),
            # 'expire': request.data.get("expire"),
            'admin_status': 'Confirmed',
            'is_own' :True,
            'specification_status': product_status
        }

     

    else:


        specification_data_value = {
            'product_id': product_id,
            'color': request.data.get("color"),
            'size': request.data.get("size"),
            'weight': request.data.get("weight"),
            'warranty': request.data.get("warranty"),
            'warranty_unit': request.data.get("warranty_unit"),
            'unit': request.data.get("product_unit"),
            'vat': request.data.get("vat"),
            # 'seller_quantity': request.data.get("seller_quantity"),
            # 'remaining': request.data.get("seller_quantity"),
            'manufacture_date': request.data.get("manufacture_date"),
            'expire': request.data.get("expire"),
            'admin_status': 'Confirmed',
            'is_own' :True,
            'specification_status': product_status
        }

    # product_price = {
    #     'product_id': product_id,
    #     'price': request.data.get("price"),
    #     'purchase_price': request.data.get("purchase_price"),
    #     # 'currency_id': request.data.get('currency_id')
    # }
    discount_type = request.data.get("discount_type")
    discount_amount = request.data.get("discount_amount")
    discount_start_date = request.data.get("discount_start_date")
    discount_end_date = request.data.get("discount_end_date")
    point_amount = request.data.get("point_amount")
    point_start_date = request.data.get("point_start_date")
    point_end_date = request.data.get("point_end_date")
    if discount_type == "none" or discount_amount == '' or discount_start_date == '' or discount_end_date == '':
        discount_flag = False
    else:
        discount_flag = True

    print(discount_flag)
     
    if ((point_amount == "") or (point_start_date == "") or (point_end_date == "")):
        point_flag = False
        # print("False")

    else:
        point_flag = True

    print(point_flag)
    product_discount = {
        'product_id': product_id,
        'amount': request.data.get("discount_amount"),
        'discount_type': request.data.get("discount_type"),
        'start_date': request.data.get("discount_start_date"),
        # 'end_date' : data['discount_end_date']
        'end_date': request.data.get("discount_end_date")
    }

    print(product_discount)
    product_point = {
        'product_id': product_id,
        'point': request.data.get("point_amount"),
        # 'end_date': data['point_end_date']
        'start_date': request.data.get("point_start_date"),
        'end_date': request.data.get("point_end_date")
    }
    delivery_info = {
        'height': request.data.get("delivery_height"),
        'width': request.data.get("delivery_width"),
        'length': request.data.get("delivery_length"),
        'weight': request.data.get("delivery_weight"),
        'measument_unit': request.data.get("delivery_product_unit"),
        'delivery_free': request.data.get("delivery_free"),

    }
    print(delivery_info)
    product_code = {
        'product_id': product_id,
        'manual_SKU' : request.data.get("SKU"),
        'uid': request.data.get("uid"),
    }

    if request.method == 'POST':
        delivery_id = 0
        discount_id = 0
        point_id = 0
        price_id = 0
        specification_id = 0
        flag = 0
        spec = {}
        price = {}
        discount = {}
        point = {}
        delivery = {}
        code={}
        try:
            print("ashtese")
            product_spec = ProductSpecificationSerializerz(
                data=specification_data_value)
            if product_spec.is_valid():
                product_spec.save()
                print("888888888888888888  spec save hoise")
                spec.update(product_spec.data)
                # print("Specification_id", spec["id"])
                specification_id = spec["id"]
            else:
                print(product_spec.errors)
                specification_id = 0
                flag = flag+1


            # product_price.update({'specification_id': spec['id']})
            # product_price = ProductPriceSerializer(data=product_price)
            # if product_price.is_valid():
            #     product_price.save()
            #     # print("price save hochche")
            #     price.update(product_price.data)
            #     price_id = price["id"]
            # else:
            #     price_id = 0
            #     flag = flag+1

            if discount_flag == False:
                discount = {}
            else:
                product_discount.update({'specification_id': spec['id']})
                print("product_discount")
                print(product_discount)
                product_dis = ProductDiscountSerializer(data=product_discount)
                if product_dis.is_valid():
                    product_dis.save()
                    print(product_dis.errors)
                    # print("savwe hochche")
                    discount.update(product_dis.data)
                    discount_id = discount["id"]
                else:
                    print(product_dis.errors)
                    discount_id = 0
                    flag = flag+1
            if point_flag == False:
                point = {}
            else:
                # print("99999999999999999999999999999")
                product_point.update({'specification_id': spec['id']})
                product_point_value = ProductPointSerializer(
                    data=product_point)
                if product_point_value.is_valid():
                    product_point_value.save()
                    print("point save")
                    point.update(product_point_value.data)
                    point_id = point["id"]
                else:
                    point_id = 0
                    print(product_point_value.errors)
                    flag = flag+1
            delivery_info.update({'specification_id': spec['id']})
            # print("here delivery",delivery_info )
            delivery_value = DeliveryInfoSerializer(data=delivery_info)
            # print("serializer",delivery_value)
            if delivery_value.is_valid():
                # print("Inside the delivery ")
                delivery_value.save()
                # print("delivery is saved")
                delivery.update(delivery_value.data)
                delivery_id = delivery["id"]
            else:
                delivery_id = 0
                print("errors delivery " ,delivery_value.errors)
                flag = flag+1
            product_code.update({'specification_id':spec['id']})
            # print("product point",product_code )
            product_code_value= ProductCodeSerializer (data=product_code)
            # print("product code serial", product_code_value)
            # print("before validation")
            if product_code_value.is_valid():
                # print("inside validation")
                product_code_value.save()
                print("code is saved", product_code_value.data)
                code.update(product_code_value.data)
                create_product_code(product_code)
                code_id = code["id"]
                # print("code id", code_id)
            else:
                # print("code error", product_code_value.errors)
                flag= flag+1

            
            data_val = {
                'option' : request.data.get("option"),
                'spec': spec['id'],
                # 'arrayForDelivery': [
                #     {
                #         'selectedDistrict': 'Dhaka',
                #         'selectedThana':[
                #             'Banani',
                #             'Gulshan',
                #             'Rampura',
                #             'Dhanmondi'
                #         ]
                #     },
                #     {
                #         'selectedDistrict': 'Barishal',
                #         'selectedThana':[
                #             'Hizla',
                #             'Muladi',
                #             'Borguna',
                #             'Betagi'
                #         ]
                #     }
                # ]
                'arrayForDelivery': request.data.get("arrayForDelivery")
                    
            }

            # print("before calling method")
            value = add_delivery_data(data_val)
            
            if flag > 0 or value == 'error' :
                try:
                    spe = ProductSpecification.objects.get(id=specification_id)
                except:
                    spe = None
                if spe:
                    spe.delete()
                # try:
                #     pri = ProductPrice.objects.get(id=price_id)
                # except:
                #     pri = None
                # if pri:
                #     pri.delete()
                try:
                    poi = ProductPoint.objects.get(id=point_id)
                except:
                    poi = None
                if poi:
                    poi.delete()
                try:
                    dis = discount_product.objects.get(id=discount_id)
                except:
                    dis = None
                if dis:
                    dis.delete()
                try:
                    deli = DeliveryInfo.objects.get(id=delivery_id)
                except:
                    deli = None
                if deli:
                    deli.delete()
                try:
                    deli = ProductCode.objects.get(id=code_id)
                except:
                    deli = None
                if deli:
                    deli.delete()
                return JsonResponse({
                    "success": False,
                    "message": "Something went wrong !!"
                })

            else:
                return JsonResponse({
                    "success": True,
                    "message": "Specification data has been inserted Successfully",
                    "specification": spec,
                    "price": price,
                    "discount": discount,
                    "point": point,
                    "delivery": delivery
                })
        except:
            try:
                spe = ProductSpecification.objects.get(id=specification_id)
            except:
                spe = None
            if spe:
                spe.delete()
            # try:
            #     pri = ProductPrice.objects.get(id=price_id)
            # except:
            #     pri = None
            # if pri:
            #     pri.delete()
            try:
                poi = ProductPoint.objects.get(id=point_id)
            except:
                poi = None
            if poi:
                poi.delete()
            try:
                dis = discount_product.objects.get(id=discount_id)
            except:
                dis = None
            if dis:
                dis.delete()
            try:
                deli = DeliveryInfo.objects.get(id=delivery_id)
            except:
                deli = None
            if deli:
                deli.delete()
            try:
                deli = ProductCode.objects.get(id=code_id)
            except:
                deli = None
            if deli:
                deli.delete()
            return JsonResponse({
                "success": False,
                "message": "Something went wrong !!"
            })

@api_view(['POST', ])
def merchant_spec(request, product_id):
    current_date = date.today()

    specification_data_value = {
        'product_id': product_id,
        'color': request.data.get("color"),
        'size': request.data.get("size"),
        'weight': request.data.get("weight"),
        'warranty': request.data.get("warranty"),
        'warranty_unit': request.data.get("warranty_unit"),
        'unit': request.data.get("product_unit"),
        'vat': request.data.get("vat"),
        'manufacture_date': request.data.get("manufacture_date"),
        'expire': request.data.get("expire")
    }

    delivery_info = {
        'height': request.data.get("delivery_height"),
        'width': request.data.get("delivery_width"),
        'length': request.data.get("delivery_length"),
        'weight': request.data.get("delivery_weight"),
        'measument_unit': request.data.get("delivery_product_unit"),
    }
    product_code = {
        'product_id': product_id,
        'manual_SKU' : request.data.get("SKU"),
        'uid': request.data.get("uid"),
    }

    if request.method == 'POST':
        delivery_id = 0
        discount_id = 0
        point_id = 0
        price_id = 0
        specification_id = 0
        flag = 0
        spec = {}
        delivery = {}
        code={}
        try:
            product_spec = ProductSpecificationSerializerz(
                data=specification_data_value)
            if product_spec.is_valid():
                product_spec.save()
                spec.update(product_spec.data)
                specification_id = spec["id"]
            else:
                specification_id = 0
                flag = flag+1
        
            delivery_info.update({'specification_id': spec['id']})
            delivery_value = DeliveryInfoSerializer(data=delivery_info)
            if delivery_value.is_valid():
                delivery_value.save()
                delivery.update(delivery_value.data)
                delivery_id = delivery["id"]
            else:
                delivery_id = 0
                flag = flag+1
            product_code.update({'specification_id':spec['id']})
            product_code_value= ProductCodeSerializer (data=product_code)
            if product_code_value.is_valid():
                product_code_value.save()
                code.update(product_code_value.data)
                create_product_code(product_code)
                code_id = code["id"]
            else:
                flag= flag+1
            
            if flag > 0:
                try:
                    spe = ProductSpecification.objects.get(id=specification_id)
                except:
                    spe = None
                if spe:
                    spe.delete()
               
                try:
                    deli = DeliveryInfo.objects.get(id=delivery_id)
                except:
                    deli = None
                if deli:
                    deli.delete()
                try:
                    deli = ProductCode.objects.get(id=code_id)
                except:
                    deli = None
                if deli:
                    deli.delete()
                return JsonResponse({
                    "success": False,
                    "message": "Something went wrong !!"
                })

            else:
                return JsonResponse({
                    "success": True,
                    "message": "Specification data has been inserted Successfully",
                    "specification": spec,
                    "delivery": delivery
                })
        except:
            try:
                spe = ProductSpecification.objects.get(id=specification_id)
            except:
                spe = None
            if spe:
                spe.delete()
            try:
                deli = DeliveryInfo.objects.get(id=delivery_id)
            except:
                deli = None
            if deli:
                deli.delete()
            try:
                deli = ProductCode.objects.get(id=code_id)
            except:
                deli = None
            if deli:
                deli.delete()
            return JsonResponse({
                "success": False,
                "message": "Something went wrong !!"
            })

@api_view(['POST', ])
def merchant_spec_edit(request, specification_id):
 
    specification_data_value = {
        'color': request.data.get("color"),
        'size': request.data.get("size"),
        'weight': request.data.get("weight"),
        'warranty': request.data.get("warranty"),
        'warranty_unit': request.data.get("warranty_unit"),
        'unit': request.data.get("product_unit"),
        'vat': request.data.get("vat"),
        'manufacture_date': request.data.get("manufacture_date"),
        'expire': request.data.get("expire")
    }

    delivery_info = {
        'height': request.data.get("delivery_height"),
        'width': request.data.get("delivery_width"),
        'length': request.data.get("delivery_length"),
        'weight': request.data.get("delivery_weight"),
        'measument_unit': request.data.get("delivery_product_unit"),
    }
    if request.method == 'POST':
        delivery_id = 0
        flag = 0
        spec = {}
        delivery = {}
        try:
            try:
                merchant_spec = ProductSpecification.objects.get(pk=specification_id, admin_status = 'Processing')
                merchant_delivery = DeliveryInfo.objects.get(specification_id = specification_id)
            except:
                merchant_spec = None
                merchant_delivery = None

            if merchant_spec and merchant_delivery:
                product_spec = ProductSpecificationSerializerz(merchant_spec,data=specification_data_value)
                if product_spec.is_valid():
                    product_spec.save()
                    spec.update(product_spec.data)
                else:
                    flag = flag+1
        
                delivery_value = DeliveryInfoSerializer(merchant_delivery,data=delivery_info)
                if delivery_value.is_valid():
                    delivery_value.save()
                    delivery.update(delivery_value.data)
                else:
                    delivery_id = 0
                    flag = flag+1
            
                if flag > 0:
                    try:
                        spe = ProductSpecification.objects.get(id=specification_id)
                    except:
                        spe = None
                    if spe:
                        spe.delete()
                
                    try:
                        deli = DeliveryInfo.objects.get(id=delivery_id)
                    except:
                        deli = None
                    if deli:
                        deli.delete()
                    return JsonResponse({
                        "success": False,
                        "message": "Something went wrong !!"
                    })

                else:
                    return JsonResponse({
                        "success": True,
                        "message": "Specification data has been updated Successfully !!",
                        "specification": spec,
                        "delivery": delivery
                  })
            else:
                return JsonResponse({
                    "success": False,
                    "message": "Update is restriced after specification being approved/cancelled by main site !!"
                })
        except:
            try:
                spe = ProductSpecification.objects.get(id=specification_id)
            except:
                spe = None
            if spe:
                spe.delete()
            try:
                deli = DeliveryInfo.objects.get(id=delivery_id)
            except:
                deli = None
            if deli:
                deli.delete()
            return JsonResponse({
                "success": False,
                "message": "Something went wrong !!"
            })




@api_view(['GET', ])
def merchant_products(request,seller_id):

    specification_ids = []

    try:

        product = Product.objects.filter(seller=seller_id)

    except:

        product= None 

    if product:

        product_ids = list(product.values_list('id',flat=True))

        try:

            product_specs = ProductSpecification.objects.filter(product_id__in=product_ids)

        except:

            product_specs = None 

        if product_specs:

            product_specs_serializer = SellerSpecificationSerializer(product_specs,many=True)

            return JsonResponse({"success":True,"message":"Products are displayed","data":product_specs_serializer.data})

        else:

            return({"success":False,"message":"There are no products to display"})



    else:
        return({"success":False,"message":"There are no products to display"})


@api_view(["GET",])
def cancel_invoice(request,invoice_id):

    try:

        invoice = Invoice.objects.get(id=invoice_id)

    except:

        invoice = None 

    if invoice:

        if invoice.order_id:

            try:
                order = Order.objects.get(id=invoice.order_id)
            except:
                order = None 

            if order:
                order.admin_status = "Cancelled"
                order.save()
                return JsonResponse({"success":True,"message":"This invoice has been cancelled"})
            else:
                return JsonResponse({"success":False,"message":"This order does not exist"})

        else:
            return JsonResponse({"success":False,"message":"This order does not exist"})

    else:
        return JsonResponse({"success":False,"message":"This invoice does not exist"})




@api_view(["GET", "POST"])
def seller_insert_product_quantity(request):

    # demo values
    # api_values = [{
    #     'product_id':35,
    #     'order_id': 111,
    #     'product_status': "Approved",
    #     'specification_id':87,
    #     'order_details_id': 243,
    #     'purchase_price': 100,
    #     'selling_price': 120,
    #     'warehouse': [
    #         {
    #             'warehouse_id': 1,
    #             'quantity': 200

    #         },
    #         {
    #             'warehouse_id': 2,
    #             'quantity': 200

    #         }
    #     ],

    #      'shop': [
    #         {
    #             'shop_id': 3,
    #             'quantity': 200

    #         },
    #         {
    #             'shop_id': 2,
    #             'quantity': 200

    #         },
    #         {
    #             'shop_id': 1,
    #             'quantity': 200

    #         }


    #     ]

    #     },
    #     {
    #     'product_id':35,
    #     'order_id': 111,
    #     'product_status': "Cancelled",
    #     'specification_id':28,
    #     'order_details_id': 242,
    #     'purchase_price': 100,
    #     'selling_price': 120,
    #     'warehouse': [
    #         {
    #             'warehouse_id': 1,
    #             'quantity': 200

    #         },
    #         {
    #             'warehouse_id': 2,
    #             'quantity': 200

    #         }
    #     ],

    #      'shop': [
    #         {
    #             'shop_id': 3,
    #             'quantity': 200

    #         },
    #         {
    #             'shop_id': 2,
    #             'quantity': 200

    #         },
    #         {
    #             'shop_id': 1,
    #             'quantity': 200

    #         }


    #     ]

    #     },
    #     {
    #     'product_id':35,
    #     'order_id': 111,
    #     'product_status': "Cancelled",
    #     'specification_id':45,
    #     'order_details_id': 244,


    #     }]

    api_values = request.data
    current_date = date.today()
    quantity_flag = 0 
    order_id = api_values[0]["order_id"]
    print(order_id)

    if request.method == 'POST':

        data_length = int(len(api_values))

        main_flag = False

        try:

            for i in range(data_length):

                print(i)
                print(api_values[i]["product_status"])

                if api_values[i]["product_status"] == "Approved":

                    print("approve hoise")

                    api_valuess = api_values[i]

                    mflag = False

                    pflag = admin_approve_add_merchant_specification(api_valuess)
                    print("pflag")

                    print(pflag)
                    #pflag = True

                    if pflag == True:


                        #Insert the purchase price and selling price for that object:

                        try:

                            print(api_valuess["product_id"])
                            print(api_valuess["specification_id"])
                            print(int(api_valuess["unit_price"]))
                            #print(int(api_valuess["purchase_price"]))

                            price_data = {"product_id":api_valuess["product_id"],"specification_id":api_valuess["specification_id"],"price":int(api_valuess["selling_price"]),"purchase_price":int(api_valuess["unit_price"])}
                            print(price_data)

                            #Inserting the price

                            product_price_serializer = ProductPriceSerializer(data = price_data)
                            if product_price_serializer.is_valid():
                                product_price_serializer.save()
                                print(i)
                                print("price saved")
                            else:
                                print(product_price_serializer.errors)


                        except:

                            return JsonResponse({"success":False,"message":"The price could not be inserted"})



                        try:
                            #Fetching the product price 

                            prod_price = ProductPrice.objects.filter(specification_id=int(api_valuess["specification_id"])).last()

                        except:

                            prod_price = None 

                        if prod_price:

                            print(i)

                            print("price ase")


                            purchase_price = prod_price.purchase_price
                            selling_price = prod_price.price

                        else:

                            return JsonResponse({"success":False,"message":"Price does not exist for this product"})


                        try:

                            # checking is there any warehouse data exists or not
                            if len(api_valuess['warehouse']) > 0:
                                for wareh in api_valuess['warehouse']:
                                    try:
                                        # getting the previous data if there is any in the similar name. If exists update the new value. if does not create new records.
                                        wareh_query = WarehouseInfo.objects.filter(
                                            warehouse_id=int(wareh['warehouse_id']), specification_id=int(api_valuess['specification_id'])).last()

                                        print("quertresult")
                                        print(wareh_query)

                                        if wareh_query:
                                            # quantity_val = wareh_query[0].quantity
                                            # new_quantity = quantity_val + wareh['quantity']
                                            # wareh_query.update(quantity=new_quantity)
                                            # wareh_query.save()
                                            print("existing warehouse")
                                            print(type(wareh['quantity']))
                                            print(wareh_query.quantity)

                                            warehouse_quantity =  wareh_query.quantity

                                            print(warehouse_quantity)

                                            new_quantity =  warehouse_quantity + int(wareh['quantity'])

                                            print(new_quantity)

                                            wareh_query.quantity = new_quantity
                                            print(wareh_query.quantity)
                                            wareh_query.save()
                                            print(wareh_query.quantity)

                                            try:
                                                product_spec = ProductSpecification.objects.get(id=int(api_valuess['specification_id']))

                                            except:
                                                product_spec = None 

                                            if product_spec:

                                                product_spec.save()




                                        else:
                                            print("else ey dhuktese")
                                            wareh_data = WarehouseInfo.objects.create(specification_id=int(api_valuess['specification_id']), product_id=int(api_valuess['product_id']), warehouse_id=int(wareh['warehouse_id']),
                                                                       quantity=int(wareh['quantity']))
                                            wareh_data.save()

                                            try:
                                                product_spec = ProductSpecification.objects.get(id=int(api_valuess['specification_id']))

                                            except:
                                                product_spec = None 

                                            if product_spec:

                                                product_spec.save()

                                        # updating the inventory report credit records for each ware house quantity. It will help to keep the records in future.
                                        # report_data = inventory_report(
                                        #     product_id=api_values['product_id'], credit=wareh['quantity'], warehouse_id=wareh['warehouse_id'])
                                        # report_data.save()
                                        #Check to see if there are any inventory_reports
                                        # try:

                                        #     report = inventory_report.objects.filter(product_id=api_values['product_id'],specification_id=api_values['specification_id'],warehouse_id=wareh['warehouse_id'],date=current_date).last()

                                        # except:

                                        #     report = None 


                                        # if report:

                                        #     #Update the existing report

                                        #     report.credit += int(wareh['quantity'])
                                        #     report.save()




                                        new_report = inventory_report.objects.create(product_id=int(api_valuess['product_id']),specification_id=int(api_valuess['specification_id']),warehouse_id=int(wareh['warehouse_id']),credit=int(wareh['quantity']),date=current_date,purchase_price=purchase_price,selling_price=selling_price)
                                        new_report.save()



                                    except:
                                        pass

                            if len(api_valuess['shop']) > 0:
                                for shops in api_valuess['shop']:
                                    try:
                                        # getting the existing shop values if is there any.
                                        print(shops['shop_id'])
                                        shop_query = ShopInfo.objects.filter(
                                            int(shop_id=shops['shop_id']), specification_id=int(api_valuess['specification_id'])).last()
                                        print(shop_query)
                                        if shop_query:
                                            print("shop ase")
                                            quantity_val = shop_query.quantity
                                            new_quantity = quantity_val + int(shops['quantity'])
                                            # shop_query.update(quantity=new_quantity)
                                            shop_query.quantity = new_quantity
                                            shop_query.save()

                                            try:
                                                product_spec = ProductSpecification.objects.get(id=int(api_values['specification_id']))

                                            except:
                                                product_spec = None 

                                            if product_spec:

                                                product_spec.save()
                                        else:
                                            print("shop nai")
                                            shop_data = ShopInfo.objects.create(specification_id=int(api_valuess['specification_id']), product_id=int(api_valuess['product_id']), shop_id=int(shops['shop_id']),
                                                                 quantity=int(shops['quantity']))
                                            shop_data.save()
                                        # Updating the report table after being inserted the quantity corresponding to credit coloumn for each shop.
                                        # report_data = inventory_report(
                                        #     product_id=api_values['product_id'], credit=shops['quantity'], shop_id=shops['shop_id'])
                                        # report_data.save()

                                            try:
                                                product_spec = ProductSpecification.objects.get(id=int(api_valuess['specification_id']))

                                            except:
                                                product_spec = None 

                                            if product_spec:

                                                product_spec.save()
                                            







                                        new_report = inventory_report.objects.create(product_id=int(api_valuess['product_id']),specification_id=int(api_valuess['specification_id']),shop_id=int(shops['shop_id']),credit=int(shops['quantity']),date=current_date,purchase_price=purchase_price,selling_price=selling_price)
                                        new_report.save()

                                    except:
                                        pass




                            mflag = True

                            # return Response({
                            #     "success": True,
                            #     "message": "Data has been added successfully"
                            # })
                        except:
                            # return Response({
                            #     "success": False,
                            #     "message": "Something went wrong !!"
                            # })

                            mflag = False

                        print(i)

                        print(mflag)


                        if mflag == True:

                            try:
                                order_details = OrderDetails.objects.get(id=int(api_valuess["order_details_id"]))

                            except:

                                order_details = None 

                            if order_details:

                                order_details.admin_status = "Approved"
                                order_details.save()
                                print(i)
                                print(order_details)

                            
                            else:
                                return Response({
                                "success": False,
                                "message": "Something went wrong.Order could not be approved!!"
                            })


                            try:
                                product_specification = ProductSpecification.objects.get(id=int(api_valuess["specification_id"]))

                            except:
                                product_specification = None 

                            if product_specification:
                                product_specification.admin_status = "Confirmed"
                                product_specification.save()
                                quantity_flag = quantity_flag + 1 
                                print(i)
                                print(product_specification)
                                print(quantity_flag)

                            else:
                                return Response({
                                "success": False,
                                "message": "Something went wrong.Specification of this product could not be approved!!"
                            })


                            #return JsonResponse({"success":True,"message":"All the quantities have been added with their prices and the order item has been approved and the specification has been approved"})
                            main_flag = True
                            print(i)
                            print("main flag true")

                        else:

                            main_flag = False



                            # return Response({
                            #     "success": False,
                            #     "message": "Something went wrong !!"
                            # })


                    else:

                        main_flag = False


                        if main_flag == False:
                            return JsonResponse({"success":False,"message":"The product point,discount or delivery info could not be added"})

                elif api_values[i]["product_status"] == "Cancelled":


                    print("wbefuefbewqufgbewqufbeqwufvbweufwebfuwegbfuwefbweufb")

                    print(i)
                    print("product status cancelled")

                    #Fetch the ordel details item and change its status

                    order_dets_id = int(api_values[i]["order_details_id"])
                    print("order_dets_id")
                    print(order_dets_id)

                    try:

                        order_dets = OrderDetails.objects.get(id=order_dets_id)

                    except:

                        order_dets = None

                    print(i)

                    print("order_dets") 

                    print(order_dets)

                    if order_dets:

                        order_dets.product_status = "Cancelled"
                        order_dets.admin_status = "Cancelled"
                        order_dets.save()
                        main_flag = True

                    else:

                        main_flag = False


                    print(main_flag)


                    if main_flag == False:

                        return JsonResponse({"success":False,"message":"Something went wrong while cancelling an order"})





                else:

                    main_flag = False



            if main_flag == True:

                print("quantity_flag")
                print("main_flag tryue hoise")
                print(order_id)
                print(quantity_flag)

                if quantity_flag > 0:

                    #Approve the order

                    try:
                        order = Order.objects.get(id=order_id)

                    except:

                        order = None 

                    if order:

                        order.admin_status = "Confirmed"
                        order.save()
                        return JsonResponse({"success":True,"message":"All the data has been inserted and the order has been approved"})

                    else:

                        return JsonResponse({"success":False,"message":"The order could not be approved"})

                else:


                    try:
                        order = Order.objects.get(id=order_id)

                    except:

                        order = None 

                    if order:

                        order.admin_status = "Cancelled"
                        order.save()
                        return JsonResponse({"success":False,"message":"None of the products were approved and the invoice is cancelled"})

                    else:

                        return JsonResponse({"success":False,"message":"The order could not be approved"})

                    

                    #approve the order

                    # try:
                    #     order = Order.objects.g

        except:


            return JsonResponse({"success":False,"message":"Something went wrong in the main method"})











def admin_approve_add_merchant_specification(value):
    current_date = current
    discount_type = value["discount_type"]
    discount_amount = value["discount_amount"]
    discount_start_date = value["discount_start_date"]
    discount_end_date = value["discount_end_date"]
    point_amount = value["point_amount"]
    point_start_date = value["point_start_date"]
    point_end_date = value["point_end_date"]
    specification_id = value['specification_id']
    product_id = value['product_id']
    if discount_type == "none" or discount_amount == '' or discount_start_date == '' or discount_end_date == '':
        discount_flag = False
    else:
        discount_flag = True
    if ((point_amount == "") or (point_start_date == "") or (point_end_date == "")):
        point_flag = False
        # print("False")
    else:
        point_flag = True
    product_discount = {
        'product_id': product_id,
        'amount': discount_amount,
        'discount_type': discount_type,
        'start_date': value["discount_start_date"],
        'end_date': value["discount_end_date"],
        'specification_id': specification_id
    }
    product_point = {
        'product_id': product_id,
        'point': value["point_amount"],
        'start_date': value["point_start_date"],
        'end_date': value["point_end_date"],
        'specification_id': specification_id
    }
    delivery_id = 0
    discount_id = 0
    point_id = 0
    price_id = 0
    flag = 0
    spec = {}
    price = {}
    discount = {}
    point = {}
    delivery = {}
    code={}
    try:   
        if discount_flag == False:
            discount = {}
        else:
            product_dis = ProductDiscountSerializer(data=product_discount)
            if product_dis.is_valid():
                product_dis.save()
                discount.update(product_dis.data)
                discount_id = discount["id"]
            else:
                discount_id = 0
                flag = flag+1
        if point_flag == False:
            point = {}
        else:
            product_point_value = ProductPointSerializer(data=product_point)
            if product_point_value.is_valid():
                product_point_value.save()
                point.update(product_point_value.data)
                point_id = point["id"]
            else:
                point_id = 0
                flag = flag+1
        data_val = {
            'option' : value["option"],
            'spec': specification_id,
            'arrayForDelivery': value["arrayForDelivery"]
            # 'arrayForDelivery': [
            #     {
            #         'selectedDistrict': 'Dhaka',
            #         'selectedThana':[
            #             'Banani',
            #             'Gulshan',
            #             'Rampura',
            #             'Dhanmondi'
            #         ]
            #     },
            #     {
            #         'selectedDistrict': 'Khulna',
            #         'selectedThana':[
            #             'Hizla',
            #             'Muladi',
            #             'Borguna',
            #             'Betagi'
            #         ]
            #     }
            # ]
        }
        value = add_delivery_data(data_val)
        if flag > 0:
            try:
                poi = ProductPoint.objects.get(id=point_id)
            except:
                poi = None
            if poi:
                poi.delete()
            try:
                dis = discount_product.objects.get(id=discount_id)
            except:
                dis = None
            if dis:
                dis.delete()
            return False
        else:
            return True
    except:
        try:
            poi = ProductPoint.objects.get(id=point_id)
        except:
            poi = None
        if poi:
            poi.delete()
        try:
            dis = discount_product.objects.get(id=discount_id)
        except:
            dis = None
        if dis:
            dis.delete()
        return False



@api_view(["GET",])
def individual_seller_spec(request,specification_id):

    try:

        product_spec = ProductSpecification.objects.get(id=specification_id)


    except:

        product_spec = None


    if product_spec:

        prod_serializer = SellerSpecificationSerializer(product_spec,many=False)
        p_data = prod_serializer.data


    else:

        p_data = {}


    return JsonResponse({"success":True,"message":"The info is shown","data":p_data})



@api_view(["GET",])
def get_delivery_info(request,specification_id):
    
    main_data = []
    
    try:
        delivery_places = product_delivery_area.objects.filter(specification_id = specification_id)
        
    except:
        delivery_places = None
        
    print(delivery_places) 
        
    if delivery_places:
        
        area_ids = list(delivery_places.values_list('delivery_area_id',flat=True))
        
        if -1 in area_ids:
            area_ids.remove(-1)
            
        print(area_ids)
            
            
        if len(area_ids) < 1:
            main_data = []
            
        # print(area_ids)
            
        else:
            for i in range(len(area_ids)):
                try:
                    product_areas = product_delivery_area.objects.get(specification_id = specification_id,delivery_area_id=area_ids[i])
                    
                except:
                    product_areas = None 
                    
                print(product_areas)
                    
                if product_areas:
                        
                    location_ids = product_areas.delivery_location_ids
                    
                else:
                    location_ids = []
                    
                try:
                    area_name = DeliveryArea.objects.get(id=area_ids[i])
                except:
                    area_name = None 
                    
                if area_name:
                    
                    selected_district = area_name.Area_name
                    
                else:
                    selected_district = ""
                    
                selected_thanas = []
                print("location_ids")
                print(location_ids)
                for j in range(len(location_ids)):
                    try:
                        deli_loc = DeliveryLocation.objects.get(id = int(location_ids[j]))
                        
                    except:
                        deli_loc = None
                        
                    print(deli_loc)
                    print("deli_loc") 
                        
                    if deli_loc:
                        loc_name = deli_loc.location_name
                    else:
                        loc_name = ""
                        
                    selected_thanas.append(loc_name)
                    
                    
                all_thanas = []
                
                try:
                    all_locs = DeliveryLocation.objects.filter(area_id = area_ids[i])
                    
                except:
                    all_locs = None 
                    
                if all_locs:
                    all_locs_ids = list(all_locs.values_list('id',flat=True))
                    all_locs_names = list(all_locs.values_list('location_name',flat=True))
                else:
                    all_locs_ids = []
                    all_locs_names =[]
                    
                for k in range(len(all_locs_names)):
                    loc_dic = {"location_name":all_locs_names[k]}
                    all_thanas.append(loc_dic)
                    
                main_dic = {"selectedDistrict":selected_district,"selectedThana":selected_thanas,"thanas":all_thanas}
                main_data.append(main_dic)
                
            
    else:
        main_data = []
        
        
    return JsonResponse({"data": main_data})
        
@api_view(["POST",])
def verify_pos(request):

    term_data = {}

    API_key = request.data.get("API_key")

    try:

        term = Terminal.objects.all()

    except:
        term = None 

    if term: 

        term_ids =  list(term.values_list('id',flat=True))

        for i in range(len(term_ids)):

            try:
                specific_term = Terminal.objects.get(id=term_ids[i])
            except:
                specific_term = None 
            if specific_term:
                if specific_term.API_key == API_key:
                    term_serializer = TerminalSerializer(specific_term,many=False)  
                    term_data = term_serializer.data                  
                    break
                else:
                    pass
            else:
                pass

    else:
        pass


    if term_data == {}:
        return JsonResponse({"success":False,"message":"The API key provided does not exist","data":term_data})

    else:
        return JsonResponse({"success":True,"message":"Installation successful","data":term_data})


@api_view(["GET",])
def warehouse_shop_info(request):

    warehouses = []
    shops = []

    try:
        warehouse = Warehouse.objects.all()
    except:
        warehouse = None 

    try:
        shop = Shop.objects.all()
    except:
        shop = None 

    if warehouse:
        warehouse_serializer = WSerializer(warehouse,many=True)
        warehouse_data = warehouse_serializer.data
    if shop:
        shop_serializer = SSerializer(shop,many=True)
        shop_data = shop_serializer.data

    return JsonResponse({"success":True,"message":"The data is shown below","warehouses":warehouse_data,"shops":shop_data})


@api_view(["POST",])
def create_terminal(request):

    # warehouses = []
    # shops = []
    terminal_name = request.data.get("terminal_name")
    warehouse_id = request.data.get("warehouse_id")
    shop_id = request.data.get("shop_id")
    admin_id = request.data.get("admin_id")

    if warehouse_id == "":

        if shop_id:
            s_id = shop_id
            w_id = -1

    elif shop_id == "":

        if warehouse_id:
            w_id = warehouse_id
            s_id = -1 

    
    main_data = {"terminal_name":terminal_name,"warehouse_id":w_id,"shop_id":s_id,"admin_id":admin_id}
    terminal = Terminal.objects.create(terminal_name = terminal_name,warehouse_id = w_id,shop_id = s_id, admin_id = admin_id)
    terminal.save()
    term_id = terminal.id
    print("terminalid")
    print(term_id)
    try:
        terminal = Terminal.objects.get(id=term_id)
    except:
        terminal = None 

    if terminal:
        terminal_serializer = TerminalSerializer(terminal,many=False)
        term_data = terminal_serializer.data
        return JsonResponse({"success":True,"message":"Terminal is created","data":term_data})
    else:
        return JsonResponse({"success":False,"message":"Terminal is not created"})


    # term_serializer = TerminalSerializer(data=main_data)
    # if term_serializer.is_valid():
    #     term_serializer.save()
    #     term_id = term_serializer.data["id"]
    #     try:
    #         terminal = Terminal.objects.get(id=int(term_id))
    #     except:
    #         terminal = None
    #     if terminal:
    #         terminal.save()
        
        
    # else:
    #     return JsonResponse({"success":False,"message":"Terminal is not created"})



@api_view(["GET",])
def terminal_list(request):

    try:
        terminals = Terminal.objects.all()
    except:
        terminals = None 

    if terminals:

        term_serializer = TerminalSerializer(terminals,many=True)
        term_data = term_serializer.data
        return JsonResponse({"success":True,"message":"Data is shown","data":term_data})
    
    else:
        return JsonResponse({"success":False,"message":"Data doesnt exist"})
    
        

#This is for the admin panel.Admin will use this to create a user
@api_view (["POST",])
def create_pos_user(request,terminal_id):

    email = request.data.get('email')
    password = request.data.get('password')
    role =  request.data.get('role')
    pwd = make_password(password)
    username = request.data.get('username')
    phone_number = request.data.get('phone_number')
    if username is None:
        username = ""
    if phone_number is None:
        phone_number = ""
    



    #Create an user 
    

    new_user = User.objects.create(email=email,password=pwd,pwd=password,role=role,is_staff=False,is_verified=True,is_active=True,username=username,phone_number=phone_number)
    new_user.save()
    user_id = new_user.id
    email = new_user.email
    print(new_user)
    data = {'email':email,'password':pwd,'pwd':password,'role':role,'is_staff':False,'is_verified':True,'is_active':True,'username':username,'phone_number':phone_number}
    new_serializer = UserSerializerz(new_user,data=data)

    if new_serializer.is_valid():
        new_serializer.save()
    
        # balance_values = {'user_id':user_id}
        # create_user_balance(balance_values)
        profile_values ={'user_id':user_id,'email':email}
        create_user_profile(profile_values)
        data = new_serializer.data
        #Insertion in the TerminalUsers table
        terminal_user = TerminalUsers.objects.create(terminal_id=terminal_id,user_id=user_id,is_active=True) 
        terminal_user.save()

    # try:
    #     current_user = User.objects.get(id=user_id)
    # except:
    #     current_user = None

    # if current_user:
    #     new_serializer = UserSerializerz(new_user,many=False)
    #     data = new_serializer.data
    # else:
    #     data = {}

        return Response(
        {
        'success': True,
        'message': 'User has been created',
        'data' : data,
        # 'encrypted_password': data["password"],
        'password': password
        
        })

    else:
        print(new_serializer.errors)
        return Response(
        {
        'success': False,
        'message': 'Could not create user',
        
        
        })


def make_terminal_active_inactive(request,terminal_id):

    try:
        terminal = Terminal.objects.get(id=terminal_id)
    except:
        terminal = None

    print(terminal) 

    if terminal:
        if terminal.is_active == True:
            print("is true")
            terminal.is_active = False
            terminal.save()
            return JsonResponse({"success":True,"message":"The active status has been changed","is_active":False})
        elif terminal.is_active == False:
            terminal.is_active = True 
            terminal.save()
            return JsonResponse({"success":True,"message":"The active status has been changed","is_active":True})

    else:
        return JsonResponse({"success":False,"message":"The terminal does not exist"})





def make_user_active_inactive(request,user_id,terminal_id):
    
    try:
        terminal = TerminalUsers.objects.get(terminal_id=terminal_id,user_id=user_id)
    except:
        terminal = None

    print(terminal) 

    if terminal:
        if terminal.is_active == True:
            print("is true")
            terminal.is_active = False
            terminal.save()
            return JsonResponse({"success":True,"message":"The active status has been changed","is_active":False})
        elif terminal.is_active == False:
            terminal.is_active = True 
            terminal.save()
            return JsonResponse({"success":True,"message":"The active status has been changed","is_active":True})

    else:
        return JsonResponse({"success":False,"message":"The user does not exist"})



@api_view (["POST",])        
def insert_specification_price(request,specification_id):

    # data = {
    #     "MRP": 25.00,
    #     "data_array" : [{
    #         "status": "Single",
    #         "quantity": 1,
    #         "purchase_price": 300.0,
    #         "selling_price": 350.0,
    #     },
    #     {
    #         "status": "Minimum",
    #         "quantity": 10,
    #         "purchase_price": 300.0,
    #         "selling_price": 350.0,
    #     },
    #     {
    #         "status": "Maximum",
    #         "quantity": 100,
    #         "purchase_price": 300.0,
    #         "selling_price": 350.0,
    #     }]
    # }
    data = request.data
    print(data)


    try:
        prod_specz = ProductSpecification.objects.get(id=specification_id)
    except:
        prod_specz = None 



    if prod_specz:
        shared_status = prod_specz.shared
        if shared_status == False:
            MRP = data["MRP"]
            data_info = data["data_array"]
            ids = []

            for i in range(len(data_info)):
                spec_price = SpecificationPrice.objects.create(specification_id = specification_id, mrp = MRP, status = data_info[i]["status"],quantity = data_info[i]["quantity"],purchase_price = data_info[i]["purchase_price"],selling_price = data_info[i]["selling_price"] )
                spec_price.save()
                spec_id = spec_price.id
                ids.append(spec_id)


            try:
                specs = SpecificationPrice.objects.filter(id__in=ids,is_active = True)
            except:
                specs = None 

            if specs:
                specs_serializer = MaxMinSerializer(specs,many=True)
                specs_data = specs_serializer.data

                #Change the specification status
                # try:
                #     specific_spec = ProductSpecification.objects.get(id=specification_id)
                # except:
                #     specific_spec = None 

                # if specific_spec:
                #     specific_spec.
                try:
                    prod_spec = ProductSpecification.objects.get(id=specification_id)
                except:
                    prod_spec = None

                
                 

            

                if prod_spec:
                    try:
                        prod = Product.objects.get(id = prod_spec.product_id)
                    except:
                        prod = None 
                    if prod:
                        prod.shared = True
                        prod.save()

                    prod_spec.shared = True
                    prod_spec.save()
                    spec_serializer = MotherSpecificationSerializer(prod_spec,many=False)
                    spec_data = spec_serializer.data
                else:
                    spec_data = {}

                print(spec_data)

                # specc_data = json.loads(spec_data)
                spec_dataz = json.dumps(spec_data)
    
                url = site_path + "productdetails/insert_child_product_info/"
                headers = {'Content-Type': 'application/json',}
                dataz = requests.post(url = url, headers=headers,data = spec_dataz)
                # print(dataz) 
                dataz = dataz.json()
               
                # print(dataz)

                if dataz["success"] == True:
                    return JsonResponse({"success":True,"message":"Data has been inserted","data": specs_data,"product_info":spec_data})
                else:
                    #Delete the max min values
                    prod_spec.shared = False
                    prod_spec.save()

                    try:
                        max_del = SpecificationPrice.objects.filter(id__in = ids)
                    except:
                        max_del = None 

                    if max_del:
                        max_del.delete()
                    return JsonResponse({"success":True,"message":"Data could not be inserted in mothersite","data": specs_data,"product_info":spec_data})


            else:
                return JsonResponse({"success":False,"message":"Data could not be inserted"})

        else:
            return JsonResponse({"success":False,"message":"This product has already been shared before"})


    else:
        return JsonResponse({"success":False,"message":"This product does not exist"})


    
        

@api_view(["GET", ])
def mothersite_approval_response(request,specification_id):

    try:
        specs = ProductSpecification.objects.get(id=specification_id)
    except:
        specs = None 

    

    if specs:
        
        # try:
        #     prod = Product.objects.get(specs.product_id)
        # except:
        #     prod = None 
        # if prod:
        #     prod.product_admin_status = "Cancelled"

        specs.mother_status = "Confirmed"
        specs.save()

        return JsonResponse({"success":True,"message":"Mother Site has approved this product"})

    else:

        return JsonResponse({"success":False,"message":"The product does not exist"})



@api_view(["GET", ])
def mothersite_cancelled_response(request,specification_id):

    try:
        specs = ProductSpecification.objects.get(id=specification_id)
    except:
        specs = None 

    if specs:
        
        # try:
        #     prod = Product.objects.get(specs.product_id)
        # except:
        #     prod = None 
        # if prod:
        #     prod.product_admin_status = "Cancelled"

        specs.mother_status = "Cancelled"
        specs.save()

        return JsonResponse({"success":True,"message":"Mother Site has cancelled this product"})

    else:

        return JsonResponse({"success":False,"message":"The product does not exist"})



@api_view(["GET", ])
def all_shared_motherproducts(request):

    try:
        specs = ProductSpecification.objects.filter(is_own=False)
    except:
        specs = None 

    if specs:
        specs_serializer = MotherSpecificationSerializer(specs,many=True)
        return JsonResponse({"success":True,"message":"Specifications are displayed","data":specs_serializer.data})
    else:
        return JsonResponse({"success": False,"message":"There is no data to show"})


@api_view(["GET", ])
def all_shared_products(request):

    try:
        specs = ProductSpecification.objects.filter(shared = True)
    except:
        specs = None 

    if specs:
        specs_serializer = MotherSpecificationSerializer(specs,many=True)
        return JsonResponse({"success":True,"message":"Specifications are displayed","data":specs_serializer.data})
    else:
        return JsonResponse({"success": False,"message":"There is no data to show"})
    

@api_view(["GET", ])
def approved_shared_products(request):

    try:
        specs = ProductSpecification.objects.filter(shared = True,mother_status="Confirmed")
    except:
        specs = None 

    if specs:
        specs_serializer = MotherSpecificationSerializer(specs,many=True)
        return JsonResponse({"success":True,"message":"Specifications are displayed","data":specs_serializer.data})
    else:
        return JsonResponse({"success": False,"message":"There is no data to show"})


@api_view(["GET", ])
def pending_shared_products(request):

    try:
        specs = ProductSpecification.objects.filter(shared= True,mother_status="Processing")
    except:
        specs = None 

    if specs:
        specs_serializer = MotherSpecificationSerializer(specs,many=True)
        return JsonResponse({"success":True,"message":"Specifications are displayed","data":specs_serializer.data})
    else:
        return JsonResponse({"success": False,"message":"There is no data to show"})


@api_view(["GET", ])
def cancelled_shared_products(request):

    try:
        specs = ProductSpecification.objects.filter(shared= True,mother_status="Cancelled")
    except:
        specs = None 

    if specs:
        specs_serializer = MotherSpecificationSerializer(specs,many=True)
        return JsonResponse({"success":True,"message":"Specifications are displayed","data":specs_serializer.data})
    else:
        return JsonResponse({"success": False,"message":"There is no data to show"})



@api_view(["GET", ])
def all_mothersite_products(request):


    try:
        company= CompanyInfo.objects.all()
    except:
        company = None 

    if company:
        company = company[0]
        site_id = company.site_identification
    else:
        site_id = ""

    print(site_id)
    print(type(site_id))



    url = site_path + "productdetails/all_mothersite_products/" +str(site_id)+ "/"
    mother_response = requests.get(url = url)
    mother_data = mother_response.json()
    if mother_data["success"] == True:
        all_products = mother_data["data"]
        return JsonResponse({"success":True,"message":"Mother Site products are shown","data":all_products})
    else:
        return JsonResponse({"success":False,"message":"There are no mother site products to show"})



@api_view(["GET", ])
def individual_specs(request,specification_id):

    try:
        specs = ProductSpecification.objects.get(id = specification_id)
    except:
        specs = None 

    if specs:

        specs_serializer = MotherSpecificationSerializer(specs,many=False)

        return JsonResponse({"success":True,"message":"Individual data is shown","data":specs_serializer.data})
    else:
        return JsonResponse({"success": False,"message":"There is no data to show"})



# @api_view(["POST", ])
# def bring_product(request,mother_specification_id):


#     # data = [{
#     #         "status": "Single",
#     #         "quantity": 1,
#     #         "purchase_price": 300.0,
#     #         "selling_price": 0.0,
#     #         "MRP": 1125.00,
#     #         "increament_type": "Percentage",
# 	#         "increament_value": 10.0,
    
#     #     },
#     #     {
#     #         "status": "Minimum",
#     #         "quantity": 10,
#     #         "purchase_price": 280.0,
#     #         "selling_price": 0.0,
#     #         "MRP": 1125.00,
#     #         "increament_type": "Percentage",
# 	#         "increament_value": 10.0,
#     #     },
#     #     {
#     #         "status": "Maximum",
#     #         "quantity": 100,
#     #         "purchase_price": 30000.0,
#     #         "selling_price": 0.0,
#     #         "MRP": 111125.00,
#     #         "increament_type": "Percentage",
# 	#         "increament_value": 10.0,
#     #     }]
#     data = request.data

#     MRP_flag = 1
#     purchase_price = float(data[0]["purchase_price"])
#     selling_price = float(data[0]["MRP"])
#     main_product_id = 0
#     main_specification_id = 0
    


#     for k in range(len(data)):
#         if data[k]["MRP"] >= data[k]["purchase_price"]:
#             MRP_flag = 1
#         else:
#             MRP_flag = 0
#             break


#     if MRP_flag == 1:


#         try:
#             company= CompanyInfo.objects.all()
#         except:
#             company = None 

#         if company:
#             company = company[0]

#             site_id = company.site_identification
#         else:
#             site_id = ""
#         print("site_id")
#         print(site_id)


#         try:
#             prod_specz = ProductSpecification.objects.all()
#         except:
#             prod_specz = None

#         if prod_specz:

#             all_mother_specification_ids = list(prod_specz.values_list('mother_specification_id',flat=True))

#         else:
#             all_mother_specification_ids = []

#         print(all_mother_specification_ids)

#         if mother_specification_id not in all_mother_specification_ids:

#             specification_id = mother_specification_id
#             url = site_path + "productdetails/individual_specs/" +str(specification_id)+ "/"
#             mother_response = requests.get(url = url)
#             mother_data = mother_response.json()
#             if mother_data["success"] == True:
#                 data = mother_data["data"]
                
#                 print("main data")
#                 print(data)
#                 mother_product_id = data["product_data"]["id"]

#                 try:
#                     product = Product.objects.get(mother_product_id=mother_product_id)

#                 except:
#                     product = None 

#                 if product:
#                     # return JsonResponse({"success":False})
#                     print("product already stored")
#                     product_id = product.id
#                     main_product_id = product_id

#                     spec_data = {"product_id": product_id, "size": data["size"], "unit": data["unit"], "weight": data["weight"], "color": data["color"], "warranty": data["warranty"],
#                     "warranty_unit": data["warranty_unit"], "vat": float(data["vat"]), "weight_unit": data["weight_unit"], "manufacture_date": data["manufacture_date"], "expire": data["expire"],"is_own":False,
#                     "mother_status":"Confirmed","admin_status":"Confirmed","mother_specification_id":data["id"]}
#                     spec_info = insert_specification_data(spec_data)
#                     print("spec_info")
#                     print(spec_info)
#                     specification_id = spec_info["data"]["id"]
#                     main_specification_id = specification_id
#                     data["product_code"]["specification_id"] = specification_id
#                     data["product_code"]["product_id"] = product_id
#                     code_info = insert_code_data(data["product_code"])
#                     print("code_info")
#                     print(code_info)
#                     data["delivery_info"]["specification_id"] = specification_id
#                     delivery_info = insert_delivery_data(data["delivery_info"])
#                     print("dekivery_info")
#                     print(delivery_info)
#                     for i in range(len(data["max_min"])):
#                         data["max_min"][i]["specification_id"] = specification_id
#                         data["max_min"][i]["mother_specification_id"] = data["id"]
#                         data["max_min"][i]["is_own"] = False


#                     max_min_info = insert_max_min_info(data["max_min"])
#                     print("max")
#                     print(max_min_info)

#                     if  spec_info["flag"] == True and code_info["flag"] == True and delivery_info["flag"] == True and max_min_info["flag"] == True:
#                         print("shob true hoise")
#                         main_flag = True
#                         mother_spec_id = data["id"]
#                         print(mother_spec_id)
#                         print(site_id)
#                         url = site_path + "productdetails/track_sharing/"+str(mother_spec_id)+"/"+str(site_id)+ "/"
#                         mother_responses = requests.get(url = url)
#                         print()
#                         mother_datas = mother_responses.json()
#                         if mother_datas["success"] == True:
#                             #Insert the mrp
#                             for i in range(len(data)):
#                                 specification_price = SpecificationPrice.objects.create(specification_id=specification_id,status=data[i]["status"],quantity=int(data[i]["quantity"]),purchase_price=float(data[i]["purchase_price"]),selling_price=float(data[i]["selling_price"]),mrp=float(data[i]["MRP"]),is_active=True,is_own=False)
#                                 specification_price.save()


#                             #Insert the price
#                             spec_price = ProductPrice.objects.create(specification_id=main_specification_id,product_id=main_product_id,price=selling_price,purchase_price=purchase_price)
#                             spec_price.save()

                            


#                             return JsonResponse({"success": True,"message":"Data have been inserted.Product info and product image info has been added before.","spec":spec_info,"code":code_info,"delivery_info":delivery_info,"max_min_info":max_min_info})
#                         else:
#                             return JsonResponse({"success":False,"message": "Data was inserted nut the tracking info was not stored"})
#                     else:
#                         return JsonResponse({"success":False,"message":"Data could not be inserted"})
                    

#                 else:
#                     prod_data = insert_product_data(
#                     data["product_data"], data["category_data"], data["site_id"])
#                     product_id = prod_data["data"]["id"]
#                     main_product_id = main_product_id
#                     product_name = prod_data["data"]["title"]
#                     print(product_name)
#                     print(product_id)
#                     image_data = insert_product_image( data["product_images"],product_id,product_name)
#                     spec_data = {"product_id": product_id, "size": data["size"], "unit": data["unit"], "weight": data["weight"], "color": data["color"], "warranty": data["warranty"],
#                     "warranty_unit": data["warranty_unit"], "vat": float(data["vat"]), "weight_unit": data["weight_unit"], "manufacture_date": data["manufacture_date"], "expire": data["expire"],"is_own":False,
#                     "mother_status":"Confirmed","admin_status":"Confirmed","mother_specification_id":data["id"]}
#                     spec_info = insert_specification_data(spec_data)
#                     specification_id = spec_info["data"]["id"]
#                     main_specification_id = specification_id
#                     data["product_code"]["specification_id"] = specification_id
#                     data["product_code"]["product_id"] = product_id
#                     code_info = insert_code_data(data["product_code"])
#                     data["delivery_info"]["specification_id"] = specification_id
#                     delivery_info = insert_delivery_data(data["delivery_info"])
#                     for i in range(len(data["max_min"])):
#                         data["max_min"][i]["specification_id"] = specification_id
#                         data["max_min"][i]["mother_specification_id"] = data["id"]
#                         data["max_min"][i]["is_own"] = False


#                     max_min_info = insert_max_min_info(data["max_min"])

#                     if prod_data["flag"] == True and spec_info["flag"] == True and code_info["flag"] == True and delivery_info["flag"] == True and max_min_info["flag"] == True:
#                         main_flag = True
#                         mother_spec_id = data["id"]
#                         url = site_path + "productdetails/track_sharing/"+str(mother_spec_id)+"/"+str(site_id)+ "/"
#                         mother_responses = requests.get(url = url)
#                         mother_datas = mother_responses.json()
#                         if mother_datas["success"] == True:
#                             #Insert the mrp
#                             for i in range(len(data)):
#                                 specification_price = SpecificationPrice.objects.create(specification_id=specification_id,status=data[i]["status"],quantity=int(data[i]["quantity"]),purchase_price=float(data[i]["purchase_price"]),selling_price=float(data[i]["selling_price"]),mrp=float(data[i]["MRP"]),is_active=True,is_own=False)
#                                 specification_price.save()

#                             #Insert the price
#                             spec_price = ProductPrice.objects.create(specification_id=main_specification_id,product_id=main_product_id,price=selling_price,purchase_price=purchase_price)
#                             spec_price.save()

#                             return JsonResponse({"success": True,"message":"Data have been inserted","product": prod_data,"spec":spec_info,"code":code_info,"delivery_info":delivery_info,"max_min_info":max_min_info,"product_image":image_data})
#                         else:
#                             return JsonResponse({"success":False,"message": "Data was inserted nut the tracking info was not stored"})
#                     else:
#                         return JsonResponse({"success":False,"message":"Data could not be inserted"})

                    
                    
                    
#             else:
#                 return JsonResponse({"success":False,"message":"Data could not be retrieved from mother site"})

#         else:
#             return JsonResponse({"success":False,"message":"This specfication had already been shared before"})

#     else:
#         return JsonResponse({"success":False,"message":'The MRP provided is less than the purchase price'})

@api_view(["POST", ])
def bring_product(request,mother_specification_id):


    # data = [{
    #         "status": "Single",
    #         "quantity": 1,
    #         "purchase_price": 300.0,
    #         "selling_price": 0.0,
    #         "MRP": 1125.00,
    #         "increament_type": "Percentage",
	#         "increament_value": 10.0,
    
    #     },
    #     {
    #         "status": "Minimum",
    #         "quantity": 10,
    #         "purchase_price": 280.0,
    #         "selling_price": 0.0,
    #         "MRP": 1125.00,
    #         "increament_type": "Percentage",
	#         "increament_value": 10.0,
    #     },
    #     {
    #         "status": "Maximum",
    #         "quantity": 100,
    #         "purchase_price": 30000.0,
    #         "selling_price": 0.0,
    #         "MRP": 111125.00,
    #         "increament_type": "Percentage",
	#         "increament_value": 10.0,
    #     }]

    data = request.data
    dataX = data
    
    print(data)

    MRP_flag = 1
    purchase_price = float(data[0]["purchase_price"])
    selling_price = float(data[0]["MRP"])
    main_product_id = 0
    main_specification_id = 0
    


    for k in range(len(data)):
        if data[k]["MRP"] >= data[k]["purchase_price"]:
            MRP_flag = 1
        else:
            MRP_flag = 0
            break


    if MRP_flag == 1:


        try:
            company= CompanyInfo.objects.all()
        except:
            company = None 

        if company:
            company = company[0]

            site_id = company.site_identification
        else:
            site_id = ""
        print("site_id")
        print(site_id)


        try:
            prod_specz = ProductSpecification.objects.all()
        except:
            prod_specz = None

        if prod_specz:

            all_mother_specification_ids = list(prod_specz.values_list('mother_specification_id',flat=True))

        else:
            all_mother_specification_ids = []

        print(all_mother_specification_ids)

        if mother_specification_id not in all_mother_specification_ids:

            specification_id = mother_specification_id
            url = site_path + "productdetails/individual_specs/" +str(specification_id)+ "/"
            mother_response = requests.get(url = url)
            mother_data = mother_response.json()
            if mother_data["success"] == True:
                data = mother_data["data"]
                
                print("main data")
                print(data)
                mother_product_id = data["product_data"]["id"]

                try:
                    product = Product.objects.get(mother_product_id=mother_product_id)

                except:
                    product = None 

                if product:
                    # return JsonResponse({"success":False})
                    print("product already stored")
                    product_id = product.id
                    main_product_id = product_id

                    spec_data = {"product_id": product_id, "size": data["size"], "unit": data["unit"], "weight": data["weight"], "color": data["color"], "warranty": data["warranty"],
                    "warranty_unit": data["warranty_unit"], "vat": float(data["vat"]), "weight_unit": data["weight_unit"], "manufacture_date": data["manufacture_date"], "expire": data["expire"],"is_own":False,
                    "mother_status":"Confirmed","admin_status":"Confirmed","mother_specification_id":data["id"]}
                    spec_info = insert_specification_data(spec_data)
                    print("spec_info")
                    print(spec_info)
                    specification_id = spec_info["data"]["id"]
                    main_specification_id = specification_id
                    data["product_code"]["specification_id"] = specification_id
                    data["product_code"]["product_id"] = product_id
                    code_info = insert_code_data(data["product_code"])
                    print("code_info")
                    print(code_info)
                    data["delivery_info"]["specification_id"] = specification_id
                    delivery_info = insert_delivery_data(data["delivery_info"])
                    print("dekivery_info")
                    print(delivery_info)
                    for i in range(len(data["max_min"])):
                        data["max_min"][i]["specification_id"] = specification_id
                        data["max_min"][i]["mother_specification_id"] = data["id"]
                        data["max_min"][i]["is_own"] = False


                    max_min_info = insert_max_min_info(data["max_min"])
                    print("max")
                    print(max_min_info)

                    if  spec_info["flag"] == True and code_info["flag"] == True and delivery_info["flag"] == True and max_min_info["flag"] == True:
                        print("shob true hoise")
                        main_flag = True
                        mother_spec_id = data["id"]
                        print(mother_spec_id)
                        print(site_id)
                        url = site_path + "productdetails/track_sharing/"+str(mother_spec_id)+"/"+str(site_id)+ "/"
                        mother_responses = requests.get(url = url)
                        print()
                        mother_datas = mother_responses.json()
                        if mother_datas["success"] == True:
                            #Insert the mrp
                            print("databefore")
                            print(data)
                            for i in range(len(dataX)):
                                specification_price = SpecificationPrice.objects.create(specification_id=specification_id,status=dataX[i]["status"],quantity=int(dataX[i]["quantity"]),purchase_price=float(dataX[i]["purchase_price"]),selling_price=float(dataX[i]["selling_price"]),mrp=float(dataX[i]["MRP"]),is_active=True,is_own=False)
                                specification_price.save()


                            #Insert the price
                            spec_price = ProductPrice.objects.create(specification_id=main_specification_id,product_id=main_product_id,price=selling_price,purchase_price=purchase_price)
                            spec_price.save()

                            


                            return JsonResponse({"success": True,"message":"Data have been inserted.Product info and product image info has been added before.","spec":spec_info,"code":code_info,"delivery_info":delivery_info,"max_min_info":max_min_info})
                        else:
                            return JsonResponse({"success":False,"message": "Data was inserted nut the tracking info was not stored"})
                    else:
                        return JsonResponse({"success":False,"message":"Data could not be inserted"})
                    

                else:
                    prod_data = insert_product_data(
                    data["product_data"], data["category_data"], data["site_id"])
                    product_id = prod_data["data"]["id"]
                    main_product_id = main_product_id
                    product_name = prod_data["data"]["title"]
                    print(product_name)
                    print(product_id)
                    image_data = insert_product_image( data["product_images"],product_id,product_name)
                    spec_data = {"product_id": product_id, "size": data["size"], "unit": data["unit"], "weight": data["weight"], "color": data["color"], "warranty": data["warranty"],
                    "warranty_unit": data["warranty_unit"], "vat": float(data["vat"]), "weight_unit": data["weight_unit"], "manufacture_date": data["manufacture_date"], "expire": data["expire"],"is_own":False,
                    "mother_status":"Confirmed","admin_status":"Confirmed","mother_specification_id":data["id"]}
                    spec_info = insert_specification_data(spec_data)
                    specification_id = spec_info["data"]["id"]
                    main_specification_id = specification_id
                    data["product_code"]["specification_id"] = specification_id
                    data["product_code"]["product_id"] = product_id
                    code_info = insert_code_data(data["product_code"])
                    data["delivery_info"]["specification_id"] = specification_id
                    delivery_info = insert_delivery_data(data["delivery_info"])
                    for i in range(len(data["max_min"])):
                        data["max_min"][i]["specification_id"] = specification_id
                        data["max_min"][i]["mother_specification_id"] = data["id"]
                        data["max_min"][i]["is_own"] = False


                    max_min_info = insert_max_min_info(data["max_min"])

                    if prod_data["flag"] == True and spec_info["flag"] == True and code_info["flag"] == True and delivery_info["flag"] == True and max_min_info["flag"] == True:
                        main_flag = True
                        mother_spec_id = data["id"]
                        url = site_path + "productdetails/track_sharing/"+str(mother_spec_id)+"/"+str(site_id)+ "/"
                        mother_responses = requests.get(url = url)
                        mother_datas = mother_responses.json()
                        if mother_datas["success"] == True:
                            #Insert the mrp
                            # print("data")
                            # print(data)
                            for i in range(len(dataX)):
                                # print(specification_id)
                                # print(data[i]["status"])
                                # print(data[i]["quantity"])
                                # print(data[i]["purchase_price"])
                                # print(data[i]["selling_price"])
                                # print(data[i]["MRP"])
                                specification_price = SpecificationPrice.objects.create(specification_id=specification_id,status=dataX[i]["status"],quantity=int(dataX[i]["quantity"]),purchase_price=float(dataX[i]["purchase_price"]),selling_price=float(dataX[i]["selling_price"]),mrp=float(dataX[i]["MRP"]),is_active=True,is_own=False)
                                specification_price.save()

                            #Insert the price
                            spec_price = ProductPrice.objects.create(specification_id=main_specification_id,product_id=main_product_id,price=selling_price,purchase_price=purchase_price)
                            spec_price.save()

                            return JsonResponse({"success": True,"message":"Data have been inserted","product": prod_data,"spec":spec_info,"code":code_info,"delivery_info":delivery_info,"max_min_info":max_min_info,"product_image":image_data})
                        else:
                            return JsonResponse({"success":False,"message": "Data was inserted nut the tracking info was not stored"})
                    else:
                        return JsonResponse({"success":False,"message":"Data could not be inserted"})

                    
                    
                    
            else:
                return JsonResponse({"success":False,"message":"Data could not be retrieved from mother site"})

        else:
            return JsonResponse({"success":False,"message":"This specfication had already been shared before"})

    else:
        return JsonResponse({"success":False,"message":'The MRP provided is less than the purchase price'})

def insert_product_image(product_images,product_id,product_name):

    image_data = []
    
    for i in range(len(product_images)):
        prod_image = ProductImage.objects.create(product_id = product_id ,content = product_images[i]["content"], mother_url = product_images[i]["image_url"], is_own=False)
        prod_image.save()
        prod_image_id = prod_image.id
        

        #image_url = 'http://whatever.com/image.jpg'
        image_url = prod_image.mother_url
        r = requests.get(image_url)
        # img_temp = NamedTemporaryFile()
        # img_temp.write(urlopen(image_url).read())
        # img_temp.flush()
        img_temp = NamedTemporaryFile()
        img_temp.write(r.content)
        img_temp.flush()
        image_name = product_name + str(prod_image_id)+".jpg"

        prod_image.product_image.save(image_name, File(img_temp), save=True)

        # prod_image.product_image.save("image_%s" % prod_image.pk, ImageFile(img_temp))

        # response = requests.get(image_url)
        # img = Image.open(BytesIO(response.content))
        # prod_image.product_image = img
        # prod_image.save()

        prod_image_serializer  = MotherProductImageCreationSerializer(prod_image,many=False)
        im_data = prod_image_serializer.data
        image_data.append(im_data)

    return ({"flag":True,"data":image_data})
        






def insert_product_data(product_data, category_data, site_data):
    # print(product_data)
    # print(category_data)

    category_ids = category1_data_upload(category_data)
    cat_data = category_ids.json()
    category_id = cat_data["category"]
    sub_category_id = cat_data["sub_category"]
    sub_sub_category_id = cat_data["sub_sub_category"]
    is_own = False
    product_admin_status = "Confirmed"
    title = product_data["title"]
    brand = product_data["brand"]
    description = product_data["description"]
    # print("description")
    # print(description)
    key_features = product_data["key_features"]
    # print("key_features")
    # print(key_features)
    is_group = product_data["is_group"]
    origin = product_data["origin"]
    shipping_country = product_data["shipping_country"]
    # mother_status =  product_data["mother_status"]
    mother_product_id = int(product_data["id"])

    # unique_id = "X"+str(child_product_id) + "Y" + str(child_site_id)
    # data_values = {"category_id": category_id, "sub_category_id": sub_category_id, "sub_sub_category_id": sub_sub_category_id,
    #                "is_own": False, "product_admin_status": product_admin_status, "title": title, "brand": brand, "description": description, "key_features": key_features,
    #                "origin": origin, "shipping_country": shipping_country, "is_group": is_group, "mother_product_id": mother_product_id,
    #                "mother_status": "Confirmed","product_status" :"Published"}

    product = Product.objects.create(category_id = category_id,sub_category_id=sub_category_id,sub_sub_category_id=sub_sub_category_id,is_own=False,product_admin_status=product_admin_status,title=title,brand=brand,description=description,key_features=key_features,origin=origin,shipping_country=shipping_country,is_group=is_group,mother_product_id=mother_product_id,mother_status="Confimred",product_status="Published")
    product.save()
    p_id = product.id 
    try:
        prod = Product.objects.get(id=p_id)
    except:
        prod = None 

    if prod:
        product_serializer = ChildProductCreationSerializer(prod,many=False)
        return ({"flag":True,"data":product_serializer.data})
    else:
        return ({"flag":False,"data":[]})




    # product_serializer = ChildProductCreationSerializer(data=data_values)
    # if product_serializer.is_valid():
    #     print("product save hochche")
    #     product_serializer.save()
    #     product_id = int(product_serializer.data["id"])
        # globals()['global_product_id'] = product_id
        # try:
        #     product = Product.objects.get(id=product_id)
        # except:
        #     product = None
        # if product:
        #     unique_id = "X"+str(child_product_id) + "Y" + str(child_site_id) + "Z" + str(product_id)
        #     product.unique_id = unique_id
        #     product.save()
        #     product_serializer = ChildProductCreationSerializer(product,many=False)
    #     return ({"flag":True,"data":product_serializer.data})

    # else:
    #     print(product_serializer.errors)
    #     return ({"flag":False,"data":[]})


def insert_specification_data(spec_data):

    specification_serializer = MotherSpecificationCreationSerializer(data=spec_data)
    if specification_serializer.is_valid():
        specification_serializer.save()
        print("specification save hochche")
        # product_id = int(product_serializer.data["id"])
        #globals()['global_product_id'] = product_id
        #print(product_serializer.data)
        return ({"flag":True,"data": specification_serializer.data})

    else:
        print(specification_serializer.errors)
        return ({"flag":False,"data":[]})


def insert_code_data(code_data):

    specification_serializer = MotherCodeCreationSerializer(data=code_data)
    if specification_serializer.is_valid():
        specification_serializer.save()
        # product_id = int(product_serializer.data["id"])
        #globals()['global_product_id'] = product_id
        #print(product_serializer.data)
        return ({"flag":True,"data": specification_serializer.data})

    else:
        print(specification_serializer.errors)
        return ({"flag":False,"data":[]})
    
def insert_delivery_data(delivery_data):

    specification_serializer = MotherDeliveryInfoCreationSerializer(data= delivery_data)
    if specification_serializer.is_valid():
        specification_serializer.save()
        # product_id = int(product_serializer.data["id"])
        #globals()['global_product_id'] = product_id
        #print(product_serializer.data)
        return ({"flag":True,"data": specification_serializer.data})

    else:
        print(specification_serializer.errors)
        return ({"flag":False,"data":[]})
    

def insert_max_min_info(max_min_data):

    max_min = []

    for i in range(len(max_min_data)):

        if max_min_data[i]["status"] == "single" or max_min_data[i]["status"] == "Single" :
            max_min_data[i]["status"] = "Single"

        if max_min_data[i]["status"] == "min" or max_min_data[i]["status"] == "Single" :
            max_min_data[i]["status"] = "Single"


        specification_serializer = ChildSpecificationPriceSerializer(data= max_min_data[i])
        if specification_serializer.is_valid():
            specification_serializer.save()
            max_min.append(specification_serializer.data)
        else:
            return ({"flag":False,"data":[]})

    return ({"flag":True,"data":max_min})




@api_view(["GET",])
def unsharedSpecification(request):

    try:
        spec = ProductSpecification.objects.filter(shared=False,is_own=True)
    except:
        spec = None
    print("this is spec data" , spec) 

    if spec:
        spec_serializer = OwnSpecificationSerializer(spec,many=True)
        spec_data = spec_serializer.data
        return JsonResponse({"success":True,"message":"Data is shown","data":spec_data})
     
    
    else:
        return JsonResponse({"success":False,"message":"Data doesnt exist"})
    

@api_view(["GET"])
def own_quantity_check(request,specification_id):

    try:
        prod = ProductSpecification.objects.get(id=specification_id)
    except:
        prod = None 

    if prod:
        if prod.is_own == True:
            if prod.shared == True:
                quantity = prod.quantity
                return JsonResponse({"success":True,"message":"The current quantity is shown","quantity":quantity})
            
            else:
                return JsonResponse({"success":False,"message":"This product has not been shared so cannot return the quantity"})


        else:
            return JsonResponse({"success":False,"message":"This product is not my own product so cannot return the quantity"})


    else:
        return JsonResponse({"success":False,"message":"This product does not exist"})



@api_view(["GET"])
def not_own_quantity_check(request,specification_id):

    try:
        prod = ProductSpecification.objects.get(id=specification_id)
    except:
        prod = None 

    if prod:
        if prod.is_own == False:
            mother_specification_id = prod.mother_specification_id
            
            url = site_path + "productdetails/quantity_checker/" +str(mother_specification_id)+ "/"
            mother_response = requests.get(url = url)
            mother_response = mother_response.json()
            if mother_response["success"] == True:
                quantity = mother_response["quantity"]           
                return JsonResponse({"success":True,"message":"The current quantity is shown","quantity":quantity})

            else:
                return JsonResponse({"success":False,"message":"The quantity could not be retireved."})
            
           


        else:
            return JsonResponse({"success":False,"message":"This product is your own product"})


    else:
        return JsonResponse({"success":False,"message":"This product does not exist"})




# def get_max_min_values()
@api_view(["POST"])
def update_max_min_values(request,specification_id):

    # data = [
    #     {
    #                 "id": 53,
    #                 "status": "Single",
    #                 "quantity": 1,
    #                 "purchase_price": 300.0,
    #                 "selling_price": 370.0,
    #                 "mrp": 25.0,
    #                 "is_active": True,
    #                 "specification_id": 10,
    #                 "is_own": True,
    #                 "mother_specification_id": -1,
    #                 "increament_type": "Percentage",
    #                 "increament_value": 0.0
    #             },
    #             {
    #                 "id": 54,
    #                 "status": "Minimum",
    #                 "quantity": 10,
    #                 "purchase_price": 300.0,
    #                 "selling_price": 370.0,
    #                 "mrp": 25.0,
    #                 "is_active": True,
    #                 "specification_id": 10,
    #                 "is_own": True,
    #                 "mother_specification_id": -1,
    #                 "increament_type": "Percentage",
    #                 "increament_value": 0.0
    #             },
    #             {
    #                 "id": 55,
    #                 "status": "Maximum",
    #                 "quantity": 100,
    #                 "purchase_price": 300.0,
    #                 "selling_price": 370.0,
    #                 "mrp": 25.0,
    #                 "is_active": True,
    #                 "specification_id": 10,
    #                 "is_own": True,
    #                 "mother_specification_id": -1,
    #                 "increament_type": "Percentage",
    #                 "increament_value": 0.0
    #             }


            
                
    #     ]

    data = {  'arrayForDelivery': [
                    {
                        'selectedDistrict': 'Dhaka',
                        'selectedThana':[
                            'Banani',
                            'Gulshan',
                            'Rampura',
                            'Dhanmondi'
                        ]
                    },
                    {
                        'selectedDistrict': 'Barishal',
                        'selectedThana':[
                            'Hizla',
                            'Muladi',
                            'Borguna',
                            'Betagi'
                        ]
                    }
                ],

                'max_min' : [
        {
                    "id": 53,
                    "status": "Single",
                    "quantity": 1,
                    "purchase_price": 300.0,
                    "selling_price": 370.0,
                    "mrp": 25.0,
                    "is_active": True,
                    "specification_id": 10,
                    "is_own": True,
                    "mother_specification_id": -1,
                    "increament_type": "Percentage",
                    "increament_value": 0.0
                },
                {
                    "id": 54,
                    "status": "Minimum",
                    "quantity": 10,
                    "purchase_price": 300.0,
                    "selling_price": 370.0,
                    "mrp": 25.0,
                    "is_active": True,
                    "specification_id": 10,
                    "is_own": True,
                    "mother_specification_id": -1,
                    "increament_type": "Percentage",
                    "increament_value": 0.0
                },
                {
                    "id": 55,
                    "status": "Maximum",
                    "quantity": 100,
                    "purchase_price": 300.0,
                    "selling_price": 370.0,
                    "mrp": 25.0,
                    "is_active": True,
                    "specification_id": 10,
                    "is_own": True,
                    "mother_specification_id": -1,
                    "increament_type": "Percentage",
                    "increament_value": 0.0
                }           
        ]
                }

    # data = request.data

    
    flag = 0 
    spec_data = []
    restore_data = []
    


    for i in range(len(data)):
        max_min_id = data[i]["id"]
        max_min_data = data[i]
        try:
            spec_price = SpecificationPrice.objects.get(id=max_min_id)

        except:
            spec_price = None 

        if spec_price:
            restore_serializer = MaxMinSerializer1(spec_price,many=False)
            restore_dataz = restore_serializer.data
            restore_data.append(restore_dataz)

            spec_price_serializer = MaxMinSerializer1(spec_price,data=max_min_data)
            if spec_price_serializer.is_valid():
                spec_price_serializer.save()
                flag = flag + 1
        else:
            return JsonResponse({"success":False,"message":"This max min value does not exist"})

    try:
        spec_pricez = SpecificationPrice.objects.filter(specification_id=specification_id)
    except:
        spec_pricez = None 

    if spec_pricez:
        spec_pricez_serializer = MaxMinSerializer(spec_pricez,many=True)
        spec_data = spec_pricez_serializer.data
    else:
        spec_data = []


    if flag == 3:

        try:
            company= CompanyInfo.objects.all()
        except:
            company = None 

        if company:
            company = company[0]
            site_id = company.site_identification
        else:
            site_id = ""

        print(specification_id)
        print(site_id)

        spec_dataz = json.dumps(spec_data)

        url = site_path + "productdetails/update_own_specification_prices/" + str(specification_id) + "/" +  str(site_id) + "/"
        headers = {'Content-Type': 'application/json',}
        print(spec_data)
        dataz = requests.post(url = url, headers=headers,data = spec_dataz)

        data_response = dataz.json()
        if data_response["success"] == True:
            print("true hochche")
            return JsonResponse({"success":True,"message":"The values have been updated","data":spec_data})

        else:
            #restore the values 
            print("true hochche na")
            data = restore_data
            for i in range(len(data)):
                max_min_id = data[i]["id"]
                max_min_data = data[i]
                try:
                    spec_price = SpecificationPrice.objects.get(id=max_min_id)

                except:
                    spec_price = None 

                if spec_price:
                    # restore_serializer = MaxMinSerializer(spec_price,many=False)
                    # restore_dataz = restore_serializer.data
                    # restore_data.append(restore_dataz)

                    spec_price_serializer = MaxMinSerializer1(spec_price,data=max_min_data)
                    if spec_price_serializer.is_valid():
                        spec_price_serializer.save()
                        flag = flag + 1
                else:
                    return JsonResponse({"success":False,"message":"This max min value does not exist"})

            return JsonResponse({"success":False,"message":'Mother site did not respond so data was not inserted'})



    else:
        #restore the data

        data = restore_data

        for i in range(len(data)):

            max_min_id = data[i]["id"]
            max_min_data = data[i]
            try:
                spec_price = SpecificationPrice.objects.get(id=max_min_id)

            except:
                spec_price = None 

            if spec_price:
                # restore_serializer = MaxMinSerializer1(spec_price,many=False)
                # restore_dataz = restore_serializer.data
                # restore_data.append(restore_dataz)

                spec_price_serializer = MaxMinSerializer1(spec_price,data=max_min_data)
                if spec_price_serializer.is_valid():
                    spec_price_serializer.save()
                    flag = flag + 1
            else:
                return JsonResponse({"success":False,"message":"This max min value does not exist"})

        return JsonResponse({"success":False,"message":"The values could not be updated"})



def check_price(request,specification_id):

    #Fetching the max min values

    try:
        product_spec = ProductSpecification.objects.get(id = specification_id)
    except:
        product_spec = None 

    print(product_spec)

    if product_spec:
        mother_specification_id = product_spec.mother_specification_id
        if product_spec.is_own == True:

            return JsonResponse({"success":False, "message":"This is your own product you dont need to check the price."})

        else:
            #Fetch the max min values from the mother site
            url = site_path + "productdetails/show_max_min_values/" +str(mother_specification_id)+ "/"
            mother_response = requests.get(url = url)
            mother_response = mother_response.json()
           
            if mother_response["success"] == True:
                if mother_response["on_hold"] == True:
                    product_spec.on_hold = True
                    return JsonResponse({"success":True,"message":"The product is kept on hold and cannot be sold"})

                else:
                    counter_flag = 0
                    mother_data = mother_response["data"]
                    print(mother_data)
                    print(specification_id)

                    #Fetch the Specification Price of this product
                    try:
                        specification_prices = SpecificationPrice.objects.filter(specification_id = specification_id).order_by('id')
                    except:
                        specification_prices = None 
                    
                   

                    print(specification_prices)

                    if specification_prices:

                        spec_serializer = MaxMinSerializer1(specification_prices,many=True)
                        specs_data = spec_serializer.data

                        specs_data = json.loads(json.dumps(specs_data))
                        

                        #Making the comparisons
                        print(specs_data)
                        print(type(mother_data[0]["quantity"]))
                        print(type(specs_data[0]["quantity"]))
                        if mother_data[0]["status"] == "Single" and specs_data[0]["status"] == "Single":
                            if mother_data[0]["quantity"] == specs_data[0]["quantity"] and mother_data[0]["selling_price"] == specs_data[0]["purchase_price"]:
                                counter_flag = counter_flag +1 
                            else:
                                pass

                        else:
                            pass 

                        if mother_data[1]["status"] == "Minimum" and specs_data[1]["status"] == "Minimum":
                            if mother_data[1]["quantity"] == specs_data[1]["quantity"] and mother_data[1]["selling_price"] == specs_data[1]["purchase_price"]:
                                counter_flag = counter_flag +1 
                            else:
                                pass

                        else:
                            pass


                        
                        if mother_data[2]["status"] == "Maximum" and specs_data[2]["status"] == "Maximum":
                            if mother_data[2]["quantity"] == specs_data[2]["quantity"] and mother_data[2]["selling_price"] == specs_data[2]["purchase_price"]:
                                counter_flag = counter_flag +1 
                            else:
                                pass

                        else:
                            pass  

                        print("counter_flag")

                        print(counter_flag)


                        if counter_flag == 3:
                            return JsonResponse({"success":True,"message":"The product can be sold"})

                        else:
                            return JsonResponse({"success":False,"message":"This product's price has been changed and has to be on hold"})

                    else:
                        return JsonResponse({"success":False,"message":"The specification prices do not exist"})
    else:
        return JsonResponse({"success":False,"message":"This product does not exist"})

             

        
@api_view(["GET",])
def approve_purchase_order(request, order_id):

    try:
        order = Order.objects.get(id = order_id)

    except:
        order = None 

    

    all_item_data = []

    if order:
        order.admin_status = "Confirmed"
        order.save()
        warehouse_id = find_warehouse_id()
        try:
            order_details = OrderDetails.objects.filter(order_id = order_id)

        except:
            order_details = None 

        if order_details:
            order_details_ids = list(order_details.values_list('id', flat=True))
        else:
            order_details_ids = []

        for i in range(len(order_details_ids)):
            try:
                specific_item = OrderDetails.objects.get(id = order_details_ids[i])
            except:
                specific_item = None 

            if specific_item:
                specific_item.admin_status = specific_item.mother_admin_status
                specific_item.save()
                purchase_price = specific_item.unit_price
                specification_id = specific_item.specification_id
                selling_price = fetch_selling_price(specification_id)
                warehouse = [{"warehouse_id":warehouse_id,"quantity":specific_item.total_quantity}]
                shop = []
                item_data = {"product_id":specific_item.product_id,"specification_id":specific_item.specification_id,"purchase_price":purchase_price,"selling_price":selling_price,"warehouse":warehouse,"shop":shop}
                insert_quantity = insert_purchase_product_quantity(item_data,order_id)
                print("INSERT QUANTITY")
                print(insert_quantity)
                # all_item_data.append(item_data)

            else:
                pass


        # main_data = {"order_id":order_id,"info":all_item_data }
        # print(main_data)
        # change_statuses = change_orderdetails_statuses(main_data)
        return JsonResponse({"success":True,"message":"This invoice hass been approved"})

            
    
    else:
        return JsonResponse({"success":False,"message":"This order does not exist"})





def insert_purchase_product_quantity(api_values,order_id):

    # demo values
    # api_values = {
          
    #     'product_id':35,
    #     'specification_id':34,
    #     'purchase_price': 100,
    #     'selling_price': 120,
    #     'warehouse': [
    #         {
    #             'warehouse_id': 1,
    #             'quantity': 200

    #         },
    #         {
    #             'warehouse_id': 2,
    #             'quantity': 200

    #         }
    #     ],

    #      'shop': [
    #         {
    #             'shop_id': 3,
    #             'quantity': 200

    #         },
    #         {
    #             'shop_id': 2,
    #             'quantity': 200

    #         },
    #         {
    #             'shop_id': 1,
    #             'quantity': 200

    #         }

    #     ]

    #     }

    #api_values = request.data
    current_date = date.today()

    #if request.method == 'POST':

        # Insert the purchase price and selling price for that object:

        # try:

    price_data = {"product_id": api_values["product_id"], "specification_id": api_values["specification_id"],
                    "price": api_values["selling_price"], "purchase_price": api_values["purchase_price"]}

    # Inserting the price

    product_price_serializer = ProductPriceSerializer(data=price_data)
    print("fjeswdifhfhds")
    if product_price_serializer.is_valid():

        product_price_serializer.save()
    else:
        print(product_price_serializer.errors)

    # except:

    #     return JsonResponse({"success": False, "message": "The price could not be inserted"})

    try:
        # Fetching the product price

        prod_price = ProductPrice.objects.filter(
            specification_id=api_values["specification_id"]).last()

    except:

        prod_price = None

    if prod_price:

        purchase_price = prod_price.purchase_price
        selling_price = prod_price.price

    else:

        return {"success": False, "message": "Price does not exist for this product"}

    try:

        # checking is there any warehouse data exists or not
        if len(api_values['warehouse']) > 0:
            for wareh in api_values['warehouse']:
                try:
                    # getting the previous data if there is any in the similar name. If exists update the new value. if does not create new records.
                    wareh_query = WarehouseInfo.objects.filter(
                        warehouse_id=wareh['warehouse_id'], specification_id=api_values['specification_id']).last()

                    print("quertresult")
                    print(wareh_query)

                    if wareh_query:
                        # quantity_val = wareh_query[0].quantity
                        # new_quantity = quantity_val + wareh['quantity']
                        # wareh_query.update(quantity=new_quantity)
                        # wareh_query.save()
                        print("existing warehouse")
                        print(type(wareh['quantity']))
                        print(wareh_query.quantity)

                        warehouse_quantity = wareh_query.quantity

                        print(warehouse_quantity)

                        new_quantity = warehouse_quantity + int(wareh['quantity'])

                        print(new_quantity)

                        wareh_query.quantity = new_quantity
                        print(wareh_query.quantity)
                        wareh_query.save()
                        print(wareh_query.quantity)

                        try:
                            product_spec = ProductSpecification.objects.get(
                                id=api_values['specification_id'])

                        except:
                            product_spec = None

                        if product_spec:

                            product_spec.save()

                    else:
                        print("else ey dhuktese")
                        wareh_data = WarehouseInfo.objects.create(specification_id=api_values['specification_id'], product_id=api_values['product_id'], warehouse_id=wareh['warehouse_id'],
                                                                    quantity=int(wareh['quantity']))
                        wareh_data.save()

                        try:
                            product_spec = ProductSpecification.objects.get(
                                id=api_values['specification_id'])

                        except:
                            product_spec = None

                        if product_spec:

                            product_spec.save()

                    # updating the inventory report credit records for each ware house quantity. It will help to keep the records in future.
                    # report_data = inventory_report(
                    #     product_id=api_values['product_id'], credit=wareh['quantity'], warehouse_id=wareh['warehouse_id'])
                    # report_data.save()
                    # Check to see if there are any inventory_reports
                    # try:

                    #     report = inventory_report.objects.filter(product_id=api_values['product_id'],specification_id=api_values['specification_id'],warehouse_id=wareh['warehouse_id'],date=current_date).last()

                    # except:

                    #     report = None

                    # if report:

                    #     #Update the existing report

                    #     report.credit += int(wareh['quantity'])
                    #     report.save()

                    new_report = inventory_report.objects.create(product_id=api_values['product_id'], specification_id=api_values['specification_id'], warehouse_id=wareh['warehouse_id'], credit=int(
                        wareh['quantity']), date=current_date, purchase_price=purchase_price, selling_price=selling_price)
                    new_report.save()

                    # subtract_item = subtraction_track.objects.create(order_id = order_id, specification_id=api_values['specification_id'], warehouse_id=wareh['warehouse_id'], debit_quantity=int(
                    #     wareh['quantity']), date=current_date)

                    # subtract_item.save()

                except:
                    pass

        if len(api_values['shop']) > 0:
            for shops in api_values['shop']:
                try:
                    # getting the existing shop values if is there any.
                    print(shops['shop_id'])
                    shop_query = ShopInfo.objects.filter(
                        shop_id=shops['shop_id'], specification_id=api_values['specification_id']).last()
                    print(shop_query)
                    if shop_query:
                        print("shop ase")
                        quantity_val = shop_query.quantity
                        new_quantity = quantity_val + int(shops['quantity'])
                        # shop_query.update(quantity=new_quantity)
                        shop_query.quantity = new_quantity
                        shop_query.save()

                        try:
                            product_spec = ProductSpecification.objects.get(
                                id=api_values['specification_id'])

                        except:
                            product_spec = None

                        if product_spec:

                            product_spec.save()
                    else:
                        print("shop nai")
                        shop_data = ShopInfo.objects.create(specification_id=api_values['specification_id'], product_id=api_values['product_id'], shop_id=shops['shop_id'],
                                                            quantity=int(shops['quantity']))
                        shop_data.save()
                    # Updating the report table after being inserted the quantity corresponding to credit coloumn for each shop.
                    # report_data = inventory_report(
                    #     product_id=api_values['product_id'], credit=shops['quantity'], shop_id=shops['shop_id'])
                    # report_data.save()

                        try:
                            product_spec = ProductSpecification.objects.get(
                                id=api_values['specification_id'])

                        except:
                            product_spec = None

                        if product_spec:

                            product_spec.save()

                    new_report = inventory_report.objects.create(product_id=api_values['product_id'], specification_id=api_values['specification_id'], shop_id=shops['shop_id'], credit=int(
                        shops['quantity']), date=current_date, purchase_price=purchase_price, selling_price=selling_price)
                    new_report.save()

                    # subtract_item = subtraction_track.objects.create(order_id = order_id, specification_id=api_values['specification_id'], shop_id = shops['shop_id'], debit_quantity=int(
                    #     shops['quantity']), date=current_date)

                    # subtract_item.save()

                except:
                    pass

        #Insert subtract method here
        subtraction_result = subtract_purchase_product_quantity(api_values,order_id)
        print("SUBTRACTION_RESULT")
        print(subtraction_result)

        return {
            "success": True,
            "message": "Data has been added successfully"
        }
    except:
        return {
            "success": False,
            "message": "Something went wrong !!"
        }


# def subtract_purchase_warehouse quantity()
# def approve_purchase_orders(request,order_id):

def subtract_purchase_product_quantity(api_values,order_id):  
    print(api_values)

    # api_values = {
        
    # 'product_id':35,
    # 'specification_id':34,
    # 'purchase_price': 100,
    # 'selling_price': 120,
    # 'warehouse': [
    #     {
    #         'warehouse_id': 1,
    #         'quantity': 200

    #     },
    #     {
    #         'warehouse_id': 2,
    #         'quantity': 200

    #     }
    # ],

    #  'shop': [
    #     {
    #         'shop_id': 3,
    #         'quantity': 200

    #     },
    #     {
    #         'shop_id': 2,
    #         'quantity': 200

    #     },
    #     {
    #         'shop_id': 1,
    #         'quantity': 200

    #     }

    # ]

    # }

    #api_values = request.data
    current_date = date.today()

    warehouse_data = api_values["warehouse"]
    shop_data = api_values["shop"]
    specification_id = api_values["specification_id"]
    product_id = api_values["product_id"]

    print(shop_data)
    print(warehouse_data)


    try:
        if len(warehouse_data) > 0:

            for i in range(len(warehouse_data)):

                try:
                    warehouse_info = WarehouseInfo.objects.filter(specification_id=specification_id,warehouse_id=warehouse_data[i]["warehouse_id"]).last()
                except:
                    warehouse_info = None 

                if warehouse_info:
                    if warehouse_info.quantity >= int(warehouse_data[i]["quantity"]):
                        #subtract the quantity 
                        warehouse_info.quantity -=  int(warehouse_data[i]["quantity"])
                        warehouse_info.save()

                        new_report = inventory_report.objects.create (product_id=product_id, specification_id= specification_id, warehouse_id= warehouse_data[i]["warehouse_id"], debit= int(warehouse_data[i]["quantity"]), date=current_date)
                        new_report.save()

                        subtract_item = subtraction_track.objects.create(order_id = order_id, specification_id = specification_id, warehouse_id = warehouse_data[i]["warehouse_id"], debit_quantity= int(warehouse_data[i]["quantity"]),date=current_date)

                        subtract_item.save()

                    else:
                        return False

                else:
                    return False


        if len(shop_data) > 0:

            print(len(shop_data))

            for k in range(len(shop_data)):

                i = k 

                try:
                    shop_info = ShopInfo.objects.filter(specification_id=specification_id,shop_id=shop_data[i]["shop_id"]).last()
                except:
                    shop_info = None 

                if shop_info:
                    print("SHOP INFO")
                    print(shop_info)
                    if shop_info.quantity >= int(shop_data[i]["quantity"]):
                        print("quantity subtract hochchce")
                        #subtract the quantity 
                        shop_info.quantity -=  int(shop_data[i]["quantity"])
                        shop_info.save()
                        print("shop_info save hochche")

                        # new_report = inventory_report.objects.create (product_id=product_id, specification_id= specification_id, shop_id= shop_data[i]["warehouse_id"], credit= int(shop_data[i]["quantity"]))
                        # new_report.save()
                        # print("new_report save")

                        # subtract_item = subtraction_track.objects.create(order_id = order_id, specification_id = specification_id, shop_id = shop_data[i]["warehouse_id"], debit_quantity= int(shop_data[i]["quantity"]),date=current_date)

                        # subtract_item.save()
                        # print("subtract_item save")

                        new_report = inventory_report.objects.create (product_id=product_id, specification_id= specification_id, shop_id= shop_data[i]["shop_id"], debit= int(shop_data[i]["quantity"]), date=current_date)
                        new_report.save()

                        subtract_item = subtraction_track.objects.create(order_id = order_id, specification_id = specification_id, shop_id = shop_data[i]["shop_id"], debit_quantity= int(shop_data[i]["quantity"]),date=current_date)

                        subtract_item.save()

                    else:
                        print("ERRRORRRRRR")
                        return False

                else:
                    print("SECONDDDDDDDDDDDDDDDDDD")
                    return False

        return True

    except:
        return False



@api_view(["GET", "POST"])
def get_all_quantity_list_and_price(request, specification_id):

    if request.method == 'GET':


        purchase_price = 0 
        selling_price = 0 

        try:
            spec_price = SpecificationPrice.objects.filter(specification_id = specification_id,status="Single").last()
        except:
            spec_price = None


        if spec_price:
            purchase_price = spec_price.purchase_price
            selling_price = spec_price.mrp


        


        try:
            warehouse_values = []
            shop_values = []
            warehouse_ids = []
            shop_ids = []
            warehouse_query = WarehouseInfo.objects.filter(
                specification_id=specification_id)
            print(warehouse_query)
            wh_name = Warehouse.objects.all()
            print(wh_name)
            for wq in warehouse_query:
                print(wq.warehouse_id)
                warehouse_data = Warehouse.objects.get(id=wq.warehouse_id)
                wh_data = {"warehouse_id": warehouse_data.id, "previous_quantity": wq.quantity,
                           "warehouse_name": warehouse_data.warehouse_name}
                print(wh_data)
                warehouse_values.append(wh_data)
                warehouse_ids.append(wq.warehouse_id)

            print(warehouse_values)
            for warehouse in wh_name:
                if warehouse.id not in warehouse_ids:
                    wh_data = {"warehouse_id": warehouse.id, "previous_quantity": 0,
                               "warehouse_name": warehouse.warehouse_name}
                    warehouse_values.append(wh_data)

            print(warehouse_values)

            shopinfo_query = ShopInfo.objects.filter(
                specification_id=specification_id)
            all_shops = Shop.objects.all()
            print(shopinfo_query)
            print(all_shops)
            for shop in shopinfo_query:
                shop_data = Shop.objects.get(id=shop.shop_id)
                datas = {"shop_id": shop_data.id, "previous_quantity": shop.quantity,
                         "shop_name": shop_data.shop_name}
                shop_values.append(datas)
                shop_ids.append(shop.shop_id)

            for shops in all_shops:
                if shops.id not in shop_ids:
                    datas = {"shop_id": shops.id, "previous_quantity": 0,
                             "shop_name": shops.shop_name}
                    shop_values.append(datas)

            return JsonResponse({
                "success": True,
                "message": "Data has been retrieved successfully",
                "data": {
                    "warehouse": warehouse_values,
                    "shop": shop_values ,
                    "purchase_price": purchase_price,
                    "selling_price" : selling_price

                }
            })
        except:
            return JsonResponse({
                "success": False,
                "message": "Something went wrong"
            })


#Find warehouse id
def find_warehouse_id():

    try:
        warehouse = Warehouse.objects.filter(warehouse_name="Mothersite",warehouse_location="Mothersite").last()

    except:
        warehouse = None

    if warehouse:
        warehouse_id = warehouse.id
    else:
        warehouse_id = -1

    return warehouse_id


def fetch_selling_price(specification_id):
    try:
        p_price = ProductPrice.objects.get(specification_id=specification_id)
    except:
        p_price = None 

    if p_price:
        selling_price = p_price.price
    else:
        selling_price = 0

    return selling_price

