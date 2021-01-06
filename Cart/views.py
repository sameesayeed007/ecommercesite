from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
import datetime

from Intense.models import Product,TerminalUsers,Warehouse,MotherSpecificationPrice,Shop,BkashPaymentInfo,SpecificationPrice, product_delivery_area, subtraction_track, Terminal, Order, OrderDetails, ProductPrice, Userz, BillingAddress, ProductPoint, discount_product, ProductImpression, Profile, Cupons, ProductSpecification, PaymentInfo, CompanyInfo, OrderInfo, Invoice, WarehouseInfo, ShopInfo, inventory_report, DeliveryArea, DeliveryLocation, User

from Cart.serializers import ProductSerializer, PoSOrderSerializer, PoSInvoiceSerializer, PaymentInfoSerializer, OrderSerializer, OrderSerializer3, OrderInvoiceSerializer, OrderSerializerz, OrderSerializerzz, OrderDetailsSerializer, ProductPriceSerializer, UserzSerializer, BillingAddressSerializer, ProductPointSerializer, OrderInfoSerializer, InvoiceSerializer, SalesSerializer, PurchaseInvoiceSerializer, OrderDetailsSerializer1
from Product_details.serializers import ProductImpressionSerializer, ProductSpecificationSerializer
from Site_settings.serializers import CompanyInfoSerializer,CompanyInfoSerializer1
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from datetime import date
from .payment import paymentInformation
import requests
import json
from rest_framework.response import Response
from django.core.serializers.json import DjangoJSONEncoder
# from django.contrib.auth.models import User
own_site_path = "http://127.0.0.1:8000/"
site_path = "http://127.0.0.1:7000/"

# Create your views here.
@api_view(['PUT', ])
def add_cart(request, productid):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    quantity = request.data.get('quantity')
    color = request.data.get('color')
    size = request.data.get('size')
    #unit = request.data.get('unit')
    quantity = int(quantity)
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

        # Fetching the specific product info
    p_price = 0
    p_discount = 0
    p_point = 0
    total_price = 0
    total_point = 0
    p_name = ""
    unit_point = 0
    unit_price = 0
    # Fetching the product points
    try:
        product_point = ProductPoint.objects.filter(
            product_id=productid).last()
    except:
        product_point = None

    if product_point is not None:

        if product_point.point:
            p_point = product_point.point

        else:
            p_point = 0
        current_date = timezone.now().date()
        start_date = current_date
        end_date = current_date

        if product_point.start_date:
            start_date = product_point.start_date
        else:
            start_date = current_date

        if product_point.end_date:
            end_date = product_point.end_date

        else:
            end_date = current_date

        if (current_date >= start_date) and (current_date <= end_date):
            total_point = p_point * quantity
            unit_point = p_point

        else:
            total_point = 0
            unit_point = 0

    else:

        total_point = 0
        unit_point = 0

    # Fetching the product price
    try:

        product_price = ProductPrice.objects.filter(
            product_id=productid).last()
    except:
        product_price = None

    if product_price is not None:
        p_price = product_price.price
        unit_price = p_price
    else:
        p_price = 0
        unit_price = p_price

    # Fetching the product discount
    try:
        product_discount = discount_product.objects.filter(
            product_id=productid).last()
    except:
        product_discount = None

    if product_discount is not None:
        if product_discount.amount:
            p_discount = product_discount.amount
        else:
            p_discount = 0
        current_date = timezone.now().date()
        discount_start_date = current_date
        discount_end_date = current_date
        if product_discount.start_date:

            discount_start_date = product_discount.start_date
        else:
            discount_start_date = current_date

        if product_discount.end_date:
            discount_end_date = product_discount.end_date

        else:
            discount_end_date = current_date

        if (current_date >= discount_start_date) and (current_date <= discount_end_date):
            total_discount = p_discount * quantity
            total_price = (p_price * quantity) - total_discount
            unit_price = p_price - p_discount

        else:
            total_discount = 0
            total_price = (p_price * quantity) - total_discount
            unit_price = p_price
    else:
        total_price = p_price * quantity
        unit_price = p_price

    try:
        product_name = Product.objects.filter(id=productid).last()
    except:
        product_name = None

    if product_name is not None:

        p_name = str(product_name.title)
        p_id = product_name.id

    else:
        p_name = ""

    try:
        product_impression = ProductImpression.objects.filter(product_id=productid)[
            0:1].get()
    except:
        product_impression = None

    if product_impression is None:
        # Create a productimpression object for that particular product
        print("create impression")
        p_impression = ProductImpression.objects.create(product_id=productid)
        p_impression_serializer = ProductImpressionSerializer(
            p_impression, data=request.data)
        if p_impression_serializer.is_valid():
            p_impression_serializer.save()

    else:
        product_impression = ProductImpression.objects.filter(product_id=productid)[
            0:1].get()

    # Fetching the the specification id

    print("dfdfdfdfdffdfd")
    print(color)
    print(size)
    print(productid)
    print(quantity)

    try:

        product_spec = ProductSpecification.objects.get(
            product_id=productid, color=color, size=size)

    except:

        product_spec = None

    # print(product_spec)

    if product_spec:

        item_quantity = product_spec.quantity
        item_color = product_spec.color
        item_size = product_spec.size

        if item_quantity >= quantity:

            # then add to cart

            # Add yo cart
            if non_verified_user_id == 0:

                # checking if the user exists in product impression
                try:
                    product_impression = ProductImpression.objects.filter(product_id=productid)[
                        0:1].get()
                except:
                    product_impression = None

                if product_impression:
                    users_list = product_impression.users
                    cart_count = product_impression.cart_count
                    if user_id in users_list:
                        pass
                    else:
                        users_list.append(user_id)

                    cart = cart_count + quantity
                    ProductImpression.objects.filter(product_id=productid).update(
                        users=users_list, cart_count=cart)

                try:
                    # Fetching the specific order of the specific user that hasnt been checked out
                    specific_order = Order.objects.filter(
                        user_id=user_id, checkout_status=False)[0:1].get()
                    order_id = specific_order.id

                except:
                    specific_order = None

                # if the specific user order exists
                if specific_order is not None:

                    try:
                        # checking if the product exists in this order
                        specific_order_product = OrderDetails.objects.filter(
                            order_id=order_id, product_id=productid, is_removed=False, delivery_removed=False, product_color=color, product_size=size)[0:1].get()
                    except:
                        specific_order_product = None

                    orderserializers = OrderSerializer(
                        specific_order, data=request.data)

                    if orderserializers.is_valid():
                        orderserializers.save()

                    if specific_order_product is not None:

                        specific_order_product.total_quantity += quantity
                        specific_order_product.remaining += quantity
                        specific_order_product.total_price += total_price
                        specific_order_product.total_point += total_point
                        # specifc_order_product.product_color.append(color)
                        # specifc_order_product.product_size.append(size)
                        # specifc_order_product.product_unit.append(unit)
                        specific_order_product.save()
                        orderdetailsserializers = OrderDetailsSerializer(
                            specific_order_product, data=request.data)
                        if orderdetailsserializers.is_valid():
                            orderdetailsserializers.save()
                            return JsonResponse({'success': True, 'message': 'The quantity has been updated'})
                        else:
                            return JsonResponse(orderdetailsserializers.errors)

                    else:
                        # create a new orderdetail for that order id if the product is bough for the first time
                        # product_color = [color]
                        # product_size = [size]
                        # product_color = [unit]

                        orderdetails = OrderDetails.objects.create(order_id=order_id, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity,
                                                                   unit_price=unit_price, unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size)

                        orderdetails.save()
                        orderdetailsserializer = OrderDetailsSerializer(
                            orderdetails, data=request.data)
                        if orderdetailsserializer.is_valid():
                            orderdetailsserializer.save()
                            return JsonResponse({'success': True, 'message': 'The product has been added to your cart'})
                        else:
                            return JsonResponse(orderdetailsserializers.errors)

                # if no order for the user exists
                else:

                    # create a new Order
                    order = Order.objects.create(user_id=user_id)
                    order.save()
                    orderserializer = OrderSerializer(order, data=request.data)
                    if orderserializer.is_valid():
                        orderserializer.save()
                    else:
                        return JsonResponse(orderserializer.errors)

                    # create a new order details for the specific product for the specific order
                    orderdetails = OrderDetails.objects.create(order_id=order.id, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity,
                                                               unit_price=unit_price, unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size)

                    orderdetails.save()
                    orderdetailserializer = OrderDetailsSerializer(
                        orderdetails, data=request.data)
                    if orderdetailserializer.is_valid():
                        orderdetailserializer.save()
                        return JsonResponse({'success': True, 'message': 'A new order with a order details has been created'})
                    else:
                        return JsonResponse(orderdetailserializer.errors)

            else:

                # checking if the user exists in the impression user list
                try:
                    product_impression = ProductImpression.objects.filter(product_id=productid)[
                        0:1].get()
                except:
                    product_impression = None
                if product_impression:
                    users_list = product_impression.non_verified_user
                    cart_count = product_impression.cart_count
                    if non_verified_user_id in users_list:
                        pass
                    else:
                        users_list.append(non_verified_user_id)

                    cart = cart_count + quantity
                    ProductImpression.objects.filter(product_id=productid).update(
                        non_verified_user=users_list, cart_count=cart)

                try:
                    # Fetching the specific order of the specific user that hasnt been checked out
                    specific_order = Order.objects.filter(
                        non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()
                    order_id = specific_order.id

                except:
                    specific_order = None

                # if the specific user order exists
                if specific_order is not None:

                    try:
                        # checking if the product exists in this order
                        specific_order_product = OrderDetails.objects.filter(
                            order_id=order_id, product_id=productid, delivery_removed=False, is_removed=False, product_color=color, product_size=size)[0:1].get()
                    except:
                        specific_order_product = None

                    orderserializers = OrderSerializer(
                        specific_order, data=request.data)

                    if orderserializers.is_valid():
                        orderserializers.save()

                    if specific_order_product is not None:

                        specific_order_product.total_quantity += quantity
                        specific_order_product.remaining += quantity
                        specific_order_product.total_price += total_price
                        specific_order_product.total_point += total_point
                        specific_order_product.save()
                        orderdetailsserializers = OrderDetailsSerializer(
                            specific_order_product, data=request.data)
                        if orderdetailsserializers.is_valid():
                            orderdetailsserializers.save()
                            return JsonResponse({'success': True, 'message': 'The quantity has been updated'})
                        else:
                            return JsonResponse(orderdetailsserializers.errors)

                    else:
                        # create a new orderdetail for that order id if the product is bough for the first time
                        orderdetails = OrderDetails.objects.create(order_id=order_id, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity,
                                                                   unit_price=unit_price, unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size)

                        orderdetails.save()
                        orderdetailsserializer = OrderDetailsSerializer(
                            orderdetails, data=request.data)
                        if orderdetailsserializer.is_valid():
                            orderdetailsserializer.save()
                            return JsonResponse({'success': True, 'message': 'The product has been added to your cart'})
                        else:
                            return JsonResponse(orderdetailsserializers.errors)

                # if no order for the user exists
                else:

                    # create a new Order
                    order = Order.objects.create(
                        non_verified_user_id=non_verified_user_id)
                    order.save()
                    orderserializer = OrderSerializer(order, data=request.data)
                    if orderserializer.is_valid():
                        orderserializer.save()
                    else:
                        return JsonResponse(orderserializer.errors)

                    # create a new order details for the specific product for the specific order
                    orderdetails = OrderDetails.objects.create(order_id=order.id, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity,
                                                               unit_price=unit_price, unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size)

                    orderdetails.save()
                    orderdetailserializer = OrderDetailsSerializer(
                        orderdetails, data=request.data)
                    if orderdetailserializer.is_valid():
                        orderdetailserializer.save()
                        return JsonResponse({'success': True, 'message': 'A new order with a order details has been created'})
                    else:
                        return JsonResponse(orderdetailserializer.errors)

        else:

            message = "You cannot add to cart.We only have "+str(item_quantity)+" of item "+str(
                p_name)+" of color "+str(item_color)+" of size "+str(item_size)+" in our stock currently."

            return JsonResponse({'success': False, 'message': message})

    else:

        return JsonResponse({'success': False, 'message': 'This product does not exist'})


# # Create your views here.
# @api_view(['PUT', ])
# def add_cart1(request, specificationid):

#     user_id = request.data.get('user_id')
#     non_verified_user_id = request.data.get('non_verified_user_id')
#     quantity = int(request.data.get('quantity'))
#     print(quantity)
#     # color = request.data.get('color')
#     # size = request.data.get('size')
#     #unit = request.data.get('unit')
#     productid = request.data.get('product_id')
#     quantity = int(quantity)
#     if user_id is not None:
#         user_id = int(user_id)
#         non_verified_user_id = 0

#     else:
#         non_verified_user_id = int(non_verified_user_id)
#         user_id = 0

#         # Fetching the specific product info
#     p_price = 0
#     p_discount = 0
#     p_point = 0
#     total_price = 0
#     total_point = 0
#     p_name = ""
#     unit_point = 0
#     unit_price = 0
#     # Fetching the product points
#     try:
#         product_point = ProductPoint.objects.filter(
#             specification_id=specificationid).last()
#     except:
#         product_point = None

#     if product_point is not None:

#         if product_point.point:
#             p_point = product_point.point

#         else:
#             p_point = 0
#         current_date = timezone.now().date()
#         start_date = current_date
#         end_date = current_date

#         if product_point.start_date:
#             start_date = product_point.start_date
#         else:
#             start_date = current_date

#         if product_point.end_date:
#             end_date = product_point.end_date

#         else:
#             end_date = current_date

#         if (current_date >= start_date) and (current_date <= end_date):
#             total_point = p_point * quantity
#             unit_point = p_point

#         else:
#             total_point = 0
#             unit_point = 0

#     else:

#         total_point = 0
#         unit_point = 0

#     # Fetching the product price
#     try:

#         product_price = ProductPrice.objects.filter(
#             specification_id=specificationid).last()
#     except:
#         product_price = None

#     if product_price is not None:
#         p_price = product_price.price
#         unit_price = p_price
#     else:
#         p_price = 0
#         unit_price = p_price

#     # Fetching the product discount
#     try:
#         product_discount = discount_product.objects.filter(
#             specification_id=specificationid).last()
#     except:
#         product_discount = None

#     print(product_discount)

#     if product_discount:

#         if product_discount.discount_type == "amount":

#             print("amount")

#             if product_discount.amount:
#                 p_discount = product_discount.amount
#             else:
#                 p_discount = 0

#             print(p_discount)

#             current_date = timezone.now().date()
#             discount_start_date = current_date
#             discount_end_date = current_date
#             if product_discount.start_date:

#                 discount_start_date = product_discount.start_date
#             else:
#                 discount_start_date = current_date

#             if product_discount.end_date:
#                 discount_end_date = product_discount.end_date

#             else:
#                 discount_end_date = current_date

#             if (current_date >= discount_start_date) and (current_date <= discount_end_date):
#                 total_discount = p_discount * quantity
#                 total_price = (p_price * quantity) - total_discount
#                 unit_price = p_price - p_discount

#             else:
#                 total_discount = 0
#                 total_price = (p_price * quantity) - total_discount
#                 unit_price = p_price

#         elif product_discount.discount_type == "percentage":

#             print("percentage")

#             if product_discount.amount:
#                 p_discount = product_discount.amount
#                 p_discount = (p_discount * p_price)/100
#             else:
#                 p_discount = 0

#             current_date = timezone.now().date()
#             discount_start_date = current_date
#             discount_end_date = current_date
#             if product_discount.start_date:

#                 discount_start_date = product_discount.start_date
#             else:
#                 discount_start_date = current_date

#             if product_discount.end_date:
#                 discount_end_date = product_discount.end_date

#             else:
#                 discount_end_date = current_date

#             if (current_date >= discount_start_date) and (current_date <= discount_end_date):

#                 total_discount = p_discount * quantity
#                 total_price = (p_price * quantity) - total_discount
#                 unit_price = p_price - p_discount

#             else:
#                 total_discount = 0
#                 total_price = (p_price * quantity) - total_discount
#                 unit_price = p_price

#         else:
#             total_price = p_price * quantity
#             unit_price = p_price

#     else:
#         total_price = p_price * quantity
#         unit_price = p_price

#     try:
#         product_name = Product.objects.filter(id=productid).last()
#     except:
#         product_name = None

#     if product_name is not None:

#         p_name = str(product_name.title)
#         p_id = product_name.id

#     else:
#         p_name = ""

#     try:
#         product_impression = ProductImpression.objects.filter(product_id=productid)[
#             0:1].get()
#     except:
#         product_impression = None

#     if product_impression is None:
#         # Create a productimpression object for that particular product
#         print("create impression")
#         p_impression = ProductImpression.objects.create(product_id=productid)
#         p_impression_serializer = ProductImpressionSerializer(
#             p_impression, data=request.data)
#         if p_impression_serializer.is_valid():
#             p_impression_serializer.save()

#     else:
#         product_impression = ProductImpression.objects.filter(product_id=productid)[
#             0:1].get()

#     # Fetching the the specification id

#     # print("dfdfdfdfdffdfd")
#     # print(color)
#     # print(size)
#     # print(productid)
#     # print(quantity)

#     try:

#         product_spec = ProductSpecification.objects.get(id=specificationid)

#     except:

#         product_spec = None

#     # print(product_spec)

#     print(product_spec)

#     if product_spec:

#         item_quantity = product_spec.quantity
#         color = product_spec.color
#         size = product_spec.size
#         unit = product_spec.unit
#         weight = product_spec.weight

#         if item_quantity >= quantity:

#             # then add to cart

#             # Add yo cart
#             if non_verified_user_id == 0:

#                 # checking if the user exists in product impression
#                 try:
#                     product_impression = ProductImpression.objects.filter(product_id=productid)[
#                         0:1].get()
#                 except:
#                     product_impression = None

#                 if product_impression:
#                     users_list = product_impression.users
#                     cart_count = product_impression.cart_count
#                     if user_id in users_list:
#                         pass
#                     else:
#                         users_list.append(user_id)

#                     cart = cart_count + quantity
#                     ProductImpression.objects.filter(product_id=productid).update(
#                         users=users_list, cart_count=cart)

#                 try:
#                     # Fetching the specific order of the specific user that hasnt been checked out
#                     specific_order = Order.objects.filter(
#                         user_id=user_id, checkout_status=False)[0:1].get()
#                     order_id = specific_order.id

#                 except:
#                     specific_order = None

#                 # if the specific user order exists
#                 if specific_order is not None:

#                     try:
#                         # checking if the product exists in this order
#                         specific_order_product = OrderDetails.objects.filter(
#                             order_id=order_id, specification_id=specificationid, product_id=productid, is_removed=False, delivery_removed=False)[0:1].get()
#                     except:
#                         specific_order_product = None

#                     orderserializers = OrderSerializer(
#                         specific_order, data=request.data)

#                     if orderserializers.is_valid():
#                         orderserializers.save()

#                     if specific_order_product is not None:

#                         specific_order_product.total_quantity += quantity
#                         specific_order_product.remaining += quantity
#                         specific_order_product.total_price += total_price
#                         specific_order_product.total_point += total_point
#                         # specifc_order_product.product_color.append(color)
#                         # specifc_order_product.product_size.append(size)
#                         # specifc_order_product.product_unit.append(unit)
#                         specific_order_product.save()
#                         orderdetailsserializers = OrderDetailsSerializer(
#                             specific_order_product, data=request.data)
#                         if orderdetailsserializers.is_valid():
#                             orderdetailsserializers.save()
#                             return JsonResponse({'success': True, 'message': 'The quantity has been updated'})
#                         else:
#                             return JsonResponse(orderdetailsserializers.errors)

#                     else:
#                         # create a new orderdetail for that order id if the product is bough for the first time
#                         # product_color = [color]
#                         # product_size = [size]
#                         # product_color = [unit]

#                         orderdetails = OrderDetails.objects.create(order_id=order_id, specification_id=specificationid, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity, unit_price=unit_price,
#                                                                    unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size, product_unit=unit, product_weight=weight)

#                         orderdetails.save()
#                         orderdetailsserializer = OrderDetailsSerializer(
#                             orderdetails, data=request.data)
#                         if orderdetailsserializer.is_valid():
#                             orderdetailsserializer.save()
#                             return JsonResponse({'success': True, 'message': 'The product has been added to your cart'})
#                         else:
#                             return JsonResponse(orderdetailsserializers.errors)

#                 # if no order for the user exists
#                 else:

#                     # create a new Order
#                     order = Order.objects.create(user_id=user_id)
#                     order.save()
#                     orderserializer = OrderSerializer(order, data=request.data)
#                     if orderserializer.is_valid():
#                         orderserializer.save()
#                     else:
#                         return JsonResponse(orderserializer.errors)

#                     # create a new order details for the specific product for the specific order
#                     orderdetails = OrderDetails.objects.create(order_id=order.id, specification_id=specificationid, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity, unit_price=unit_price,
#                                                                unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size, product_weight=weight, product_unit=unit)

#                     orderdetails.save()
#                     orderdetailserializer = OrderDetailsSerializer(
#                         orderdetails, data=request.data)
#                     if orderdetailserializer.is_valid():
#                         orderdetailserializer.save()
#                         return JsonResponse({'success': True, 'message': 'A new order with a order details has been created'})
#                     else:
#                         return JsonResponse(orderdetailserializer.errors)

#             else:

#                 # checking if the user exists in the impression user list
#                 try:
#                     product_impression = ProductImpression.objects.filter(product_id=productid)[
#                         0:1].get()
#                 except:
#                     product_impression = None
#                 if product_impression:
#                     users_list = product_impression.non_verified_user
#                     cart_count = product_impression.cart_count
#                     if non_verified_user_id in users_list:
#                         pass
#                     else:
#                         users_list.append(non_verified_user_id)

#                     cart = cart_count + quantity
#                     ProductImpression.objects.filter(product_id=productid).update(
#                         non_verified_user=users_list, cart_count=cart)

#                 try:
#                     # Fetching the specific order of the specific user that hasnt been checked out
#                     specific_order = Order.objects.filter(
#                         non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()
#                     order_id = specific_order.id

#                 except:
#                     specific_order = None

#                 # if the specific user order exists
#                 if specific_order is not None:

#                     try:
#                         # checking if the product exists in this order
#                         specific_order_product = OrderDetails.objects.filter(
#                             order_id=order_id, product_id=productid, is_removed=False, delivery_removed=False, specification_id=specificationid)[0:1].get()
#                     except:
#                         specific_order_product = None

#                     orderserializers = OrderSerializer(
#                         specific_order, data=request.data)

#                     if orderserializers.is_valid():
#                         orderserializers.save()

#                     if specific_order_product is not None:

#                         specific_order_product.total_quantity += quantity
#                         specific_order_product.remaining += quantity
#                         specific_order_product.total_price += total_price
#                         specific_order_product.total_point += total_point
#                         specific_order_product.save()
#                         orderdetailsserializers = OrderDetailsSerializer(
#                             specific_order_product, data=request.data)
#                         if orderdetailsserializers.is_valid():
#                             orderdetailsserializers.save()
#                             return JsonResponse({'success': True, 'message': 'The quantity has been updated'})
#                         else:
#                             return JsonResponse(orderdetailsserializers.errors)

#                     else:
#                         # create a new orderdetail for that order id if the product is bough for the first time
#                         orderdetails = OrderDetails.objects.create(order_id=order_id, specification_id=specificationid, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity, unit_price=unit_price,
#                                                                    unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size, product_weight=weight, product_unit=unit)

#                         orderdetails.save()
#                         orderdetailsserializer = OrderDetailsSerializer(
#                             orderdetails, data=request.data)
#                         if orderdetailsserializer.is_valid():
#                             orderdetailsserializer.save()
#                             return JsonResponse({'success': True, 'message': 'The product has been added to your cart'})
#                         else:
#                             return JsonResponse(orderdetailsserializers.errors)

#                 # if no order for the user exists
#                 else:

#                     # create a new Order
#                     order = Order.objects.create(
#                         non_verified_user_id=non_verified_user_id)
#                     order.save()
#                     orderserializer = OrderSerializer(order, data=request.data)
#                     if orderserializer.is_valid():
#                         orderserializer.save()
#                     else:
#                         return JsonResponse(orderserializer.errors)

#                     # create a new order details for the specific product for the specific order
#                     orderdetails = OrderDetails.objects.create(order_id=order.id, specification_id=specificationid, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity, unit_price=unit_price,
#                                                                unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size, product_unit=unit, product_weight=weight)

#                     orderdetails.save()
#                     orderdetailserializer = OrderDetailsSerializer(
#                         orderdetails, data=request.data)
#                     if orderdetailserializer.is_valid():
#                         orderdetailserializer.save()
#                         return JsonResponse({'success': True, 'message': 'A new order with a order details has been created'})
#                     else:
#                         return JsonResponse(orderdetailserializer.errors)

#         else:

#             message = "You cannot add to cart.We only have "+str(item_quantity)+" of item "+str(
#                 p_name)+" of color "+str(color)+" of size "+str(size)+" in our stock currently."

#             return JsonResponse({'success': False, 'message': message})

#     else:

#         return JsonResponse({'success': False, 'message': 'This product does not exist'})



# Create your views here.
@api_view(['PUT', ])
def add_cart1(request, specificationid):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    quantity = int(request.data.get('quantity'))
    print(quantity)
    # color = request.data.get('color')
    # size = request.data.get('size')
    #unit = request.data.get('unit')
    productid = request.data.get('product_id')
    quantity = int(quantity)
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

        # Fetching the specific product info
    p_price = 0
    p_discount = 0
    p_point = 0
    total_price = 0
    total_point = 0
    p_name = ""
    unit_point = 0
    unit_price = 0
    # Fetching the product points
    try:
        product_point = ProductPoint.objects.filter(
            specification_id=specificationid).last()
    except:
        product_point = None

    if product_point is not None:

        if product_point.point:
            p_point = product_point.point

        else:
            p_point = 0
        current_date = timezone.now().date()
        start_date = current_date
        end_date = current_date

        if product_point.start_date:
            start_date = product_point.start_date
        else:
            start_date = current_date

        if product_point.end_date:
            end_date = product_point.end_date

        else:
            end_date = current_date

        if (current_date >= start_date) and (current_date <= end_date):
            total_point = p_point * quantity
            unit_point = p_point

        else:
            total_point = 0
            unit_point = 0

    else:

        total_point = 0
        unit_point = 0

    # Fetching the product price
    try:

        product_price = ProductPrice.objects.filter(
            specification_id=specificationid).last()
    except:
        product_price = None

    if product_price is not None:
        p_price = product_price.price
        unit_price = p_price
    else:
        p_price = 0
        unit_price = p_price

    # Fetching the product discount
    try:
        product_discount = discount_product.objects.filter(
            specification_id=specificationid).last()
    except:
        product_discount = None

    print(product_discount)

    if product_discount:

        if product_discount.discount_type == "amount":

            print("amount")

            if product_discount.amount:
                p_discount = product_discount.amount
            else:
                p_discount = 0

            print(p_discount)

            current_date = timezone.now().date()
            discount_start_date = current_date
            discount_end_date = current_date
            if product_discount.start_date:

                discount_start_date = product_discount.start_date
            else:
                discount_start_date = current_date

            if product_discount.end_date:
                discount_end_date = product_discount.end_date

            else:
                discount_end_date = current_date

            if (current_date >= discount_start_date) and (current_date <= discount_end_date):
                total_discount = p_discount * quantity
                total_price = (p_price * quantity) - total_discount
                unit_price = p_price - p_discount

            else:
                total_discount = 0
                total_price = (p_price * quantity) - total_discount
                unit_price = p_price

        elif product_discount.discount_type == "percentage":

            print("percentage")

            if product_discount.amount:
                p_discount = product_discount.amount
                p_discount = (p_discount * p_price)/100
            else:
                p_discount = 0

            current_date = timezone.now().date()
            discount_start_date = current_date
            discount_end_date = current_date
            if product_discount.start_date:

                discount_start_date = product_discount.start_date
            else:
                discount_start_date = current_date

            if product_discount.end_date:
                discount_end_date = product_discount.end_date

            else:
                discount_end_date = current_date

            if (current_date >= discount_start_date) and (current_date <= discount_end_date):

                total_discount = p_discount * quantity
                total_price = (p_price * quantity) - total_discount
                unit_price = p_price - p_discount

            else:
                total_discount = 0
                total_price = (p_price * quantity) - total_discount
                unit_price = p_price

        else:
            total_price = p_price * quantity
            unit_price = p_price

    else:
        total_price = p_price * quantity
        unit_price = p_price

    try:
        product_name = Product.objects.filter(id=productid).last()
    except:
        product_name = None

    if product_name is not None:

        p_name = str(product_name.title)
        p_id = product_name.id

    else:
        p_name = ""

    try:
        product_impression = ProductImpression.objects.filter(product_id=productid)[
            0:1].get()
    except:
        product_impression = None

    if product_impression is None:
        # Create a productimpression object for that particular product
        print("create impression")
        p_impression = ProductImpression.objects.create(product_id=productid)
        p_impression_serializer = ProductImpressionSerializer(
            p_impression, data=request.data)
        if p_impression_serializer.is_valid():
            p_impression_serializer.save()

    else:
        product_impression = ProductImpression.objects.filter(product_id=productid)[
            0:1].get()

    # Fetching the the specification id

    # print("dfdfdfdfdffdfd")
    # print(color)
    # print(size)
    # print(productid)
    # print(quantity)

    try:

        product_spec = ProductSpecification.objects.get(id=specificationid)

    except:

        product_spec = None

    # print(product_spec)

    print(product_spec)

    if product_spec:

        item_quantity = 0 

        if product_spec.is_own == True:
            item_quantity = product_spec.quantity
        else:
            url = own_site_path + "productdetails/not_own_quantity_check/" +str(specificationid)+ "/"
            own_response = requests.get(url = url)
            own_response = own_response.json()
            print(own_response)
            if own_response["success"] == True:
                #update the quantity
                item_quantity = own_response["quantity"]

            else:
                item_quantity = 0
                

        #item_quantity = product_spec.quantity
        own = product_spec.is_own
        color = product_spec.color
        size = product_spec.size
        unit = product_spec.unit
        weight = product_spec.weight

        if item_quantity >= quantity:

            # then add to cart

            # Add yo cart
            if non_verified_user_id == 0:

                # checking if the user exists in product impression
                try:
                    product_impression = ProductImpression.objects.filter(product_id=productid)[
                        0:1].get()
                except:
                    product_impression = None

                if product_impression:
                    users_list = product_impression.users
                    cart_count = product_impression.cart_count
                    if user_id in users_list:
                        pass
                    else:
                        users_list.append(user_id)

                    cart = cart_count + quantity
                    ProductImpression.objects.filter(product_id=productid).update(
                        users=users_list, cart_count=cart)

                try:
                    # Fetching the specific order of the specific user that hasnt been checked out
                    specific_order = Order.objects.filter(
                        user_id=user_id, checkout_status=False)[0:1].get()
                    order_id = specific_order.id

                except:
                    specific_order = None

                # if the specific user order exists
                if specific_order is not None:

                    try:
                        # checking if the product exists in this order
                        specific_order_product = OrderDetails.objects.filter(
                            order_id=order_id, specification_id=specificationid, product_id=productid, is_removed=False, delivery_removed=False)[0:1].get()
                    except:
                        specific_order_product = None

                    orderserializers = OrderSerializer(
                        specific_order, data=request.data)

                    if orderserializers.is_valid():
                        orderserializers.save()

                    if specific_order_product is not None:

                        specific_order_product.total_quantity += quantity
                        specific_order_product.remaining += quantity
                        specific_order_product.total_price += total_price
                        specific_order_product.total_point += total_point
                        # specifc_order_product.product_color.append(color)
                        # specifc_order_product.product_size.append(size)
                        # specifc_order_product.product_unit.append(unit)
                        specific_order_product.save()
                        orderdetailsserializers = OrderDetailsSerializer(
                            specific_order_product, data=request.data)
                        if orderdetailsserializers.is_valid():
                            orderdetailsserializers.save()
                            return JsonResponse({'success': True, 'message': 'The quantity has been updated'})
                        else:
                            return JsonResponse(orderdetailsserializers.errors)

                    else:
                        # create a new orderdetail for that order id if the product is bough for the first time
                        # product_color = [color]
                        # product_size = [size]
                        # product_color = [unit]

                        orderdetails = OrderDetails.objects.create(order_id=order_id, specification_id=specificationid, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity, unit_price=unit_price,
                                                                   unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size, product_unit=unit, product_weight=weight,is_own=own)

                        orderdetails.save()
                        orderdetailsserializer = OrderDetailsSerializer(
                            orderdetails, data=request.data)
                        if orderdetailsserializer.is_valid():
                            orderdetailsserializer.save()
                            return JsonResponse({'success': True, 'message': 'The product has been added to your cart'})
                        else:
                            return JsonResponse(orderdetailsserializers.errors)

                # if no order for the user exists
                else:

                    # create a new Order
                    order = Order.objects.create(user_id=user_id)
                    order.save()
                    orderserializer = OrderSerializer(order, data=request.data)
                    if orderserializer.is_valid():
                        orderserializer.save()
                    else:
                        return JsonResponse(orderserializer.errors)

                    # create a new order details for the specific product for the specific order
                    orderdetails = OrderDetails.objects.create(order_id=order.id, specification_id=specificationid, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity, unit_price=unit_price,
                                                               unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size, product_weight=weight, product_unit=unit,is_own=own)

                    orderdetails.save()
                    orderdetailserializer = OrderDetailsSerializer(
                        orderdetails, data=request.data)
                    if orderdetailserializer.is_valid():
                        orderdetailserializer.save()
                        return JsonResponse({'success': True, 'message': 'A new order with a order details has been created'})
                    else:
                        return JsonResponse(orderdetailserializer.errors)

            else:

                # checking if the user exists in the impression user list
                try:
                    product_impression = ProductImpression.objects.filter(product_id=productid)[
                        0:1].get()
                except:
                    product_impression = None
                if product_impression:
                    users_list = product_impression.non_verified_user
                    cart_count = product_impression.cart_count
                    if non_verified_user_id in users_list:
                        pass
                    else:
                        users_list.append(non_verified_user_id)

                    cart = cart_count + quantity
                    ProductImpression.objects.filter(product_id=productid).update(
                        non_verified_user=users_list, cart_count=cart)

                try:
                    # Fetching the specific order of the specific user that hasnt been checked out
                    specific_order = Order.objects.filter(
                        non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()
                    order_id = specific_order.id

                except:
                    specific_order = None

                # if the specific user order exists
                if specific_order is not None:

                    try:
                        # checking if the product exists in this order
                        specific_order_product = OrderDetails.objects.filter(
                            order_id=order_id, product_id=productid, is_removed=False, delivery_removed=False, specification_id=specificationid)[0:1].get()
                    except:
                        specific_order_product = None

                    orderserializers = OrderSerializer(
                        specific_order, data=request.data)

                    if orderserializers.is_valid():
                        orderserializers.save()

                    if specific_order_product is not None:

                        specific_order_product.total_quantity += quantity
                        specific_order_product.remaining += quantity
                        specific_order_product.total_price += total_price
                        specific_order_product.total_point += total_point
                        specific_order_product.save()
                        orderdetailsserializers = OrderDetailsSerializer(
                            specific_order_product, data=request.data)
                        if orderdetailsserializers.is_valid():
                            orderdetailsserializers.save()
                            return JsonResponse({'success': True, 'message': 'The quantity has been updated'})
                        else:
                            return JsonResponse(orderdetailsserializers.errors)

                    else:
                        # create a new orderdetail for that order id if the product is bough for the first time
                        orderdetails = OrderDetails.objects.create(order_id=order_id, specification_id=specificationid, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity, unit_price=unit_price,
                                                                   unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size, product_weight=weight, product_unit=unit,is_own=own)

                        orderdetails.save()
                        orderdetailsserializer = OrderDetailsSerializer(
                            orderdetails, data=request.data)
                        if orderdetailsserializer.is_valid():
                            orderdetailsserializer.save()
                            return JsonResponse({'success': True, 'message': 'The product has been added to your cart'})
                        else:
                            return JsonResponse(orderdetailsserializers.errors)

                # if no order for the user exists
                else:

                    # create a new Order
                    order = Order.objects.create(
                        non_verified_user_id=non_verified_user_id)
                    order.save()
                    orderserializer = OrderSerializer(order, data=request.data)
                    if orderserializer.is_valid():
                        orderserializer.save()
                    else:
                        return JsonResponse(orderserializer.errors)

                    # create a new order details for the specific product for the specific order
                    orderdetails = OrderDetails.objects.create(order_id=order.id, specification_id=specificationid, product_id=productid, quantity=quantity, total_quantity=quantity, remaining=quantity, unit_price=unit_price,
                                                               unit_point=unit_point, total_price=total_price, total_point=total_point, product_name=p_name, product_color=color, product_size=size, product_unit=unit, product_weight=weight,is_own=own)

                    orderdetails.save()
                    orderdetailserializer = OrderDetailsSerializer(
                        orderdetails, data=request.data)
                    if orderdetailserializer.is_valid():
                        orderdetailserializer.save()
                        return JsonResponse({'success': True, 'message': 'A new order with a order details has been created'})
                    else:
                        return JsonResponse(orderdetailserializer.errors)

        else:

            message = "You cannot add to cart.We only have "+str(item_quantity)+" of item "+str(
                p_name)+" of color "+str(color)+" of size "+str(size)+" in our stock currently."

            return JsonResponse({'success': False, 'message': message})

    else:

        return JsonResponse({'success': False, 'message': 'This product does not exist'})



@api_view(['PUT', ])
def increase_quantity(request, productid):

    #values = {'user_id':'2', 'non_verified_user_id':''}
    color = request.data.get('color')
    size = request.data.get('size')
    #unit = request.data.get('unit')
    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    #quantity = request.data.get('quantity')
    #quantity = int(quantity)
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    p_price = 0
    p_discount = 0
    p_point = 0
    total_price = 0
    total_point = 0
    p_name = ""
    unit_point = 0
    unit_price = 0
    quantity = 1
    # Fetching the product points
    try:
        product_point = ProductPoint.objects.filter(
            product_id=productid).last()
    except:
        product_point = None

    if product_point is not None:
        p_point = product_point.point
        start_date = product_point.start_date
        end_date = product_point.end_date
        current_date = timezone.now().date()

        if product_point.start_date:
            start_date = product_point.start_date
        else:
            start_date = current_date

        if product_point.end_date:
            end_date = product_point.end_date

        else:

            end_date = current_date

        if (current_date >= start_date) and (current_date <= end_date):
            total_point = p_point * quantity
            unit_point = p_point

        else:
            total_point = 0
            unit_point = 0

    else:

        total_point = 0
        unit_point = 0

    # Fetching the product price
    try:

        product_price = ProductPrice.objects.filter(
            product_id=productid).last()
    except:
        product_price = None

    if product_price is not None:
        p_price = product_price.price
        unit_price = p_price
    else:
        p_price = 0
        unit_price = p_price

    # Fetching the product discount
    try:
        product_discount = discount_product.objects.filter(
            product_id=productid).last()
    except:
        product_discount = None

    if product_discount is not None:
        p_discount = product_discount.amount
        discount_start_date = product_discount.start_date
        discount_end_date = product_discount.end_date
        current_date = timezone.now().date()

        if product_discount.start_date:
            discount_start_date = product_discount.start_date
        else:
            discount_start_date = current_date

        if product_discount.end_date:
            discount_end_date = product_discount.end_date

        else:

            discount_end_date = current_date

        if (current_date >= discount_start_date) and (current_date <= discount_end_date):
            total_discount = p_discount * quantity
            total_price = (p_price * quantity) - total_discount
            unit_price = p_price - p_discount

        else:
            total_discount = 0
            total_price = (p_price * quantity) - total_discount
            unit_price = p_price
    else:
        total_price = p_price * quantity
        unit_price = p_price

    try:
        product_name = Product.objects.filter(id=productid).last()
    except:
        product_name = None

    if product_name is not None:

        p_name = str(product_name.title)
        p_id = product_name.id

    else:
        p_name = ""

    # user_id = values['user_id']
    # non_verified_user_id = values['non_verified_user_id']
    cart_count = 0

    try:
        product_impression = ProductImpression.objects.filter(product_id=productid)[
            0:1].get()
    except:
        product_impression = None

    if product_impression is None:
        pass
    else:

        cart_count = product_impression.cart_count

    cart = cart_count + 1
    ProductImpression.objects.filter(
        product_id=productid).update(cart_count=cart)

    if non_verified_user_id == 0:

        try:
            # Fetching the specific order of the specific user that hasnt been checked out
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=False)[0:1].get()
            order_id = specific_order.id
        except:
            specific_order = None

        # if the specific user exists
        if specific_order is not None:

            try:
                # checking if the product exists in this order
                specific_order_product = OrderDetails.objects.filter(
                    order_id=order_id, product_id=productid, is_removed=False, delivery_removed=False, product_color=color, product_size=size)[0:1].get()

            except:
                specific_order_product = None

            if specific_order_product is not None:

                if specific_order_product.total_quantity >= 1:
                    specific_order_product.total_quantity += 1
                    specific_order_product.remaining += 1
                    specific_order_product.total_price += total_price
                    specific_order_product.total_point += total_point
                    specific_order_product.save()
                    orderdetailsserializers = OrderDetailsSerializer(
                        specific_order_product, data=request.data)
                    if orderdetailsserializers.is_valid():
                        orderdetailsserializers.save()
                        return JsonResponse({'success': True, 'message': 'The quantity has been increased'})

            else:
                return JsonResponse({'success': False, 'message': 'The item does not exist'})

        else:
            return JsonResponse({'success': False, 'message': 'The order does not exist'})

    else:

        try:
            # Fetching the specific order of the specific user that hasnt been checked out
            specific_order = Order.objects.filter(
                non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()
            order_id = specific_order.id
        except:
            specific_order = None

        # if the specific user exists
        if specific_order is not None:

            try:
                # checking if the product exists in this order
                specific_order_product = OrderDetails.objects.filter(
                    order_id=order_id, product_id=productid, is_removed=False, delivery_removed=False, product_color=color, product_size=size)[0:1].get()

            except:
                specific_order_product = None

            if specific_order_product is not None:

                if specific_order_product.total_quantity >= 1:
                    specific_order_product.total_quantity += 1
                    specific_order_product.remaining += 1
                    specific_order_product.total_price += total_price
                    specific_order_product.total_point += total_point
                    specific_order_product.save()
                    orderdetailsserializers = OrderDetailsSerializer(
                        specific_order_product, data=request.data)
                    if orderdetailsserializers.is_valid():
                        orderdetailsserializers.save()

                        return JsonResponse({'success': True, 'message': 'The quantity has been increased'})

            else:
                return JsonResponse({'success': False, 'message': 'The item does not exist'})

        else:
            return JsonResponse({'success': False, 'message': 'The order does not exist'})


@api_view(['PUT', ])
def increase_quantity1(request, specificationid):

    #values = {'user_id':'2', 'non_verified_user_id':''}
    # color = request.data.get('color')
    # size = request.data.get('size')
    try:
        spec_prod = ProductSpecification.objects.get(id=specificationid)
    except:
        spec_prod = None 
    if spec_prod:

        if spec_prod == True:
            item_quantity = spec_prod.quantity
        else:
            url = own_site_path + "productdetails/not_own_quantity_check/" +str(specificationid)+ "/"
            own_response = requests.get(url = url)
            own_response = own_response.json()
            print(own_response)
            if own_response["success"] == True:
                #update the quantity
                item_quantity = own_response["quantity"]

            else:
                item_quantity = 0

    
    else:
        return JsonResponse({"success":False , "message":"The product does not exist"})
    
    if item_quantity > 0:
        productid = request.data.get('product_id')
        user_id = request.data.get('user_id')
        non_verified_user_id = request.data.get('non_verified_user_id')
        #quantity = request.data.get('quantity')
        #quantity = int(quantity)
        if user_id is not None:
            user_id = int(user_id)
            non_verified_user_id = 0

        else:
            non_verified_user_id = int(non_verified_user_id)
            user_id = 0

        p_price = 0
        p_discount = 0
        p_point = 0
        total_price = 0
        total_point = 0
        p_name = ""
        unit_point = 0
        unit_price = 0
        quantity = 1
        # Fetching the product points
        try:
            product_point = ProductPoint.objects.filter(
                specification_id=specificationid).last()
        except:
            product_point = None

        if product_point is not None:

            if product_point.point:
                p_point = product_point.point

            else:
                p_point = 0
            current_date = timezone.now().date()
            start_date = current_date
            end_date = current_date

            if product_point.start_date:
                start_date = product_point.start_date
            else:
                start_date = current_date

            if product_point.end_date:
                end_date = product_point.end_date

            else:
                end_date = current_date

            if (current_date >= start_date) and (current_date <= end_date):
                total_point = p_point * quantity
                unit_point = p_point

            else:
                total_point = 0
                unit_point = 0

        else:

            total_point = 0
            unit_point = 0

        # Fetching the product price
        try:

            product_price = ProductPrice.objects.filter(
                specification_id=specificationid).last()
        except:
            product_price = None

        if product_price is not None:
            p_price = product_price.price
            unit_price = p_price
        else:
            p_price = 0
            unit_price = p_price

        # Fetching the product discount
        try:
            product_discount = discount_product.objects.filter(
                specification_id=specificationid).last()
        except:
            product_discount = None

        if product_discount is not None:

            if product_discount.discount_type == "amount":

                if product_discount.amount:
                    p_discount = product_discount.amount
                else:
                    p_discount = 0

                current_date = timezone.now().date()
                discount_start_date = current_date
                discount_end_date = current_date
                if product_discount.start_date:

                    discount_start_date = product_discount.start_date
                else:
                    discount_start_date = current_date

                if product_discount.end_date:
                    discount_end_date = product_discount.end_date

                else:
                    discount_end_date = current_date

                if (current_date >= discount_start_date) and (current_date <= discount_end_date):
                    total_discount = p_discount * quantity
                    total_price = (p_price * quantity) - total_discount
                    unit_price = p_price - p_discount

                else:
                    total_discount = 0
                    total_price = (p_price * quantity) - total_discount
                    unit_price = p_price

            elif product_discount.discount_type == "percentage":

                if product_discount.amount:
                    p_discount = product_discount.amount
                    p_discount = (p_discount * p_price)/100
                else:
                    p_discount = 0

                current_date = timezone.now().date()
                discount_start_date = current_date
                discount_end_date = current_date
                if product_discount.start_date:

                    discount_start_date = product_discount.start_date
                else:
                    discount_start_date = current_date

                if product_discount.end_date:
                    discount_end_date = product_discount.end_date

                else:
                    discount_end_date = current_date

                if (current_date >= discount_start_date) and (current_date <= discount_end_date):

                    total_discount = p_discount * quantity
                    total_price = (p_price * quantity) - total_discount
                    unit_price = p_price - p_discount

                else:
                    total_discount = 0
                    total_price = (p_price * quantity) - total_discount
                    unit_price = p_price

            else:
                total_price = p_price * quantity
                unit_price = p_price

        else:
            total_price = p_price * quantity
            unit_price = p_price

        try:
            product_name = Product.objects.filter(id=productid).last()
        except:
            product_name = None

        if product_name is not None:

            p_name = str(product_name.title)
            p_id = product_name.id

        else:
            p_name = ""

        # user_id = values['user_id']
        # non_verified_user_id = values['non_verified_user_id']
        cart_count = 0

        try:
            product_impression = ProductImpression.objects.filter(product_id=productid)[
                0:1].get()
        except:
            product_impression = None

        if product_impression is None:
            pass
        else:

            cart_count = product_impression.cart_count

        cart = cart_count + 1
        ProductImpression.objects.filter(
            product_id=productid).update(cart_count=cart)

        try:

            product_spec = ProductSpecification.objects.get(id=specificationid)

        except:

            product_spec = None

        # print(product_spec)

        print(product_spec)

        if product_spec:

            item_quantity = product_spec.quantity
            color = product_spec.color
            size = product_spec.size
            unit = product_spec.unit
            weight = product_spec.weight

            if item_quantity >= quantity:

                if non_verified_user_id == 0:

                    try:
                        # Fetching the specific order of the specific user that hasnt been checked out
                        specific_order = Order.objects.filter(
                            user_id=user_id, checkout_status=False)[0:1].get()
                        order_id = specific_order.id
                    except:
                        specific_order = None

                    # if the specific user exists
                    if specific_order is not None:

                        try:
                            # checking if the product exists in this order
                            specific_order_product = OrderDetails.objects.filter(
                                order_id=order_id, product_id=productid, is_removed=False, delivery_removed=False, specification_id=specificationid)[0:1].get()

                        except:
                            specific_order_product = None

                        if specific_order_product is not None:

                            if specific_order_product.total_quantity >= 1:
                                specific_order_product.total_quantity += 1
                                specific_order_product.remaining += 1
                                specific_order_product.total_price += total_price
                                specific_order_product.total_point += total_point
                                specific_order_product.save()
                                orderdetailsserializers = OrderDetailsSerializer(
                                    specific_order_product, data=request.data)
                                if orderdetailsserializers.is_valid():
                                    orderdetailsserializers.save()
                                    return JsonResponse({'success': True, 'message': 'The quantity has been increased'})

                        else:
                            return JsonResponse({'success': False, 'message': 'The item does not exist'})

                    else:
                        return JsonResponse({'success': False, 'message': 'The order does not exist'})

                else:

                    try:
                        # Fetching the specific order of the specific user that hasnt been checked out
                        specific_order = Order.objects.filter(
                            non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()
                        order_id = specific_order.id
                    except:
                        specific_order = None

                    # if the specific user exists
                    if specific_order is not None:

                        try:
                            # checking if the product exists in this order
                            specific_order_product = OrderDetails.objects.filter(
                                order_id=order_id, product_id=productid, delivery_removed=False, is_removed=False, specification_id=specificationid)[0:1].get()

                        except:
                            specific_order_product = None

                        if specific_order_product is not None:

                            if specific_order_product.total_quantity >= 1:
                                specific_order_product.total_quantity += 1
                                specific_order_product.remaining += 1
                                specific_order_product.total_price += total_price
                                specific_order_product.total_point += total_point
                                specific_order_product.save()
                                orderdetailsserializers = OrderDetailsSerializer(
                                    specific_order_product, data=request.data)
                                if orderdetailsserializers.is_valid():
                                    orderdetailsserializers.save()

                                    return JsonResponse({'success': True, 'message': 'The quantity has been increased'})

                        else:
                            return JsonResponse({'success': False, 'message': 'The item does not exist'})

                    else:
                        return JsonResponse({'success': False, 'message': 'The order does not exist'})

            else:

                message = "You cannot add to cart.We only have "+str(item_quantity)+" of item "+str(
                    p_name)+" of color "+str(color)+" of size "+str(size)+" in our stock currently."

                return JsonResponse({'success': False, 'message': message})

        else:

            return JsonResponse({'success': False, 'message': 'This product does not exist'})

    else:
        return JsonResponse({"success": False , "message": "There is no more of this product"})

@api_view(['PUT', ])
def decrease_quantity1(request, specificationid):

    #values = {'user_id':'2', 'non_verified_user_id':''}
    # color = request.data.get('color')
    productid = request.data.get('product_id')
    #unit = request.data.get('unit')
    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    #quantity = request.data.get('quantity')
    #quantity = int(quantity)
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    p_price = 0
    p_discount = 0
    p_point = 0
    total_price = 0
    total_point = 0
    p_name = ""
    unit_point = 0
    unit_price = 0
    quantity = 1
    # Fetching the product points
    try:
        product_point = ProductPoint.objects.filter(
            specification_id=specificationid).last()
    except:
        product_point = None

    if product_point is not None:

        if product_point.point:
            p_point = product_point.point

        else:
            p_point = 0
        current_date = timezone.now().date()
        start_date = current_date
        end_date = current_date

        if product_point.start_date:
            start_date = product_point.start_date
        else:
            start_date = current_date

        if product_point.end_date:
            end_date = product_point.end_date

        else:
            end_date = current_date

        if (current_date >= start_date) and (current_date <= end_date):
            total_point = p_point * quantity
            unit_point = p_point

        else:
            total_point = 0
            unit_point = 0

    else:

        total_point = 0
        unit_point = 0

    # Fetching the product price
    try:

        product_price = ProductPrice.objects.filter(
            specification_id=specificationid).last()
    except:
        product_price = None

    if product_price is not None:
        p_price = product_price.price
        unit_price = p_price
    else:
        p_price = 0
        unit_price = p_price

    # Fetching the product discount
    try:
        product_discount = discount_product.objects.filter(
            specification_id=specificationid).last()
    except:
        product_discount = None

    if product_discount is not None:

        if product_discount.discount_type == "amount":

            if product_discount.amount:
                p_discount = product_discount.amount
            else:
                p_discount = 0

            current_date = timezone.now().date()
            discount_start_date = current_date
            discount_end_date = current_date
            if product_discount.start_date:

                discount_start_date = product_discount.start_date
            else:
                discount_start_date = current_date

            if product_discount.end_date:
                discount_end_date = product_discount.end_date

            else:
                discount_end_date = current_date

            if (current_date >= discount_start_date) and (current_date <= discount_end_date):
                total_discount = p_discount * quantity
                total_price = (p_price * quantity) - total_discount
                unit_price = p_price - p_discount

            else:
                total_discount = 0
                total_price = (p_price * quantity) - total_discount
                unit_price = p_price

        elif product_discount.discount_type == "percentage":

            if product_discount.amount:
                p_discount = product_discount.amount
                p_discount = (p_discount * p_price)/100
            else:
                p_discount = 0

            current_date = timezone.now().date()
            discount_start_date = current_date
            discount_end_date = current_date
            if product_discount.start_date:

                discount_start_date = product_discount.start_date
            else:
                discount_start_date = current_date

            if product_discount.end_date:
                discount_end_date = product_discount.end_date

            else:
                discount_end_date = current_date

            if (current_date >= discount_start_date) and (current_date <= discount_end_date):

                total_discount = p_discount * quantity
                total_price = (p_price * quantity) - total_discount
                unit_price = p_price - p_discount

            else:
                total_discount = 0
                total_price = (p_price * quantity) - total_discount
                unit_price = p_price

        else:
            total_price = p_price * quantity
            unit_price = p_price

    else:
        total_price = p_price * quantity
        unit_price = p_price

    try:
        product_name = Product.objects.filter(id=productid).last()
    except:
        product_name = None

    if product_name is not None:

        p_name = str(product_name.title)
        p_id = product_name.id

    else:
        p_name = ""

    # user_id = values['user_id']
    # non_verified_user_id = values['non_verified_user_id']
    cart_count = 0

    try:
        product_impression = ProductImpression.objects.filter(product_id=productid)[
            0:1].get()
    except:
        product_impression = None

    if product_impression is None:
        pass
    else:

        cart_count = product_impression.cart_count

    cart = cart_count + 1
    ProductImpression.objects.filter(
        product_id=productid).update(cart_count=cart)

    try:

        product_spec = ProductSpecification.objects.get(id=specificationid)

    except:

        product_spec = None

    # print(product_spec)

    print(product_spec)

    if product_spec:

        item_quantity = product_spec.quantity
        color = product_spec.color
        size = product_spec.size
        unit = product_spec.unit
        weight = product_spec.weight

        if item_quantity >= quantity:

            if non_verified_user_id == 0:

                try:
                    # Fetching the specific order of the specific user that hasnt been checked out
                    specific_order = Order.objects.filter(
                        user_id=user_id, checkout_status=False)[0:1].get()
                    order_id = specific_order.id
                except:
                    specific_order = None

                # if the specific user exists
                if specific_order is not None:

                    try:
                        # checking if the product exists in this order
                        specific_order_product = OrderDetails.objects.filter(
                            order_id=order_id, product_id=productid, is_removed=False, delivery_removed=False, specification_id=specificationid)[0:1].get()

                    except:
                        specific_order_product = None

                    if specific_order_product is not None:

                        if specific_order_product.total_quantity >= 1:
                            specific_order_product.total_quantity -= 1
                            specific_order_product.remaining -= 1
                            specific_order_product.total_price -= total_price
                            specific_order_product.total_point -= total_point
                            specific_order_product.save()
                            orderdetailsserializers = OrderDetailsSerializer(
                                specific_order_product, data=request.data)
                            if orderdetailsserializers.is_valid():
                                orderdetailsserializers.save()
                                return JsonResponse({'success': True, 'message': 'The quantity has been decreased'})

                    else:
                        return JsonResponse({'success': False, 'message': 'The item does not exist'})

                else:
                    return JsonResponse({'success': False, 'message': 'The order does not exist'})

            else:

                try:
                    # Fetching the specific order of the specific user that hasnt been checked out
                    specific_order = Order.objects.filter(
                        non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()
                    order_id = specific_order.id
                except:
                    specific_order = None

                # if the specific user exists
                if specific_order is not None:

                    try:
                        # checking if the product exists in this order
                        specific_order_product = OrderDetails.objects.filter(
                            order_id=order_id, product_id=productid, delivery_removed=False, is_removed=False, specification_id=specificationid)[0:1].get()

                    except:
                        specific_order_product = None

                    if specific_order_product is not None:

                        if specific_order_product.total_quantity >= 1:
                            specific_order_product.total_quantity -= 1
                            specific_order_product.remaining -= 1
                            specific_order_product.total_price -= total_price
                            specific_order_product.total_point -= total_point
                            specific_order_product.save()
                            orderdetailsserializers = OrderDetailsSerializer(
                                specific_order_product, data=request.data)
                            if orderdetailsserializers.is_valid():
                                orderdetailsserializers.save()

                                return JsonResponse({'success': True, 'message': 'The quantity has been decreased'})

                    else:
                        return JsonResponse({'success': False, 'message': 'The item does not exist'})

                else:
                    return JsonResponse({'success': False, 'message': 'The order does not exist'})

        else:

            message = "You cannot add to cart.We only have "+str(item_quantity)+" of item "+str(
                p_name)+" of color "+str(color)+" of size "+str(size)+" in our stock currently."

            return JsonResponse({'success': False, 'message': message})

    else:

        return JsonResponse({'success': False, 'message': 'This product does not exist'})


@api_view(['PUT', ])
def decrease_quantity(request, productid):

    color = request.data.get('color')
    size = request.data.get('size')
    #unit = request.data.get('unit')

    p_price = 0
    p_discount = 0
    p_point = 0
    total_price = 0
    total_point = 0
    p_name = ""
    unit_point = 0
    unit_price = 0
    quantity = 1
    # Fetching the product points
    try:
        product_point = ProductPoint.objects.filter(
            product_id=productid).last()
    except:
        product_point = None

    if product_point is not None:
        p_point = product_point.point
        start_date = product_point.start_date
        end_date = product_point.end_date
        current_date = timezone.now().date()

        if product_point.start_date:
            start_date = product_point.start_date
        else:
            start_date = current_date

        if product_point.end_date:
            end_date = product_point.end_date

        else:

            end_date = current_date

        if (current_date >= start_date) and (current_date <= end_date):
            total_point = p_point * quantity
            unit_point = p_point

        else:
            total_point = 0
            unit_point = 0

    else:

        total_point = 0
        unit_point = 0

    # Fetching the product price
    try:

        product_price = ProductPrice.objects.filter(
            product_id=productid).last()
    except:
        product_price = None

    if product_price is not None:
        p_price = product_price.price
        unit_price = p_price
    else:
        p_price = 0
        unit_price = p_price

    # Fetching the product discount
    try:
        product_discount = discount_product.objects.filter(
            product_id=productid).last()
    except:
        product_discount = None

    if product_discount is not None:
        p_discount = product_discount.amount
        discount_start_date = product_discount.start_date
        discount_end_date = product_discount.end_date
        current_date = timezone.now().date()

        if product_discount.start_date:
            discount_start_date = product_discount.start_date
        else:
            discount_start_date = current_date

        if product_discount.end_date:
            discount_end_date = product_discount.end_date

        else:

            discount_end_date = current_date

        if (current_date >= discount_start_date) and (current_date <= discount_end_date):
            total_discount = p_discount * quantity
            total_price = (p_price * quantity) - total_discount
            unit_price = p_price - p_discount

        else:
            total_discount = 0
            total_price = (p_price * quantity) - total_discount
            unit_price = p_price
    else:
        total_price = p_price * quantity
        unit_price = p_price

    try:
        product_name = Product.objects.filter(id=productid).last()
    except:
        product_name = None

    if product_name is not None:

        p_name = str(product_name.title)
        p_id = product_name.id

    else:
        p_name = ""

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    cart_count = 0

    try:
        product_impression = ProductImpression.objects.filter(product_id=productid)[
            0:1].get()
    except:
        product_impression = None

    if product_impression is None:
        pass
    else:

        cart_count = product_impression.cart_count

    cart = cart_count - 1
    ProductImpression.objects.filter(
        product_id=productid).update(cart_count=cart)

    if non_verified_user_id == 0:

        try:
            # Fetching the specific order of the specific user that hasnt been checked out
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=False)[0:1].get()
            order_id = specific_order.id
        except:
            specific_order = None

        # if the specific user exists
        if specific_order is not None:

            try:
                # checking if the product exists in this order
                specific_order_product = OrderDetails.objects.filter(
                    order_id=order_id, product_id=productid, is_removed=False, product_color=color, product_size=size)[0:1].get()

            except:
                specific_order_product = None

            if specific_order_product is not None:

                if specific_order_product.total_quantity >= 1:
                    specific_order_product.total_quantity -= 1
                    specific_order_product.remaining -= 1
                    specific_order_product.total_price -= total_price
                    specific_order_product.total_point -= total_point
                    specific_order_product.save()
                    orderdetailsserializers = OrderDetailsSerializer(
                        specific_order_product, data=request.data)
                    if orderdetailsserializers.is_valid():
                        orderdetailsserializers.save()
                        return JsonResponse({'success': True, 'message': 'The quantity has been decreased'})

            else:
                return JsonResponse({'success': False, 'message': 'The item does not exist'})

        else:
            return JsonResponse({'success': False, 'message': 'The order does not exist'})

    else:

        try:
            # Fetching the specific order of the specific user that hasnt been checked out
            specific_order = Order.objects.filter(
                non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()
            order_id = specific_order.id
        except:
            specific_order = None

        # if the specific user exists
        if specific_order is not None:

            try:
                # checking if the product exists in this order
                specific_order_product = OrderDetails.objects.filter(
                    order_id=order_id, product_id=productid, is_removed=False, product_color=color, product_size=size)[0:1].get()

            except:
                specific_order_product = None

            if specific_order_product is not None:

                if specific_order_product.total_quantity >= 1:
                    specific_order_product.total_quantity -= 1
                    specific_order_product.total_price -= total_price
                    specific_order_product.total_point -= total_point
                    specific_order_product.save()
                    orderdetailsserializers = OrderDetailsSerializer(
                        specific_order_product, data=request.data)
                    if orderdetailsserializers.is_valid():
                        orderdetailsserializers.save()
                        return JsonResponse({'success': True, 'message': 'The quantity has been decreased'})

            else:
                return JsonResponse({'success': False, 'message': 'The item does not exist'})

        else:
            return JsonResponse({'success': False, 'message': 'The order does not exist'})


# this removes the specific product from the cart
@api_view(['PUT', ])
def delete_product(request, productid):

    color = request.data.get('color')
    size = request.data.get('size')
    #unit = request.data.get('unit')

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    cart_count = 0
    try:
        product_impression = ProductImpression.objects.filter(product_id=productid)[
            0:1].get()
    except:
        product_impression = None

    if ProductImpression is None:
        pass
    else:
        cart_count = product_impression.cart_count

    # cart = cart_count - 1
    # ProductImpression.objects.filter(product_id=productid).update(cart_count=cart)

    if non_verified_user_id == 0:

        try:
            # Fetching the specific order of the specific user that hasnt been checked out
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=False)[0:1].get()
            order_id = specific_order.id
        except:
            specific_order = None

        # if the specific user exists
        if specific_order is not None:

            try:
                # checking if the product exists in this order
                specific_order_product = OrderDetails.objects.filter(
                    order_id=order_id, product_id=productid, delivery_removed=False, is_removed=False, product_color=color, product_size=size)[0:1].get()

            except:
                specific_order_product = None

            if specific_order_product is not None:

                product_quantity = specific_order_product.total_quantity
                cart = cart_count - product_quantity
                ProductImpression.objects.filter(
                    product_id=productid).update(cart_count=cart)

                specific_order_product.is_removed = True
                specific_order_product.save()
                return JsonResponse({'success': True, 'message': 'The item has been removed from the cart'})

            else:
                return JsonResponse({'success': False, 'message': 'The item doesn not exist'})

        else:
            return JsonResponse({'success': False, 'message': 'The item doesn not exist'})

    else:
        try:
            # Fetching the specific order of the specific user that hasnt been checked out
            specific_order = Order.objects.filter(
                non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()
            order_id = specific_order.id
        except:
            specific_order = None

        # if the specific user exists
        if specific_order is not None:

            try:
                # checking if the product exists in this order
                specific_order_product = OrderDetails.objects.filter(
                    order_id=order_id, product_id=productid, delivery_removed=False, is_removed=False, product_color=color, product_size=size)[0:1].get()

            except:
                specific_order_product = None

            if specific_order_product is not None:

                product_quantity = specific_order_product.total_quantity
                cart = cart_count - product_quantity
                ProductImpression.objects.filter(
                    product_id=productid).update(cart_count=cart)

                specific_order_product.is_removed = True
                specific_order_product.save()
                return JsonResponse({'success': True, 'message': 'The item has been removed from the cart'})

        else:
            return JsonResponse({'success': False, 'message': 'The item doesn not exist'})


@api_view(['PUT', ])
def delete_product1(request, specificationid):

    #unit = request.data.get('unit')

    productid = request.data.get('product_id')

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    cart_count = 0
    try:
        product_impression = ProductImpression.objects.filter(product_id=productid)[
            0:1].get()
    except:
        product_impression = None

    if ProductImpression is None:
        pass
    else:
        cart_count = product_impression.cart_count

    # cart = cart_count - 1
    # ProductImpression.objects.filter(product_id=productid).update(cart_count=cart)

    if non_verified_user_id == 0:

        try:
            # Fetching the specific order of the specific user that hasnt been checked out
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=False)[0:1].get()
            order_id = specific_order.id
        except:
            specific_order = None

        # if the specific user exists
        if specific_order is not None:

            try:
                # checking if the product exists in this order
                specific_order_product = OrderDetails.objects.filter(
                    order_id=order_id, product_id=productid, delivery_removed=False, is_removed=False, specification_id=specificationid)[0:1].get()

            except:
                specific_order_product = None

            if specific_order_product is not None:

                product_quantity = specific_order_product.total_quantity
                cart = cart_count - product_quantity
                ProductImpression.objects.filter(
                    product_id=productid).update(cart_count=cart)

                specific_order_product.is_removed = True
                specific_order_product.save()
                return JsonResponse({'success': True, 'message': 'The item has been removed from the cart'})

            else:
                return JsonResponse({'success': False, 'message': 'The item doesn not exist'})

        else:
            return JsonResponse({'success': False, 'message': 'The item doesn not exist'})

    else:
        try:
            # Fetching the specific order of the specific user that hasnt been checked out
            specific_order = Order.objects.filter(
                non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()
            order_id = specific_order.id
        except:
            specific_order = None

        # if the specific user exists
        if specific_order is not None:

            try:
                # checking if the product exists in this order
                specific_order_product = OrderDetails.objects.filter(
                    order_id=order_id, product_id=productid, delivery_removed=False, is_removed=False, specification_id=specificationid)[0:1].get()

            except:
                specific_order_product = None

            if specific_order_product is not None:

                product_quantity = specific_order_product.total_quantity
                cart = cart_count - product_quantity
                ProductImpression.objects.filter(
                    product_id=productid).update(cart_count=cart)

                specific_order_product.is_removed = True
                specific_order_product.save()
                return JsonResponse({'success': True, 'message': 'The item has been removed from the cart'})

        else:
            return JsonResponse({'success': False, 'message': 'The item doesn not exist'})


# @api_view(['POST', ])
# def checkout(request):

#     user_id = request.data.get('user_id')
#     billing_address_id = request.data.get('billing_address_id')
#     #coupon_code = request.data.get('coupon_code')
#     # print(type(coupon_code))
#     non_verified_user_id = request.data.get('non_verified_user_id')
#     if user_id is not None:
#         user_id = int(user_id)
#         non_verified_user_id = 0

#     else:
#         non_verified_user_id = int(non_verified_user_id)
#         user_id = 0

#     flag = False
#     product_name = ""
#     product_quantity = 0
#     current_quantity = 0
#     current_color = ""
#     current_size = ""
#     current_unit = ""
#     current_name = ""

#     if non_verified_user_id == 0:

#         try:
#             # Fetching the specific order of the specific user that hasnt been checked out
#             specific_order = Order.objects.filter(
#                 user_id=user_id, checkout_status=False)[0:1].get()

#         except:
#             specific_order = None

#         if specific_order is not None:

#             # specific_order.checkout_status = True
#             # specific_order.order_status = "Unpaid"
#             # specific_order.delivery_status = "To pay"
#             # specific_order.ordered_date = datetime.now()
#             # specific_order.save()
#             orders_id = specific_order.id
#             orders_details = OrderDetails.objects.filter(
#                 order_id=orders_id, is_removed=False,delivery_removed=False)

#             order_det_ids = orders_details.values_list('id', flat=True)

#             not_delivered = []

#             for i in range(len(order_det_ids)):

#                 try:

#                     order_dets = OrderDetails.objects.get(id=order_det_ids[i])

#                 except:

#                     order_dets = None


#                 if order_dets:

#                     spec_id = order_dets.specification_id

#                     check_loc = check_location(spec_id,billing_address_id)


#                     print("chceck_loc")

#                     print(check_loc)

#                     if check_loc == False:

#                         not_delivered.append(order_dets.product_name)

#                         order_dets.delivery_removed = True


#                         order_dets.save()


#             #Fetch the areas and location

#             try:

#                 bill_address = BillingAddress.objects.get(id=billing_address_id)

#             except:

#                 bill_address = None

#             if bill_address:

#                 area = bill_address.area
#                 location = bill_address.location

#             else:

#                 area = ""
#                 location = ""


#             if len(not_delivered) > 0:

#                 product_message = ""

#                 # for k in range(len(not_delivered)):

#                 if len(not_delivered) == 1:

#                     product_message = not_delivered[0]

#                 elif len(not_delivered) > 1:

#                     for x in range(len(not_delivered)):

#                         product_message = product_message + not_delivered[x] + ", "


#                 new_product_message = product_message[:-2]

#                 delivery_message = new_product_message +" are not available in location:"+location+" of area:"+area


#             else:

#                 delivery_message = ""


#             order_id = specific_order.id
#             order_details = OrderDetails.objects.filter(
#                 order_id=order_id, is_removed=False,delivery_removed=False)
#             order_ids = order_details.values_list('id', flat=True)
#             order_products = order_details.values_list('product_id', flat=True)
#             order_specs = order_details.values_list(
#                 'specification_id', flat=True)
#             order_colors = order_details.values_list(
#                 'product_color', flat=True)
#             order_sizes = order_details.values_list('product_size', flat=True)
#             #order_units = order_details.values_list('product_unit',flat = True)
#             order_names = order_details.values_list('product_name', flat=True)
#             order_quantity = order_details.values_list(
#                 'total_quantity', flat=True)

#             print("order_idsssss")
#             print(order_ids)

#             if len(order_ids) > 0:


#                 for i in range(len(order_ids)):
#                     print("dhuklam")
#                     print(order_sizes[i])
#                     print(order_colors[i])
#                     # print(order_units[i])
#                     product = ProductSpecification.objects.get(id=order_specs[i])
#                     if product:
#                         product_quantity = product.quantity

#                     else:
#                         product_quantity = 0

#                     print("Ashchi")
#                     # print(product.title)
#                     # print(product.quantity)
#                     product_name = order_names[i]
#                     product_color = order_colors[i]
#                     product_size = order_sizes[i]
#                     #product_unit = order_units[i]
#                     if order_quantity[i] > product_quantity:
#                         current_quantity = product_quantity
#                         current_name = product_name
#                         current_color = product_color
#                         current_size = product_size
#                         #current_unit = product_unit
#                         flag = False
#                         break
#                     else:
#                         flag = True

#                 print(flag)

#                 if flag == True:
#                     print("cjeck kora possible")

#                     # change the coupon
#                     # if coupon_code == '':
#                     #   specific_order.coupon_code =
#                     # else:
#                     #   specific_order.coupon = True

#                     # user can checkout
#                     #specific_order.coupon_code = coupon_code
#                     specific_order.checkout_status = True
#                     specific_order.order_status = "Unpaid"
#                     specific_order.delivery_status = "To ship"
#                     specific_order.ordered_date = timezone.now()
#                     specific_order.save()

#                     for i in range(len(order_products)):
#                         product = ProductSpecification.objects.get(
#                             id=order_specs[i])
#                         product_quantity = product.quantity
#                         product.quantity -= order_quantity[i]
#                         product.save()
#                         productserializer = ProductSpecificationSerializer(
#                             product, data=request.data)
#                         print("fuhfuwhuhfuewhewuhew")
#                         if productserializer.is_valid():
#                             print("ffbwybwbfywefbweyfbefb")
#                             productserializer.save()

#                             sales_count = 0
#                             try:
#                                 product_impression = ProductImpression.objects.filter(
#                                     product_id=order_products[i])[0:1].get()
#                                 print(product_impression)
#                             except:
#                                 product_impression = None

#                             if ProductImpression is None:
#                                 print("hochche na")
#                                 pass
#                             else:
#                                 print("hochche")
#                                 product_impression.sales_count += order_quantity[i]
#                                 product_impression.save()

#                                 print(product_impression.sales_count)
#                         else:
#                             print("erroesssss")
#                             return JsonResponse(productserializer.errors)

#                     return JsonResponse({'success': True, 'message': 'The items have been checked out','delivery_message':delivery_message})

#                 else:

#                     message = "You cannot checkout.We only have "+str(current_quantity)+" of item "+str(
#                         current_name)+" of color "+str(current_color)+" of size "+str(current_size)+" in our stock currently."
#                     return JsonResponse({'success': False, 'message': message})

#             else:

#                 return JsonResponse({'success': False, 'message': 'None of the items you want can be delivered to your specific location'})

#         else:
#             return JsonResponse({'success': False, 'message': 'This order does not exist'})

#     else:

#         try:
#             # Fetching the specific order of the specific user that hasnt been checked out
#             specific_order = Order.objects.filter(
#                 non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()

#         except:
#             specific_order = None

#         if specific_order is not None:

#             # specific_order.checkout_status = True
#             # specific_order.order_status = "Unpaid"
#             # specific_order.delivery_status = "To pay"
#             # specific_order.ordered_date = datetime.now()
#             # specific_order.save()
#             orders_id = specific_order.id
#             orders_details = OrderDetails.objects.filter(
#                 order_id=orders_id, is_removed=False,delivery_removed=False)

#             order_det_ids = orders_details.values_list('id', flat=True)

#             not_delivered = []

#             for i in range(len(order_det_ids)):

#                 try:

#                     order_dets = OrderDetails.objects.get(id=order_det_ids[i])

#                 except:

#                     order_dets = None


#                 if order_dets:

#                     spec_id = order_dets.specification_id

#                     check_loc = check_location(spec_id,billing_address_id)


#                     print("chceck_loc")

#                     print(check_loc)

#                     if check_loc == False:

#                         not_delivered.append(order_dets.product_name)

#                         order_dets.delivery_removed = True


#                         order_dets.save()


#             #Fetch the areas and location

#             try:

#                 bill_address = BillingAddress.objects.get(id=billing_address_id)

#             except:

#                 bill_address = None

#             if bill_address:

#                 area = bill_address.area
#                 location = bill_address.location

#             else:

#                 area = ""
#                 location = ""


#             if len(not_delivered) > 0:

#                 product_message = ""

#                 # for k in range(len(not_delivered)):

#                 if len(not_delivered) == 1:

#                     product_message = not_delivered[0]

#                 elif len(not_delivered) > 1:

#                     for x in range(len(not_delivered)):

#                         product_message = product_message + not_delivered[x] + ", "


#                 new_product_message = product_message[:-2]

#                 delivery_message = new_product_message +" are not available in location:"+location+" of area:"+area


#             else:

#                 delivery_message = ""


#             order_id = specific_order.id
#             order_details = OrderDetails.objects.filter(
#                 order_id=order_id, is_removed=False,delivery_removed=False)
#             order_ids = order_details.values_list('id', flat=True)
#             order_products = order_details.values_list('product_id', flat=True)
#             order_specs = order_details.values_list(
#                 'specification_id', flat=True)
#             order_colors = order_details.values_list(
#                 'product_color', flat=True)
#             order_sizes = order_details.values_list('product_size', flat=True)
#             #order_units = order_details.values_list('product_unit',flat = True)
#             order_names = order_details.values_list('product_name', flat=True)
#             order_quantity = order_details.values_list(
#                 'total_quantity', flat=True)

#             print("order_idsssss")
#             print(order_ids)

#             if len(order_ids) > 0:


#                 for i in range(len(order_ids)):
#                     print("dhuklam")
#                     print(order_sizes[i])
#                     print(order_colors[i])
#                     # print(order_units[i])
#                     product = ProductSpecification.objects.get(id=order_specs[i])
#                     if product:
#                         product_quantity = product.quantity

#                     else:
#                         product_quantity = 0

#                     print("Ashchi")
#                     # print(product.title)
#                     # print(product.quantity)
#                     product_name = order_names[i]
#                     product_color = order_colors[i]
#                     product_size = order_sizes[i]
#                     #product_unit = order_units[i]
#                     if order_quantity[i] > product_quantity:
#                         current_quantity = product_quantity
#                         current_name = product_name
#                         current_color = product_color
#                         current_size = product_size
#                         #current_unit = product_unit
#                         flag = False
#                         break
#                     else:
#                         flag = True

#                 print(flag)

#                 if flag == True:
#                     print("cjeck kora possible")

#                     # change the coupon
#                     # if coupon_code == '':
#                     #   specific_order.coupon_code =
#                     # else:
#                     #   specific_order.coupon = True

#                     # user can checkout
#                     #specific_order.coupon_code = coupon_code
#                     specific_order.checkout_status = True
#                     specific_order.order_status = "Unpaid"
#                     specific_order.delivery_status = "To ship"
#                     specific_order.ordered_date = timezone.now()
#                     specific_order.save()

#                     for i in range(len(order_products)):
#                         product = ProductSpecification.objects.get(
#                             id=order_specs[i])
#                         product_quantity = product.quantity
#                         product.quantity -= order_quantity[i]
#                         product.save()
#                         productserializer = ProductSpecificationSerializer(
#                             product, data=request.data)
#                         print("fuhfuwhuhfuewhewuhew")
#                         if productserializer.is_valid():
#                             print("ffbwybwbfywefbweyfbefb")
#                             productserializer.save()

#                             sales_count = 0
#                             try:
#                                 product_impression = ProductImpression.objects.filter(
#                                     product_id=order_products[i])[0:1].get()
#                                 print(product_impression)
#                             except:
#                                 product_impression = None

#                             if ProductImpression is None:
#                                 print("hochche na")
#                                 pass
#                             else:
#                                 print("hochche")
#                                 product_impression.sales_count += order_quantity[i]
#                                 product_impression.save()

#                                 print(product_impression.sales_count)
#                         else:
#                             print("erroesssss")
#                             return JsonResponse(productserializer.errors)

#                     return JsonResponse({'success': True, 'message': 'The items have been checked out','delivery_message':delivery_message})

#                 else:

#                     message = "You cannot checkout.We only have "+str(current_quantity)+" of item "+str(
#                         current_name)+" of color "+str(current_color)+" of size "+str(current_size)+" in our stock currently."
#                     return JsonResponse({'success': False, 'message': message})

#             else:

#                 return JsonResponse({'success': False, 'message': 'None of the items you want can be delivered to your specific location'})

#         else:
#             return JsonResponse({'success': False, 'message': 'This order does not exist'})


# @api_view(['POST', ])
# def checkout(request):

#     user_id = request.data.get('user_id')
#     billing_address_id = request.data.get('billing_address')
#     #coupon_code = request.data.get('coupon_code')
#     # print(type(coupon_code))
#     non_verified_user_id = request.data.get('non_verified_user_id')
#     if user_id is not None:
#         user_id = int(user_id)
#         non_verified_user_id = 0

#     else:
#         non_verified_user_id = int(non_verified_user_id)
#         user_id = 0

#     flag = False
#     product_name = ""
#     product_quantity = 0
#     current_quantity = 0
#     current_color = ""
#     current_size = ""
#     current_unit = ""

#     if non_verified_user_id == 0:

#         try:
#             # Fetching the specific order of the specific user that hasnt been checked out
#             specific_order = Order.objects.filter(
#                 user_id=user_id, checkout_status=False)[0:1].get()

#         except:
#             specific_order = None

#         if specific_order is not None:

#             # specific_order.checkout_status = True
#             # specific_order.order_status = "Unpaid"
#             # specific_order.delivery_status = "To pay"
#             # specific_order.ordered_date = datetime.now()
#             # specific_order.save()
#             order_id = specific_order.id
#             order_details = OrderDetails.objects.filter(
#                 order_id=order_id, is_removed=False)
#             order_ids = order_details.values_list('id', flat=True)
#             order_products = order_details.values_list('product_id', flat=True)
#             order_specs = order_details.values_list(
#                 'specification_id', flat=True)
#             order_colors = order_details.values_list(
#                 'product_color', flat=True)
#             order_sizes = order_details.values_list('product_size', flat=True)
#             #order_units = order_details.values_list('product_unit',flat = True)
#             order_names = order_details.values_list('product_name', flat=True)
#             order_quantity = order_details.values_list(
#                 'total_quantity', flat=True)
#             print(order_ids)
#             for i in range(len(order_ids)):
#                 print("dhuklam")
#                 print(order_sizes[i])
#                 print(order_colors[i])
#                 # print(order_units[i])
#                 product = ProductSpecification.objects.get(id=order_specs[i])
#                 if product:
#                     product_quantity = product.quantity

#                 else:
#                     product_quantity = 0

#                 print("Ashchi")
#                 # print(product.title)
#                 # print(product.quantity)
#                 product_name = order_names[i]
#                 product_color = order_colors[i]
#                 product_size = order_sizes[i]
#                 #product_unit = order_units[i]
#                 if order_quantity[i] > product_quantity:
#                     current_quantity = product_quantity
#                     current_name = product_name
#                     current_color = product_color
#                     current_size = product_size
#                     #current_unit = product_unit
#                     flag = False
#                     break
#                 else:
#                     flag = True

#             print(flag)

#             if flag == True:
#                 print("cjeck kora possible")

#                 # change the coupon
#                 # if coupon_code == '':
#                 #     specific_order.coupon_code =
#                 # else:
#                 #     specific_order.coupon = True

#                 # user can checkout
#                 #specific_order.coupon_code = coupon_code
#                 specific_order.checkout_status = True
#                 specific_order.order_status = "Unpaid"
#                 specific_order.delivery_status = "To ship"
#                 specific_order.ordered_date = timezone.now()
#                 specific_order.save()

#                 for i in range(len(order_products)):
#                     product = ProductSpecification.objects.get(
#                         id=order_specs[i])
#                     product_quantity = product.quantity
#                     product.quantity -= order_quantity[i]
#                     product.save()
#                     productserializer = ProductSpecificationSerializer(
#                         product, data=request.data)
#                     print("fuhfuwhuhfuewhewuhew")
#                     if productserializer.is_valid():
#                         print("ffbwybwbfywefbweyfbefb")
#                         productserializer.save()

#                         sales_count = 0
#                         try:
#                             product_impression = ProductImpression.objects.filter(
#                                 product_id=order_products[i])[0:1].get()
#                             print(product_impression)
#                         except:
#                             product_impression = None

#                         if ProductImpression is None:
#                             print("hochche na")
#                             pass
#                         else:
#                             print("hochche")
#                             product_impression.sales_count += order_quantity[i]
#                             product_impression.save()

#                             print(product_impression.sales_count)
#                     else:
#                         print("erroesssss")
#                         return JsonResponse(productserializer.errors)

#                 return JsonResponse({'success': True, 'message': 'The items have been checked out'})

#             else:

#                 message = "You cannot checkout.We only have "+str(current_quantity)+" of item "+str(
#                     current_name)+" of color "+str(current_color)+" of size "+str(current_size)+" in our stock currently."
#                 return JsonResponse({'success': False, 'message': message})

#         else:
#             return JsonResponse({'success': False, 'message': 'This order does not exist'})

#     else:

#         try:
#             # Fetching the specific order of the specific user that hasnt been checked out
#             specific_order = Order.objects.filter(
#                 non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()

#         except:
#             specific_order = None

#         if specific_order is not None:

#             # specific_order.checkout_status = True
#             # specific_order.order_status = "Unpaid"
#             # specific_order.delivery_status = "To pay"
#             # specific_order.ordered_date = datetime.now()
#             # specific_order.save()
#             order_id = specific_order.id
#             order_details = OrderDetails.objects.filter(
#                 order_id=order_id, is_removed=False)
#             order_products = order_details.values_list('product_id', flat=True)
#             order_colors = order_details.values_list(
#                 'product_color', flat=True)
#             order_sizes = order_details.values_list('product_size', flat=True)
#             order_specs = order_details.values_list(
#                 'specification_id', flat=True)

#             #order_units = order_details.values_list('product_unit',flat = True)
#             order_names = order_details.values_list('product_name', flat=True)
#             order_quantity = order_details.values_list(
#                 'total_quantity', flat=True)
#             for i in range(len(order_products)):
#                 product = ProductSpecification.objects.get(id=order_specs[i])
#                 if product:
#                     product_quantity = product.quantity

#                 else:
#                     product_quantity = 0
#                 # print(product.title)
#                 # print(product.quantity)
#                 product_name = order_names[i]
#                 product_color = order_colors[i]
#                 product_size = order_sizes[i]
#                 #product_unit = order_units[i]
#                 if order_quantity[i] > product_quantity:
#                     current_quantity = product_quantity
#                     current_name = product_name
#                     current_color = product_color
#                     current_size = product_size
#                     #current_unit = product_unit
#                     flag = False
#                     break
#                 else:
#                     flag = True

#             if flag == True:

#                 # change the coupon
#                 # if coupon_code == '':
#                 #     specific_order.coupon_code =
#                 # else:
#                 #     specific_order.coupon = True

#                 # user can checkout
#                 #specific_order.coupon_code = coupon_code
#                 specific_order.checkout_status = True
#                 specific_order.order_status = "Unpaid"
#                 specific_order.delivery_status = "To ship"
#                 specific_order.ordered_date = timezone.now()
#                 specific_order.save()

#                 for i in range(len(order_products)):
#                     product = ProductSpecification.objects.get(
#                         id=order_specs[i])
#                     product_quantity = product.quantity
#                     product.quantity -= order_quantity[i]
#                     product.save()
#                     productserializer = ProductSpecificationSerializer(
#                         product, data=request.data)
#                     print("fuhfuwhuhfuewhewuhew")
#                     if productserializer.is_valid():
#                         print("ffbwybwbfywefbweyfbefb")
#                         productserializer.save()

#                         sales_count = 0
#                         try:
#                             product_impression = ProductImpression.objects.filter(
#                                 product_id=order_products[i])[0:1].get()
#                         except:
#                             product_impression = None

#                         if ProductImpression is None:
#                             pass
#                         else:
#                             product_impression.sales_count += order_quantity[i]
#                             product_impression.save()

#                     else:
#                         print("erroesssss")
#                         return JsonResponse(productserializer.errors)

#                 return JsonResponse({'success': True, 'message': 'The items have been checked out'})

#             else:

#                 message = "You cannot checkout.We only have "+str(current_quantity)+" of item "+str(
#                     current_name)+" of color "+str(current_color)+" of size "+str(current_size)+" in our stock currently."
#                 return JsonResponse({'success': False, 'message': message})

#         else:

#             return JsonResponse({'success': False, 'message': 'This order does not exist'}


@api_view(['POST', ])
def cart_view(request):

    orders_id = -1
    checkout_id = False
    orderz = []

    arr = [
        {
            "id": orders_id,
            "date_created": "",
            "order_status": "",
            "delivery_status": "",
            "user_id": orders_id,
            "non_verified_user_id": orders_id,
            "ip_address": "",
            "checkout_status": checkout_id,
            "price_total": "0.00",
            "point_total": "0.00",
            "ordered_date": "",
            "orders": orderz
        }
    ]

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=False)
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer3(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in the cart are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': True, 'message': 'There are no products in the cart', 'data': arr})

    else:

        try:
            specific_order = Order.objects.filter(
                non_verified_user_id=non_verified_user_id, checkout_status=False)
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer3(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in the cart are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': True, 'message': 'There are no products in the cart', 'data': arr})


@api_view(['POST', ])
def cart_details(request):

    orders_id = -1
    checkout_id = False
    orderz = []

    arr = [
        {
            "id": orders_id,
            "date_created": "",
            "order_status": "",
            "delivery_status": "",
            "user_id": orders_id,
            "non_verified_user_id": orders_id,
            "ip_address": "",
            "checkout_status": checkout_id,
            "price_total": "0.00",
            "point_total": "0.00",
            "ordered_date": "",
            "orders": orderz,
            "specification": orderz
        }
    ]

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=False)
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializerzz(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in the cart are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': True, 'message': 'There are no products in the cart', 'data': arr})

    else:

        try:
            specific_order = Order.objects.filter(
                non_verified_user_id=non_verified_user_id, checkout_status=False)
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializerzz(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in the cart are shown', 'data': orderserializer.data}, safe=False)

        else:

            return JsonResponse({'success': True, 'message': 'There are no products in the cart', 'data': arr})


# # This shows the information of the persons all orders
# @api_view(['POST', ])
# def all_orders(request):

#     user_id = request.data.get('user_id')
#     non_verified_user_id = request.data.get('non_verified_user_id')
#     if user_id is not None:
#         user_id = int(user_id)
#         non_verified_user_id = 0

#     else:
#         non_verified_user_id = int(non_verified_user_id)
#         user_id = 0

#     if non_verified_user_id == 0:

#         try:
#             specific_order = Order.objects.filter(
#                 user_id=user_id, checkout_status=True).order_by('-ordered_date')
#         except:
#             specific_order = None

#         if specific_order:

#             orderserializer = OrderSerializer(specific_order, many=True)
#             #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

#             #orders = [orderserializer.data , orderdetailserializer.data]
#             return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

#         else:
#             return JsonResponse({'success': False, 'message': 'You have no orders'})

#     else:

#         try:
#             specific_order = Order.objects.filter(
#                 non_verified_user_id=non_verified_user_id, checkout_status=True).order_by('-ordered_date')
#         except:
#             specific_order = None

#         if specific_order:

#             orderserializer = OrderSerializer(specific_order, many=True)
#             #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

#             #orders = [orderserializer.data , orderdetailserializer.data]
#             return JsonResponse({'success': True, 'message': 'The products in your orders are shown', 'data': orderserializer.data}, safe=False)

#         else:
#             return JsonResponse({'success': False, 'message': 'You have no orders'})


# This shows the information of the persons all orders
@api_view(['POST', ])
def all_orders(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=True).order_by('-ordered_date')
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)
            order_data = orderserializer.data
            order_data = json.loads(json.dumps(order_data, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
            order_id = order_data[0]["id"]
            try:
                order_info = OrderInfo.objects.filter(order_id=order_id).last()

            except:
                order_info = None 

            if order_info:
                billing_address_id = order_info.billing_address_id

            else:
                billing_address_id = 0

            try:
                billing_address = BillingAddress.objects.get(id=billing_address_id)
            except:
                billing_address = None 

            if billing_address:
                billing_address_serializer = BillingAddressSerializer(billing_address,many=False)
                return JsonResponse({"scuccess":True,"message":"The billing address is shown","billing_data":billing_address_serializer.data,"order_data":orderserializer.data})

            else:
                return JsonResponse({"scuccess":False,"message":"There is no address to show","order_data":orderserializer.data})


            #orders = [orderserializer.data , orderdetailserializer.data]
            #return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})

    else:

        try:
            specific_order = Order.objects.filter(
                non_verified_user_id = non_verified_user_id, checkout_status=True).order_by('-ordered_date')
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)
            order_data = orderserializer.data

            order_data = json.loads(json.dumps(order_data, sort_keys=True, indent=1, cls=DjangoJSONEncoder))

            print(order_data)



           
        
            order_id = int(order_data[0]["id"])
            try:
                order_info = OrderInfo.objects.filter(order_id=order_id).last()

            except:
                order_info = None 

            if order_info:
                billing_address_id = order_info.billing_address_id

            else:
                billing_address_id = 0

            try:
                billing_address = BillingAddress.objects.get(id=billing_address_id)
            except:
                billing_address = None 

            if billing_address:
                billing_address_serializer = BillingAddressSerializer(billing_address,many=False)
                return JsonResponse({"scuccess":True,"message":"The billing address is shown","billing_data":billing_address_serializer.data,"order_data":orderserializer.data})

            else:
                return JsonResponse({"scuccess":False,"message":"There is no address to show","order_data":orderserializer.data})


            #orders = [orderserializer.data , orderdetailserializer.data]
            #return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})





# This shows the information of the a specific
@api_view(['POST', ])
def specific_order(request, order_id):

    # user_id = request.data.get('user_id')
    # non_verified_user_id = request.data.get('non_verified_user_id')
    # if user_id is not None:
    # 	user_id = int(user_id)
    # 	non_verified_user_id =0

    # else:
    # 	non_verified_user_id = int(non_verified_user_id)
    # 	user_id = 0

    # if non_verified_user_id == 0:

    try:
        specific_order = Order.objects.get(id=order_id)
        print(specific_order)
    except:
        specific_order = None

    if specific_order:

        orderserializer = OrderSerializer(specific_order)
        #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

        #orders = [orderserializer.data , orderdetailserializer.data]
        return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

    else:
        return JsonResponse({'success': False, 'message': 'You have no orders'})


# This shows the information of the a specific
@api_view(['GET', ])
def orders(request):

    # user_id = request.data.get('user_id')
    # non_verified_user_id = request.data.get('non_verified_user_id')
    # if user_id is not None:
    # 	user_id = int(user_id)
    # 	non_verified_user_id =0

    # else:
    # 	non_verified_user_id = int(non_verified_user_id)
    # 	user_id = 0

    # if non_verified_user_id == 0:

    try:
        specific_order = Order.objects.filter(checkout_status=True, admin_status="Confirmed").order_by('-ordered_date') | Order.objects.filter(
            checkout_status=True, admin_status="Cancelled").order_by('-ordered_date')
    except:
        specific_order = None

    print("specific order")
    # print(sp)

    if specific_order:

        orderserializer = OrderSerializer(specific_order, many=True)
        #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

        #orders = [orderserializer.data , orderdetailserializer.data]
        return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

    else:
        return JsonResponse({'success': False, 'message': 'You have no orders'})

    # else:

    # 	try:
    # 		specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True)
    # 	except:
    # 		specific_order = None

    # 	if specific_order:

    # 		orderserializer = OrderSerializer(specific_order, many = True)
    # 		#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

    # 		#orders = [orderserializer.data , orderdetailserializer.data]
    # 		return JsonResponse({'success':True,'message':'The products in your orders are shown','data':orderserializer.data},safe=False)

    # 	else:
    # 		return JsonResponse({'success':False,'message': 'You have no orders'})


# This is for the admin panel. Shows all the orders not approved by the admin
@api_view(['GET', ])
def orders_pending(request):

    # user_id = request.data.get('user_id')
    # non_verified_user_id = request.data.get('non_verified_user_id')
    # if user_id is not None:
    # 	user_id = int(user_id)
    # 	non_verified_user_id =0

    # else:
    # 	non_verified_user_id = int(non_verified_user_id)
    # 	user_id = 0

    # if non_verified_user_id == 0:

    try:
        specific_order = Order.objects.filter(
            checkout_status=True, admin_status="Processing").order_by('-id')
    except:
        specific_order = None

    if specific_order:

        orderserializer = OrderSerializer(specific_order, many=True)
        #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

        #orders = [orderserializer.data , orderdetailserializer.data]
        return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

    else:
        return JsonResponse({'success': False, 'message': 'You have no orders'})

    # else:

    # 	try:
    # 		specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True)
    # 	except:
    # 		specific_order = None

    # 	if specific_order:

    # 		orderserializer = OrderSerializer(specific_order, many = True)
    # 		#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

    # 		#orders = [orderserializer.data , orderdetailserializer.data]
    # 		return JsonResponse({'success':True,'message':'The products in your orders are shown','data':orderserializer.data},safe=False)

    # 	else:
    # 		return JsonResponse({'success':False,'message': 'You have no orders'})


# This shows the information of the user's orders that are to be paid
@api_view(['POST', ])
def orders_to_pay(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=True, order_status="Unpaid", admin_status="Confirmed").order_by('-ordered_date')
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})

    else:

        try:
            specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id, checkout_status=True,
                                                  order_status="Unpaid", admin_status="Confirmed")
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in your orders are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})


# This shows the information of the user's orders that are to be shipped
@api_view(['POST', ])
def orders_to_ship(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    delivery_statuses = ["Pending", "Shipped", "Picked"]
    payment_statuses = ["Paid", "Unpaid"]

    if non_verified_user_id == 0:

        try:
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=True, delivery_status__in=delivery_statuses, admin_status="Confirmed", order_status__in=payment_statuses)

        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})

    else:

        try:
            specific_order = Order.objects.filter(
                non_verified_user_id=non_verified_user_id, checkout_status=True, delivery_status__in=delivery_statuses, admin_status="Confirmed", order_status__in=payment_statuses)
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in your orders are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})


# This shows the information of the user's orders that have already been received
@api_view(['POST', ])
def orders_received(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=True, delivery_status="Delivered", order_status="Paid", admin_status="Confirmed").order_by('-ordered_date')
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})

    else:

        try:
            specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id, checkout_status=True,
                                                  delivery_status="Received", order_status="Paid", admin_status="Confirmed")
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in your orders are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})


# This shows the information of the user's orders that have already been received
@api_view(['POST', ])
def orders_cancelled(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=True, admin_status="Cancelled").order_by('-ordered_date')
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})

    else:

        try:
            specific_order = Order.objects.filter(
                non_verified_user_id=non_verified_user_id, checkout_status=True, delivery_status="Cancelled", order_status="Cancelled")
        except:
            specific_order = None

        if specific_order:

            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'success': True, 'message': 'The products in your orders are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})

# This shows the information of all the orders that have not been paid for
# FOR THE PAYMENT API


@api_view(['GET', ])
def orders_not_paid(request):

    try:
        specific_order = Order.objects.filter(
            order_status="Unpaid", checkout_status=True).order_by('-ordered_date')
        # order_ids = specific_order.values_list('id' , flat = True)
        # orderdetails =[]
        # for i in range(len(order_ids)):
        # 	details_data = OrderDetails.objects.filter(order_id = order_ids[i],is_removed=False)
        # 	orderdetails += details_data

        if request.method == 'GET':
            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse(orderserializer.data, safe=False)

    except Order.DoesNotExist:
        return JsonResponse({'message': 'This order does not exist'}, status=status.HTTP_404_NOT_FOUND)

# This shows the information of all the orders that have not been delivered for
# FOR THE DELIVERY API


@api_view(['GET', ])
def orders_not_delivered(request):

    try:
        specific_order = Order.objects.filter(
            delivery_status="To ship", checkout_status=True).order_by('-ordered_date')
        # order_ids = specific_order.values_list('id' , flat = True)
        # orderdetails =[]
        # for i in range(len(order_ids)):
        # 	details_data = OrderDetails.objects.filter(order_id = order_ids[i],is_removed=False)
        # 	orderdetails += details_data

        if request.method == 'GET':
            orderserializer = OrderSerializer(specific_order, many=True)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse(orderserializer.data, safe=False)

    except Order.DoesNotExist:
        return JsonResponse({'message': 'This order does not exist'}, status=status.HTTP_404_NOT_FOUND)

# This shows the information of all the orders that have not been delivered for
# FROM THE DELIVERY API


@api_view(['GET', ])
def order_delivery(request, order_id):

    arr = {
        "delivery_charge": "45.00",
        "name": "DHL",
        "delivery_status": "delivered"
    }

    try:
        specific_order = Order.objects.filter(id=order_id).last()
        # order_ids = specific_order.values_list('id' , flat = True)
        # orderdetails =[]
        # for i in range(len(order_ids)):
        # 	details_data = OrderDetails.objects.filter(order_id = order_ids[i],is_removed=False)
        # 	orderdetails += details_data

        if request.method == 'GET':
            orderserializer = OrderSerializer(specific_order, many=True)

            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            return JsonResponse({'order': orderserializer.data, 'delivery_info': arr}, safe=False)

    except Order.DoesNotExist:
        return JsonResponse({'message': 'This order does not exist'}, status=status.HTTP_404_NOT_FOUND)


# This cancels the current user order
# Has to cancel within 3 days of the ordered and if delivery_status is not received
@api_view(['POST', ])
def cancel_order(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=True, delivery_status="To ship", order_status="Unpaid", admin_status="Processing").last()
        except:
            specific_order = None

        if specific_order is not None:

            order_date = specific_order.ordered_date

            cancellation_date = order_date + timedelta(days=3)
            #current_date = datetime.now()
            current_date = timezone.now()
            if current_date < cancellation_date:
                specific_order.order_status = "Cancelled"
                specific_order.delivery_status = "Cancelled"
                specific_order.admin_status = "Cancelled"
                specific_order.save()
                orderserializer = OrderSerializer(specific_order, request.data)
                if orderserializer.is_valid():
                    orderserializer.save()
                    return JsonResponse({'success': True, 'message': 'This order has been cancelled'})

            else:
                return JsonResponse({'success': False, 'message': 'This order cannot be cancelled now'})

        else:
            return JsonResponse({'success': False, 'message': 'This order does not exist'})

    else:
        try:
            specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id, checkout_status=True,
                                                  delivery_status="To ship", order_status="Unpaid", admin_status="Processing").last()
        except:
            specific_order = None

        if specific_order is not None:

            order_date = specific_order.ordered_date

            cancellation_date = order_date + timedelta(days=3)
            #current_date = datetime.now()
            current_date = timezone.now()
            if current_date < cancellation_date:
                specific_order.order_status = "Cancelled"
                specific_order.delivery_status = "Cancelled"
                specific_order.admin_status = "Cancelled"
                specific_order.save()
                orderserializer = OrderSerializer(specific_order, request.data)
                if orderserializer.is_valid():
                    orderserializer.save()
                    return JsonResponse({'success': True, 'message': 'This order has been cancelled'})

            else:
                return JsonResponse({'success': False, 'message': 'This order cannot be cancelled now'})

        else:
            return JsonResponse({'success': False, 'message': 'This order does not exist'})


# This cancels a specific order
# Has to cancel within 3 days of the ordered and if delivery_status is to ship and order_status is unpaid
@api_view(['POST', ])
def cancel_specific_order(request, order_id):

    try:
        specific_order = Order.objects.get(id=order_id)
    except:
        specific_order = None

    if specific_order is not None:

        if (specific_order.delivery_status == "To ship") and (specific_order.order_status == "Unpaid") and (specific_order.admin_status == "Processing"):

            order_date = specific_order.ordered_date

            cancellation_date = order_date + timedelta(days=3)
            #current_date = datetime.now()
            current_date = timezone.now()
            if current_date < cancellation_date:
                specific_order.order_status = "Cancelled"
                specific_order.delivery_status = "Cancelled"
                specific_order.admin_status = "Cancelled"
                specific_order.save()
                orderserializer = OrderSerializer(specific_order, request.data)
                if orderserializer.is_valid():
                    orderserializer.save()
                    return JsonResponse({'success': True, 'message': 'This order has been cancelled'})

            else:
                return JsonResponse({'success': False, 'message': 'This order cannot be cancelled now'})

        else:
            return JsonResponse({'success': False, 'message': 'This order has already been paid and shipped for or has been cancelled'})

    else:
        return JsonResponse({'success': False, 'message': 'This order does not exist'})


@api_view(['POST', ])
def cancelorder(request, order_id):

    try:
        specific_order = Order.objects.get(id=order_id)
    except:
        specific_order = None

    if specific_order is not None:

        if specific_order.admin_status == "Processing":

            specific_order.order_status = "Cancelled"
            specific_order.delivery_status = "Cancelled"
            specific_order.admin_status = "Cancelled"
            specific_order.save()
            try:
                order_details = OrderDetails.objects.filter(order_id=order_id)
            except:
                order_details = None 
            if order_details:
                #find all the item ids

                order_details_ids = list(order_details.values_list('id', flat=True))

                for k in range(len(order_details_ids)):
                    try:
                        specific_item = OrderDetails.objects.get(order_details_ids[k])
                    except:
                        specific_item = None 

                    if specific_item:
                        specific_item.order_status = "Cancelled"
                        specific_item.delivery_status = "Cancelled"
                        specific_item.admin_status = "Cancelled"
                        specific_item.save()
            orderserializer = OrderSerializer(specific_order, request.data)
            if orderserializer.is_valid():
                orderserializer.save()
                return JsonResponse({'success': True, 'message': 'This order has been cancelled'})

            else:
                return JsonResponse({'success': False, 'message': 'This order cannot be cancelled now'})

        else:
            return JsonResponse({'success': False, 'message': 'This order has already been cofirmed by the admin'})

    else:
        return JsonResponse({'success': False, 'message': 'This order does not exist'})


# if items are inside the cart and hasnt been checked out the order will be cancelled within 2 days
@api_view(['POST', ])
def cancel_cart(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=False)[0:1].get()

        except:
            specific_order = None

        if specific_order is not None:

            order_date = specific_order.date_created
            cancellation_date = order_date + timedelta(days=2)
            current_date = timezone.now()
            if current_date > cancellation_date:
                specific_order.checkout_status = True
                specific_order.order_status = "Cancelled"
                specific_order.delivery_status = "Cancelled"
                specific_order.save()
                orderserializer = OrderSerializer(specific_order, request.data)
                if orderserializer.is_valid():
                    orderserializer.save()
                    return JsonResponse({'success': True, 'message': 'This cart has been cancelled due to not been checked out within two days'})

            else:
                return JsonResponse({'success': False, 'message': 'This cart still does not have to be cancelled'})

        else:
            return JsonResponse({'success': False, 'message': 'This cart does not exist'})

    else:
        try:
            specific_order = Order.objects.filter(
                non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()

        except:
            specific_order = None

        if specific_order is not None:

            order_date = specific_order.date_created
            cancellation_date = order_date + timedelta(days=2)
            current_date = timezone.now()
            if current_date > cancellation_date:
                specific_order.checkout_status = True
                specific_order.order_status = "Cancelled"
                specific_order.delivery_status = "Cancelled"
                specific_order.save()
                orderserializer = OrderSerializer(specific_order, request.data)
                if orderserializer.is_valid():
                    orderserializer.save()
                    return JsonResponse({'success': True, 'message': 'This cart has been cancelled due to not been checked out within two days'})

            else:
                return JsonResponse({'success': False, 'message': 'This cart still does not have to be cancelled'})

        else:
            return JsonResponse({'success': False, 'message': 'This cart does not exist'})


# Admin Approval
@api_view(['GET', ])
def admin_approval(request, order_id):

    try:
        specific_order = Order.objects.get(id=order_id)

    except:
        specific_order = None

    if specific_order is not None:

        specific_order.admin_status = "Confirmed"

        orderserializer = OrderSerializer(specific_order, request.data)
        if orderserializer.is_valid():
            orderserializer.save()
            return JsonResponse({'success': True, 'message': 'This order has been approved'})

        else:
            return JsonResponse({'success': False, 'message': 'This order does not exist'})

    else:
        return JsonResponse({'success': False, 'message': 'This order does not exist'})


# Admin Approval
@api_view(['GET', ])
def admin_cancellation(request, order_id):

    try:
        specific_order = Order.objects.get(id=order_id)

    except:
        specific_order = None

    if specific_order is not None:

        specific_order.admin_status = "Cancelled"
        specific_order.save()
        order_id = specific_order.id
        try:
            items = OrderDetails.objects.filter(order_id=order_id)
        except:
            items = None
        if items:

            item_ids = list(items.values_list('id', flat=True).distinct())

            for k in range(len(item_ids)):
                try:
                    specific_item = OrderDetails.objects.get(id=item_ids[k])
                except:
                    specific_item = None

                if specific_item:
                    specific_item.admin_status = "Cancelled"
                    specific_item.save()

                else:
                    pass

        orderserializer = OrderSerializer(specific_order, request.data)
        if orderserializer.is_valid():
            orderserializer.save()
            return JsonResponse({'success': True, 'message': 'This order has been cancelled'})

        else:
            return JsonResponse({'success': False, 'message': 'This order does not exist'})

    else:
        return JsonResponse({'success': False, 'message': 'This order does not exist'})


'''
@api_view(['POST',])
def show_address(request,userid):

	try:
		user_address = Userz.objects.filter(id = userid)[0:1].get()
		address = user_address.address

	except Address.DoesNotExist:
		user_address = None


	if user_address is not None:

'''
# this creates the address and the billing address for the user


@api_view(['POST', ])
def create_address(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        # address_serializer = UserzSerializer(data=request.data)
        # if address_serializer.is_valid():
        # 	address_serializer.save()

        # Create a billing address for that user
        billing_address = BillingAddress(
            user_id=user_id, address=request.data.get('address'))
        billing_address.save()
        billing_address_serializer = BillingAddressSerializer(
            billing_address, data=request.data)
        if billing_address_serializer.is_valid():
            billing_address_serializer.save()

        #addresses = [address_serializer.data,billing_address_serializer.data]
        return JsonResponse(address_serializer.data, safe=False, status=status.HTTP_201_CREATED)

    else:

        # address_serializer = UserzSerializer(data=request.data)
        # if address_serializer.is_valid():
        # 	address_serializer.save()

        # Create a billing address for that user
        billing_address = BillingAddress(
            non_verified_user_id=non_verified_user_id, address=request.data.get('address'))
        billing_address.save()
        billing_address_serializer = BillingAddressSerializer(
            billing_address, data=request.data)
        if billing_address_serializer.is_valid():
            billing_address_serializer.save()

        #addresses = [address_serializer.data,billing_address_serializer.data]
        return JsonResponse(billing_address_serializer.data, safe=False, status=status.HTTP_201_CREATED)


# This shows the address of the user in the form
@api_view(['POST', ])
def show_address(request):

    num = -1

    arr = {
        "id": num,
        "user_id": num,
        "date_created": "",
        "date_updated": "",
        "non_verified_user_id": num,
        "ip_address": "",
        "phone_number": "",
        "address": "",
        "area": "",
        "location": ""

    }

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            address = BillingAddress.objects.filter(user_id=user_id).last()

        except:
            address = None

        if address:
            billing_address_serializers = BillingAddressSerializer(
                address, many=False)
            return JsonResponse({'success': True, 'data': billing_address_serializers.data}, safe=False)

        else:
            # Fetching the exisitng user's address
            try:

                existing_address = Profile.objects.filter(
                    user_id=user_id).last()
            except:
                existing_address = None

            if existing_address:

                #billing_address = existing_address.address
                # phone_number = existing_address.phone_number
                # city = existing_address.city
                # district = existing_address.district
                # road_number = existing_address.road_number
                # building_number = existing_address.building_number
                # apartment_number = existing_address.apartment_numbe
                if existing_address.address:
                    print("1")
                    address = existing_address.address
                else:
                    address = ""
                if existing_address.phone_number:
                    print("2")
                    phone_number = existing_address.phone_number
                else:
                    phone_number = ""

                if existing_address.name:
                    print("3")
                    name = existing_address.name
                else:
                    name = ""
                if existing_address.area:
                    print("4")
                    area = existing_address.area
                else:
                    area = ""
                if existing_address.location:
                    print("5")
                    location = existing_address.location

                else:
                    location = ""
                # create a billing address
                billing_address_obj = BillingAddress.objects.create(
                    user_id=user_id, phone_number=phone_number, address=address, name=name, area=area, location=location)
                billing_address_obj.save()
                billing_serializer = BillingAddressSerializer(
                    billing_address_obj, data=request.data)
                if billing_serializer.is_valid():
                    billing_serializer.save()
                    return JsonResponse({'success': True, 'data': billing_serializer.data})
                else:
                    return JsonResponse(billing_serializer.errors)

            else:

                # billing_address_obj = BillingAddress.objects.create(user_id=user_id)
                # billing_address_obj.save()
                # billing_serializer = BillingAddressSerializer(billing_address_obj,data=request.data)
                # if billing_serializer.is_valid():
                # 	billing_serializer.save()
                return JsonResponse({'success': False, 'data': [arr]})
                # else:
                # 	return JsonResponse(billing_serializer.errors)

    else:
        print("Coming HERE")
        try:

            address = BillingAddress.objects.filter(
                non_verified_user_id=non_verified_user_id).last()
            # print(address)

        except:
            address = None

        if address is None:
            # print("Yessssss")
            return JsonResponse({'success': False, 'data': arr})

        else:
            #print("Coming here")
            billing_address_serializer = BillingAddressSerializer(address)
            return JsonResponse({'success': True, 'data': billing_address_serializer.data})


# this edits the billing address of a verified user and creates and edits the address of a non verified user
@api_view(['POST', ])
def edit_address(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            address = BillingAddress.objects.filter(user_id=user_id).last()
        except:
            address = None

        if address:

            billing_address_serializer = BillingAddressSerializer(
                address, data=request.data)
            if billing_address_serializer.is_valid():
                billing_address_serializer.save()
                return JsonResponse({'success': True, 'data': billing_address_serializer.data}, safe=False)

        else:

            # create a new billing address
            billing_address_serializer = BillingAddressSerializer(
                data=request.data)
            if billing_address_serializer.is_valid():
                billing_address_serializer.save()
                return JsonResponse({'success': True, 'data': billing_address_serializer.data}, safe=False)

        # else:
        # 	return JsonResponse({'success':False,'data':{}},safe=False)

    else:
        try:
            address = BillingAddress.objects.filter(
                non_verified_user_id=non_verified_user_id).last()
            if address is not None:

                billing_address_serializer = BillingAddressSerializer(
                    address, data=request.data)
                if billing_address_serializer.is_valid():
                    billing_address_serializer.save()
                    return JsonResponse({'success': True, 'data': billing_address_serializer.data})

            else:
                billing_address_serializer = BillingAddressSerializer(
                    data=request.data)
                if billing_address_serializer.is_valid():
                    billing_address_serializer.save()
                    return JsonResponse({'success': True, 'data': billing_address_serializer.data}, safe=False)

        except BillingAddress.DoesNotExist:
            return JsonResponse({'message': 'This address does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', ])
def check_coupon(request):

    current_date = timezone.now().date()
    coupon_percent = 0
    flag = False
    coupon_code = request.data.get('coupon_code')
    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            # Fetching the specific order of the specific user that hasnt been checked out
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=False)[0:1].get()
            print("HOITESE NAAAAAAAAAAAAA")
            print(specific_order)

        except:
            specific_order = None

        if specific_order is not None:
            print("hfeufhfgfwgyrgfrygr")
            specific_order.coupon_code = coupon_code
            specific_order.save()
            orderserializer = OrderSerializer(specific_order, request.data)
            if orderserializer.is_valid():
                orderserializer.save()

    else:
        try:

            # Fetching the specific order of the specific user that hasnt been checked out
            specific_order = Order.objects.filter(
                non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()
            print("HOITESE NAAAAAAAAAAAAA")
            print(specific_order)

        except:
            specific_order = None

        if specific_order is not None:
            print("hfeufhfgfwgyrgfrygr")
            specific_order.coupon_code = coupon_code
            specific_order.save()
            orderserializer = OrderSerializer(specific_order, request.data)
            if orderserializer.is_valid():
                orderserializer.save()

    coupons = Cupons.objects.all()
    coupon_codes = list(coupons.values_list('cupon_code', flat=True))
    coupon_amounts = list(coupons.values_list('amount', flat=True))
    coupon_start = list(coupons.values_list('start_from', flat=True))
    coupon_end = list(coupons.values_list('valid_to', flat=True))
    coupon_validity = list(coupons.values_list('is_active', flat=True))

    for i in range(len(coupon_codes)):
        if (coupon_codes[i] == coupon_code and current_date >= coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i] == True):

            coupon_percent = coupon_amounts[i]
            flag = True
            break
        else:
            flag = False

    if flag == True:
        return JsonResponse({'success': True, 'message': 'Promo code applied'})

    else:
        return JsonResponse({'success': False, 'message': 'Promo code is not applied'})


# This is for the Delivery API and the payment site
@api_view(['POST', ])
def send_info(request, order_id):

    data = request.data

    try:

        specific_order = Order.objects.get(id=order_id)

    except:

        specific_order = None

    if specific_order:

        if specific_order.user_id == -1:

            non_verified_user_id = specific_order.non_verified_user_id
            user_id = -1

        else:
            user_id = specific_order.user_id
            non_verified_user_id = -1

        if non_verified_user_id == -1:

            try:
                address = BillingAddress.objects.filter(user_id=user_id).last()
            except:
                address = None

            if address:

                address_serializer = BillingAddressSerializer(
                    address, many=False)

                address_data = address_serializer.data

            else:

                address_data = {}

        else:

            try:
                address = BillingAddress.objects.filter(
                    non_verified_user_id=non_verified_user_id).last()
            except:
                address = None

            if address:

                address_serializer = BillingAddressSerializer(
                    address, many=False)

                address_data = address_serializer.data

            else:

                address_data = {}

        order_serializer = OrderSerializer(specific_order, many=False)

        order_info = order_serializer.data

    else:

        order_info = {}
        address_data = {}

    try:

        company_info = CompanyInfo.objects.all()[0:1].get()

    except:

        company_info = None

    if company_info:

        company_name = company_info.name

    else:

        company_name = ""

    return JsonResponse({'success': True, 'message': 'Data is shown below', 'company_name': company_name, 'order_info': order_info, 'billing_address': address_data, 'other_info': data})


# Insertion for the the order info api
@api_view(['POST', ])
def order_info(request):

    order_info_serializer = OrderInfoSerializer(data=request.data)
    if order_info_serializer.is_valid():
        order_info_serializer.save()
        return JsonResponse({'success': True, 'message': 'Data has been inserted successfully', 'data': order_info_serializer.data})

    else:

        print(order_info_serializer.errors)
        return JsonResponse({'success': False, 'message': 'Data could not be inserted'})


# @api_view(['POST', ])
# def create_invoice(request, order_id):

#     data = {'order_id': order_id}

#     invoice_serializer = InvoiceSerializer(data=data)
#     if invoice_serializer.is_valid():
#         invoice_serializer.save()

#         invoice_data = invoice_serializer.data

#         # fetch the company Info

#         try:

#             company_info = CompanyInfo.objects.all()[0:1].get()

#         except:

#             company_info = None

#         if company_info:

#             company_info_serializer = CompanyInfoSerializer(
#                 company_info, many=False)
#             company_data = company_info_serializer.data

#         else:

#             company_data = {}

#         # Fetch the orderdetails

#         try:

#             specific_order = Order.objects.get(
#                 id=order_id, admin_status="Confirmed")

#         except:

#             specific_order = None

#         if specific_order:

#             order_serializer = OrderSerializer(specific_order, many=False)
#             order_data = order_serializer.data

#         else:

#             order_data = {}

#         # Fetch the billing address

#         try:

#             order_info = OrderInfo.objects.get(order_id=order_id)

#         except:

#             order_info = None

#         if order_info:

#             billing_address_id = order_info.billing_address_id

#             try:

#                 billing_address = BillingAddress.objects.get(
#                     id=billing_address_id)

#             except:

#                 billing_address = None

#             if billing_address:

#                 billing_address_serializer = BillingAddressSerializer(
#                     billing_address, many=False)
#                 billing_address_data = billing_address_serializer.data

#             else:

#                 billing_address_data = {}

#         else:

#             billing_address_data = {}

#         return JsonResponse({'success': True, 'message': 'Invoice created successfully', 'invoice_data': invoice_data, 'order_data': order_data, 'billing_address_data': billing_address_data, 'company_data': company_data})

#     else:

#         return JsonResponse({'sucess': False, 'message': 'Data is not inserted'})


# @api_view(['GET', ])
# def create_invoice(request, order_id):

#     # data = {'order_id': order_id}


#     # invoice_serializer = InvoiceSerializer(data=data)
#     # if invoice_serializer.is_valid():
#     #     invoice_serializer.save()

#     #     invoice_data = invoice_serializer.data

#     # fetch the company Info
#     print("fhbdufbdwufbdufbbw")
#     print(order_id)
#     try:
#         invoice = Invoice.objects.get(order_id= order_id,is_active=True)

#     except:

#         invoice = None

#     print('Invoice')


#     print(invoice)

#     if invoice:

#         invoice_serializer = InvoiceSerializer(invoice,many=False)

#         invoice_data = invoice_serializer.data


#         try:

#             company_info = CompanyInfo.objects.all()[0:1].get()

#         except:

#             company_info = None

#         if company_info:

#             company_info_serializer = CompanyInfoSerializer(
#                 company_info, many=False)
#             company_data = company_info_serializer.data

#         else:

#             company_data = {}

#         # Fetch the orderdetails

#         try:

#             specific_order = Order.objects.get(
#                 id=order_id, admin_status="Confirmed")

#         except:

#             specific_order = None

#         if specific_order:

#             order_serializer = OrderInvoiceSerializer(specific_order, many=False)
#             order_data = order_serializer.data

#         else:

#             order_data = {}

#         # Fetch the billing address

#         try:

#             order_info = OrderInfo.objects.get(order_id=order_id)

#         except:

#             order_info = None

#         if order_info:

#             billing_address_id = order_info.billing_address_id

#             try:

#                 billing_address = BillingAddress.objects.get(
#                     id=billing_address_id)

#             except:

#                 billing_address = None

#             if billing_address:

#                 billing_address_serializer = BillingAddressSerializer(
#                     billing_address, many=False)
#                 billing_address_data = billing_address_serializer.data

#             else:

#                 billing_address_data = {}

#         else:

#             billing_address_data = {}

#         return JsonResponse({'success': True, 'message': 'Invoice created successfully', 'invoice_data': invoice_data, 'order_data': order_data, 'billing_address_data': billing_address_data, 'company_data': company_data})

#     else:

#         return JsonResponse({'sucess': False, 'message': 'Invoice does not exist'})


@api_view(['GET', ])
def create_invoice(request, invoice_id):

    # data = {'order_id': order_id}

    # invoice_serializer = InvoiceSerializer(data=data)
    # if invoice_serializer.is_valid():
    #     invoice_serializer.save()

    #     invoice_data = invoice_serializer.data

    # fetch the company Info
    print("fhbdufbdwufbdufbbw")
    # print(order_id)
    try:
        invoice = Invoice.objects.get(id=invoice_id)

    except:

        invoice = None

    print('Invoice')

    print(invoice)

    if invoice:

        order_id = invoice.order_id

        reference_id = invoice.ref_invoice

        invoice_serializer = InvoiceSerializer(invoice, many=False)

        invoice_data = invoice_serializer.data

        try:

            company_info = CompanyInfo.objects.all()[0:1].get()

        except:

            company_info = None

        if company_info:

            company_info_serializer = CompanyInfoSerializer(
                company_info, many=False)
            company_data = company_info_serializer.data

        else:

            company_data = {}

        # Fetch the orderdetails

        try:

            specific_order = Order.objects.get(
                id=order_id, admin_status="Confirmed")

        except:

            specific_order = None

        if specific_order:

            if reference_id == 0:

                order_serializer = OrderInvoiceSerializer(
                    specific_order, many=False)
                order_data = order_serializer.data

            else:

                order_serializer = OrderInvoiceSerializer(
                    specific_order, many=False)
                order_data = order_serializer.data

        else:

            order_data = {}

        # Fetch the billing address

        try:

            order_info = OrderInfo.objects.filter(order_id=order_id).last()

        except:

            order_info = None

        print(order_id)

        print("Order info")
        print(order_info)

        if order_info:

            billing_address_id = order_info.billing_address_id

            try:

                billing_address = BillingAddress.objects.get(
                    id=billing_address_id)

            except:

                billing_address = None

            if billing_address:

                billing_address_serializer = BillingAddressSerializer(
                    billing_address, many=False)
                billing_address_data = billing_address_serializer.data

            else:

                billing_address_data = {}

        else:

            billing_address_data = {}

        return JsonResponse({'success': True, 'message': 'Invoice created successfully', 'invoice_data': invoice_data, 'order_data': order_data, 'billing_address_data': billing_address_data, 'company_data': company_data})

    else:

        return JsonResponse({'sucess': False, 'message': 'Invoice does not exist'})


@api_view(['POST', ])
def edit_invoice(request, invoice_id):

    # Checking if this is mother invoice or not

    data = {"invoice": [
        {
            "id": 1,
            "product_status": "Returned"
        },
        {
            "id": 2,
            "product_status": "Cancelled"
        }
    ],
        "stock": [{
            'product_id': 1,
            'specification_id': 1,
            'warehouse': [
                {
                    'warehouse_id': 1,
                    'quantity': 200

                },
                {
                    'warehouse_id': 2,
                    'quantity': 200

                }
            ],

            'shop': [
                {
                    'shop_id': 1,
                    'quantity': 200

                },
                {
                    'shop_id': 2,
                    'quantity': 200

                }


            ]

        },
        {
            'product_id': 1,
            'specification_id': 2,
            'warehouse': [
                {
                    'warehouse_id': 1,
                    'quantity': 200

                },
                {
                    'warehouse_id': 2,
                    'quantity': 200

                }
            ],

            'shop': [
                {
                    'shop_id': 1,
                    'quantity': 200

                },
                {
                    'shop_id': 2,
                    'quantity': 200

                }

            ]

        }

    ]
    }

    data = request.data

    stock_data = data["stock"]

    try:

        invoice = Invoice.objects.get(id=invoice_id)

    except:

        invoice = None

    invoice_ref_no = 0

    if invoice:

        order_id = invoice.order_id

        if invoice.ref_invoice:

            invoice_ref_no = invoice.ref_invoice

        else:

            invoice_ref_no = 0

        if invoice_ref_no == 0:

            invoice_data = data["invoice"]

            for i in range(len(invoice_data)):

                order_details_id = invoice_data[i]["id"]
                product_status = invoice_data[i]["product_status"]
                # order_id = invoice_data[i]["order_id"]

                # Fetching the orderdetails info

                try:

                    item = OrderDetails.objects.get(id=order_details_id)

                except:

                    item = None

                if item:

                    item.product_status = product_status

                    item.save()

                else:

                    return JsonResponse({"success": False, "message": "This item does not exist"})

            # Adding back the quantities

            flag = insert_product_quantity(stock_data)

            print(flag)

            if flag == True:

                # Create a new_invoice and make the existing invoice inactive

                # Making the exisitng invoice inactive

                invoice.is_active = False
                invoice.save()

                # Create an invoice

                new_invoice = Invoice.objects.create(
                    order_id=order_id, is_active=True, ref_invoice=invoice_id)
                new_invoice.save()

                return JsonResponse({"success": True, "message": "A new invoice has been created"})

            else:

                return JsonResponse({"success": False, "message": "The quantities could not be added back"})

        else:

            return JsonResponse({"success": False, "message": "This invoice cannot be edited"})

    else:

        return JsonResponse({"success": False, "message": "This invoice does not exist"})


def check_location(specification_id, billing_address_id):

    flag = False

    # print(specification_id)
    # print(billing_address_id)

    try:
        billing_address = BillingAddress.objects.get(id=billing_address_id)

    except:

        billing_address = None

    # print("billing address")

    # print(billing_address)

    if billing_address:

        area = billing_address.area
        location = billing_address.location

        # Checking product delivery area

        print("area")

        print(area)
        print(location)

        try:
            prod_delivery_area = product_delivery_area.objects.filter(
                specification_id=specification_id)

        except:

            prod_delivery_area = None

        # print(prod_delivery_area)

        if prod_delivery_area:

            # Finding if is_Bangladesg
            flags = list(prod_delivery_area.values_list(
                'is_Bangladesh', flat=True))
            # print(flags)
            if True in flags:

                flag = True
                return flag
                # return JsonResponse({"flag":flag},safe=False)

            # Finding all the delivery-area_ids

            delivery_area_ids = list(prod_delivery_area.values_list(
                'delivery_area_id', flat=True).distinct())
            delivery_area_names = []
            # print("delivery_area_ids")
            # print(delivery_area_ids)

            for i in range(len(delivery_area_ids)):

                # Fetching the area names

                try:
                    delivery_area = DeliveryArea.objects.get(
                        id=delivery_area_ids[i], is_active=True)

                except:
                    delivery_area = None

                if delivery_area:

                    area_name = delivery_area.Area_name
                    delivery_area_names.append(area_name)

                else:
                    pass

            print(delivery_area_names)

            if area in delivery_area_names:

                # print("area ase")

                for i in range(len(delivery_area_ids)):

                    # Find out the location_ids

                    try:
                        delivery_loc = product_delivery_area.objects.get(
                            specification_id=specification_id, delivery_area_id=delivery_area_ids[i])

                    except:

                        delivery_loc = None

                    # print("delivery_loc_object")
                    # print(delivery_loc)

                    if delivery_loc:

                        delivery_location_ids = delivery_loc.delivery_location_ids
                        delivery_location_names = []
                        # print("delivery_location_ids")
                        # print(delivery_location_ids)

                        for j in range(len(delivery_location_ids)):

                            # Fetch the names
                            try:
                                deli_loc = DeliveryLocation.objects.get(
                                    id=delivery_location_ids[j], is_active=True)

                            except:
                                deli_loc = None

                            # print(deli_loc)

                            if deli_loc:

                                loc_name = deli_loc.location_name
                                delivery_location_names.append(loc_name)

                            else:
                                pass

                        if location in delivery_location_names:

                            flag = True
                            return flag
                            # return JsonResponse({"flag":flag},safe=False)

                        else:
                            pass

                    else:
                        pass

                if flag == True:
                    return flag
                    # return JsonResponse({"flag":flag},safe=False)

                else:

                    return flag
                    # return JsonResponse({"flag":flag},safe=False)

            else:

                return flag
                # return JsonResponse({"flag":flag},safe=False)

            # delivery_area_id = prod_delivery_area.delivery_area_id
            # delivery_location_ids = prod_delivery_area.delivery_location_ids

            # To see if the area exists

        else:

            return flag
            # return JsonResponse({"flag":flag},safe=False)

    else:

        return flag
        # return JsonResponse({"flag":flag},safe=False)


@api_view(['POST', ])
def check_delivery_location(request, order_id):

    # user_id = request.data.get('user_id')
    billing_address_id = request.data.get('billing_address_id')
    try:
        billing_addr = BillingAddress.objects.get(id=billing_address_id)
    except:
        billing_addr = None 

    if billing_addr:
        area = billing_addr.area
        location = billing_addr.location
    else:
        area = ""
        location = ""
    #coupon_code = request.data.get('coupon_code')
    # print(type(coupon_code))
    # non_verified_user_id = request.data.get('non_verified_user_id')
    # if user_id is not None:
    #     user_id = int(user_id)
    #     non_verified_user_id = 0

    # else:
    #     non_verified_user_id = int(non_verified_user_id)
    #     user_id = 0

    # flag = False
    # product_name = ""
    # product_quantity = 0
    # current_quantity = 0
    # current_color = ""
    # current_size = ""
    # current_unit = ""
    # current_name = ""

    # if non_verified_user_id == 0:

    print(area)
    print(location)

    try:
        # Fetching the specific order of the specific user that hasnt been checked out
        specific_order = Order.objects.get(id=order_id)

    except:
        specific_order = None

    if specific_order is not None:

        # specific_order.checkout_status = True
        # specific_order.order_status = "Unpaid"
        # specific_order.delivery_status = "To pay"
        # specific_order.ordered_date = datetime.now()
        # specific_order.save()
        orders_id = specific_order.id
        orders_details = OrderDetails.objects.filter(
            order_id=orders_id, is_removed=False, delivery_removed=False)

        order_det_ids = orders_details.values_list('id', flat=True)
        print(order_det_ids)

        not_delivered = []

        undelivered_items = []

        for i in range(len(order_det_ids)):

            try:

                order_dets = OrderDetails.objects.get(id=order_det_ids[i])

            except:

                order_dets = None

            if order_dets:

                spec_id = order_dets.specification_id

                try:
                    pro_spec = ProductSpecification.objects.get(id=spec_id)
                except:
                    pro_spec = None

                if pro_spec:
                    is_own = pro_spec.is_own
                    mother_specification_id = pro_spec.mother_specification_id
                else:
                    return JsonResponse({"success":False})

                if is_own == True:

                    print("my own product")

                    check_loc = check_location(spec_id, billing_address_id)

                else:
                    print("not my own product")

                    url = site_path + "Cart/check_mother_site_location/" +str(mother_specification_id)+ "/" +str(area)+ "/"  + str(location)+ "/"
                    print(url)
                    own_response = requests.get(url = url)
                    print(own_response)
                    if str(own_response) == "<Response [500]>":
                        return JsonResponse({"success":False,"message":"Mother site did not respond"})
                    own_response = own_response.json()
                    print(own_response)

                    own_flag = own_response["flag"]
                    print(own_flag)
                    check_loc = own_flag


                print(order_dets.id)

                print("chceck_loc")

                print(check_loc)

                if check_loc == False:

                    not_delivered.append(order_dets.product_name)

                    item_serializer = OrderDetailsSerializer1(
                        order_dets, many=False)

                    undelivered_items.append(item_serializer.data)

                    order_dets.delivery_removed = True
                    order_dets.save()

                    # order_dets.delete()

                    # order_dets.delivery_removed = True

                    # order_dets.save()

        # Fetch the areas and location

        try:

            bill_address = BillingAddress.objects.get(id=billing_address_id)

        except:

            bill_address = None

        if bill_address:

            area = bill_address.area
            location = bill_address.location

        else:

            area = ""
            location = ""
        print("messssageeeeee")
        print(not_delivered)

        if len(not_delivered) > 0:

            product_message = ""

            # for k in range(len(not_delivered)):

            if len(not_delivered) == 1:

                product_message = not_delivered[0]

            elif len(not_delivered) > 1:

                for x in range(len(not_delivered)):

                    product_message = product_message + not_delivered[x] + ", "

            print(product_message)

            new_product_message = product_message

            delivery_message = new_product_message + \
                " are not available in location:"+location+" of area:"+area

        else:

            delivery_message = ""

        specific_orderz = Order.objects.get(id=order_id)
        order_serializer = OrderSerializer3(specific_orderz, many=False)
        order_data = order_serializer.data

        if len(order_data["orders"]) > 0:

            return JsonResponse({"success": True, "message": 'Your products are shown', "delivery_message": delivery_message, "data": order_data, "undelivered_items": undelivered_items})

        else:

            return JsonResponse({"success": False, "message": 'None of your products are available in the location you want them to be delivered to', "delivery_message": delivery_message, "data": order_data, "undelivered_items": undelivered_items})


def insert_product_quantity(data):

    api_values = data

    # api_values = [{
    #     'product_id':1,
    #     'specification_id':1,
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
    #             'shop_id': 1,
    #             'quantity': 200

    #         },
    #         {
    #             'shop_id': 2,
    #             'quantity': 200

    #         }

    #     ]

    #     },
    #     {
    #     'product_id':1,
    #     'specification_id':2,
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
    #             'shop_id': 1,
    #             'quantity': 200

    #         },
    #         {
    #             'shop_id': 2,
    #             'quantity': 200

    #         }

    #     ]

    #     }

    #     ]

    # api_values = request.data
    current_date = date.today()
    flag = 1

    for i in range(len(api_values)):

        try:

            # checking is there any warehouse data exists or not
            if len(api_values[i]['warehouse']) > 0:
                for wareh in api_values[i]['warehouse']:
                    try:
                        # getting the previous data if there is any in the similar name. If exists update the new value. if does not create new records.
                        wareh_query = WarehouseInfo.objects.filter(
                            warehouse_id=wareh['warehouse_id'], specification_id=api_values[i]['specification_id']).last()

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

                            new_quantity = warehouse_quantity + \
                                int(wareh['quantity'])

                            print(new_quantity)

                            wareh_query.quantity = new_quantity
                            print(wareh_query.quantity)
                            wareh_query.save()
                            print(wareh_query.quantity)

                            try:
                                product_spec = ProductSpecification.objects.get(
                                    id=api_values[i]['specification_id'])

                            except:
                                product_spec = None

                            if product_spec:

                                product_spec.save()

                        else:
                            print("else ey dhuktese")
                            wareh_data = WarehouseInfo.objects.create(specification_id=api_values[i]['specification_id'], product_id=api_values[i]['product_id'], warehouse_id=wareh['warehouse_id'],
                                                                      quantity=int(wareh['quantity']))
                            wareh_data.save()

                            try:
                                product_spec = ProductSpecification.objects.get(
                                    id=api_values[i]['specification_id'])

                            except:
                                product_spec = None

                            if product_spec:

                                product_spec.save()

                        # updating the inventory report credit records for each ware house quantity. It will help to keep the records in future.
                        # report_data = inventory_report(
                        #     product_id=api_values['product_id'], credit=wareh['quantity'], warehouse_id=wareh['warehouse_id'])
                        # report_data.save()
                        # Check to see if there are any inventory_reports
                        try:

                            report = inventory_report.objects.filter(
                                product_id=api_values[i]['product_id'], specification_id=api_values[i]['specification_id'], warehouse_id=wareh['warehouse_id'], date=current_date).last()

                        except:

                            report = None

                        if report:

                            # Update the existing report

                            report.credit += int(wareh['quantity'])
                            report.save()

                        else:
                            # Create a new row

                            new_report = inventory_report.objects.create(product_id=api_values[i]['product_id'], specification_id=api_values[
                                                                         i]['specification_id'], warehouse_id=wareh['warehouse_id'], credit=int(wareh['quantity']), date=current_date)
                            new_report.save()

                    except:
                        pass

            else:
                pass

            if len(api_values[i]['shop']) > 0:
                for shops in api_values[i]['shop']:
                    try:
                        # getting the existing shop values if is there any.
                        print(shops['shop_id'])
                        shop_query = ShopInfo.objects.filter(
                            shop_id=shops['shop_id'], specification_id=api_values[i]['specification_id']).last()
                        print(shop_query)
                        if shop_query:
                            print("shop ase")
                            quantity_val = shop_query.quantity
                            new_quantity = quantity_val + \
                                int(shops['quantity'])
                            # shop_query.update(quantity=new_quantity)
                            shop_query.quantity = new_quantity
                            shop_query.save()

                            try:
                                product_spec = ProductSpecification.objects.get(
                                    id=api_values[i]['specification_id'])

                            except:
                                product_spec = None

                            if product_spec:

                                product_spec.save()
                        else:
                            print("shop nai")
                            shop_data = ShopInfo.objects.create(specification_id=api_values[i]['specification_id'], product_id=api_values[i]['product_id'], shop_id=shops['shop_id'],
                                                                quantity=int(shops['quantity']))
                            shop_data.save()
                        # Updating the report table after being inserted the quantity corresponding to credit coloumn for each shop.
                        # report_data = inventory_report(
                        #     product_id=api_values['product_id'], credit=shops['quantity'], shop_id=shops['shop_id'])
                        # report_data.save()

                            try:
                                product_spec = ProductSpecification.objects.get(
                                    id=api_values[i]['specification_id'])

                            except:
                                product_spec = None

                            if product_spec:

                                product_spec.save()

                        try:

                            report = inventory_report.objects.filter(
                                product_id=api_values[i]['product_id'], specification_id=api_values[i]['specification_id'], shop_id=shop['shop_id'], date=current_date).last()

                        except:

                            report = None

                        if report:

                            # Update the existing report

                            report.credit += int(shops['quantity'])
                            report.save()

                        else:
                            # Create a new row

                            new_report = inventory_report.objects.create(
                                product_id=api_values[i]['product_id'], specification_id=api_values[i]['specification_id'], shop_id=shops['shop_id'], credit=int(shops['quantity']), date=current_date)
                            new_report.save()
                    except:
                        pass

            else:
                pass

            # return Response({
            #     "success": True,
            #     "message": "Data has been added successfully"
            # })

            flag = 0
        except:
            flag = 1
            return False
            # return Response({
            #     "success": False,
            #     "message": "Something went wrong !!"
            # })

    if flag == 0:

        return True

    else:

        return False

        # return JsonResponse({"success":True,"message":"Data inserted successfully"})


@api_view(['GET', ])
def sales_report(request):

    try:
        specific_sales = OrderDetails.objects.filter(admin_status="Approved")
    except:
        specific_sales = None

    if specific_sales:

        salesserializers = SalesSerializer(specific_sales, many=True)

        return JsonResponse({'success': True, 'message': 'The Sales Report  are shown', 'data': salesserializers.data}, safe=False)

    else:
        return JsonResponse({'success': False, 'message': 'You have no Sales Report'})


@api_view(['POST', ])
def create_order(request, seller_id):

    # values =  [{
    #         "id": 28,
    #         "product_id": 14,
    #         "color": "none",
    #         "size": "none",
    #         "weight": "1",
    #         "unit": "pcs",
    #         "seller_selling_quantity":30,
    #         "seller_selling_price":150,
    #         "weight_unit": "1pcs",
    #         "warranty": "1",
    #         "warranty_unit": "year",
    #         "vat": 0.0,
    #         "quantity": 900631,
    #         "seller_quantity": 0,
    #         "remaining": 0,
    #         "SKU": "N/A",
    #         "barcode": "N/A",
    #         "new_price": "250.00",
    #         "old_price": "250.00",
    #         "purchase_price": "180.00",
    #         "price": {
    #             "id": 28,
    #             "product_id": 14,
    #             "specification_id": 28,
    #             "price": 250.0,
    #             "purchase_price": 180.0,
    #             "date_added": "2020-10-29T17:53:44.076000+06:00",
    #             "currency_id": -1
    #         },
    #         "discount": {
    #             "id": 16,
    #             "discount_type": "amount",
    #             "amount": 118.0,
    #             "start_date": "2020-10-29",
    #             "end_date": "2020-10-29",
    #             "max_amount": 0.0,
    #             "group_product_id": "",
    #             "product_id": 14,
    #             "specification_id": 28,
    #             "is_active": True
    #         },
    #         "point": {
    #             "id": 22,
    #             "point": 10.0,
    #             "product_id": 14,
    #             "specification_id": 28,
    #             "start_date": "2020-10-30",
    #             "is_active": True,
    #             "end_date": "2020-12-04"
    #         },
    #         "delivery_info": {},
    #         "manufacture_date": "",
    #         "expire": "",
    #         "product_name": "Cosmic Easy car wax",
    #         "product_brand": "Kangaroo"
    #     },
    #     {
    #         "id": 87,
    #         "product_id": 7,
    #         "color": "light-blue",
    #         "size": "M",
    #         "weight": "1000",
    #         "unit": "gm",
    #         "seller_selling_quantity":30,
    #         "seller_selling_price":200,
    #         "weight_unit": "1000gm",
    #         "warranty": "1",
    #         "warranty_unit": "none",
    #         "vat": 10.0,
    #         "quantity": 0,
    #         "seller_quantity": 0,
    #         "remaining": 0,
    #         "SKU": "N/A",
    #         "barcode": "N/A",
    #         "new_price": "886.00",
    #         "old_price": "886.00",
    #         "purchase_price": "5675.00",
    #         "price": {
    #             "id": 87,
    #             "product_id": 7,
    #             "specification_id": 87,
    #             "price": 886.0,
    #             "purchase_price": 5675.0,
    #             "date_added": "2020-11-04T17:40:10.194000+06:00",
    #             "currency_id": -1
    #         },
    #         "discount": {
    #             "id": 49,
    #             "discount_type": "amount",
    #             "amount": 10.0,
    #             "start_date": "2020-11-04",
    #             "end_date": "2020-11-04",
    #             "max_amount": 0.0,
    #             "group_product_id": "",
    #             "product_id": 7,
    #             "specification_id": 87,
    #             "is_active": ""
    #         },
    #         "point": {
    #             "id": 47,
    #             "point": 10.0,
    #             "product_id": 7,
    #             "specification_id": 87,
    #             "start_date": "2020-11-12",
    #             "is_active": "",
    #             "end_date": "2020-11-05"
    #         },
    #         "delivery_info": {},
    #         "manufacture_date": "",
    #         "expire": "",
    #         "product_name": "Cosmics Leather & tire Wax",
    #         "product_brand": "Kangaroo"
    #     },
    #     {
    #         "id": 45,
    #         "product_id": 7,
    #         "color": "deep-purple",
    #         "size": "none",
    #         "weight": "2",
    #         "seller_selling_quantity":20,
    #         "seller_selling_price":100,
    #         "unit": "pcs",
    #         "weight_unit": "2pcs",
    #         "warranty": "1",
    #         "warranty_unit": "year",
    #         "vat": 10.0,
    #         "quantity": 176312,
    #         "seller_quantity": 0,
    #         "remaining": 0,
    #         "SKU": "N/A",
    #         "barcode": "N/A",
    #         "new_price": "70.00",
    #         "old_price": "70.00",
    #         "purchase_price": "200.00",
    #         "price": {
    #             "id": 45,
    #             "product_id": 7,
    #             "specification_id": 45,
    #             "price": 70.0,
    #             "purchase_price": 200.0,
    #             "date_added": "2020-10-29T19:20:31.914000+06:00",
    #             "currency_id": -1
    #         },
    #         "discount": {
    #             "id": 42,
    #             "discount_type": "amount",
    #             "amount": 200.0,
    #             "start_date": "2020-11-01",
    #             "end_date": "2020-11-01",
    #             "max_amount": 0.0,
    #             "group_product_id": "",
    #             "product_id": 7,
    #             "specification_id": 45,
    #             "is_active": True
    #         },
    #         "point": {},
    #         "delivery_info": {},
    #         "manufacture_date": "",
    #         "expire": "",
    #         "product_name": "Cosmics Leather & tire Wax",
    #         "product_brand": "Kangaroo"
    #     }
    # ]

    values = request.data

    try:

        # Create an order

        order_data = {"user_id": seller_id, "is_seller": True}

        order = OrderSerializer(data=order_data)
        if order.is_valid():
            order.save()

            order_id = int(order.data["id"])

        else:
            print(order.errors)

        print("Order)id")

        print(order_id)

        # order = Order.objects.create(user_id=seller_id,is_seller=True)
        # order.save()

        # order_id = order.id

        # Create orderdetails

        if len(values) > 0:

            for i in range(len(values)):
                print("specification_iddddd")
                print(values[i]["id"])

                product_id = values[i]["product_id"]
                try:
                    product = Product.objects.get(id=product_id)

                except:
                    product = None

                if product:
                    if product.title:
                        product_name = product.title
                    else:
                        product_name = ""

                else:
                    product_name = ""
                name = product_name
                specification_id = int(values[i]["id"])
                total_quantity = int(values[i]["seller_selling_quantity"])
                unit_price = int(values[i]["seller_selling_price"])
                total_price = total_quantity*unit_price

                print(order_id)
                print(specification_id)

                # create an orderdetails object

                # order_dets = OrderDetails.objects.create(order_id=order_id,product_id=product_id,unit_price=unit_price,total_price=total_price,total_quantity=total_quantity,specification_id=specification_id)
                # order_dets.save()
                order_details_data = {"order_id": order_id, "product_id": product_id, "specification_id": specification_id,
                                      "total_quantity": total_quantity, "unit_price": unit_price, "total_price": total_price, "product_name": name}
                print(order_details_data)
                order_dets = OrderDetailsSerializer(data=order_details_data)
                if order_dets.is_valid():
                    order_dets.save()

                else:
                    print(order_dets.errors)

            # Create an invoice

            invoice = Invoice.objects.create(order_id=order_id)
            invoice.save()
            invoice_id = invoice.id

            return JsonResponse({"success": True, "message": "An order and an invoice has been created", "invoice_id": invoice_id})

        else:

            return JsonResponse({"success": False, "message": "No products were added to this order"})

    except:

        return JsonResponse({"success": False, "message": "Something went wrong"})


@api_view(['POST', ])
def seller_invoices(request, seller_id):

    types = request.data.get("type")

    if types == "Pending":

        try:
            order = Order.objects.filter(
                is_seller=True, user_id=seller_id, admin_status="Processing")

        except:

            order = None

        if order:

            order_serializer = PurchaseInvoiceSerializer(order, many=True)
            order_data = order_serializer.data

        else:

            order_data = []

    elif types == "Approved":

        try:
            order = Order.objects.filter(
                is_seller=True, user_id=seller_id, admin_status="Confirmed")

        except:

            order = None

        if order:

            order_serializer = PurchaseInvoiceSerializer(order, many=True)
            order_data = order_serializer.data

        else:

            order_data = []

    elif types == "Cancelled":

        try:
            order = Order.objects.filter(
                is_seller=True, user_id=seller_id, admin_status="Cancelled")

        except:

            order = None

        if order:

            order_serializer = PurchaseInvoiceSerializer(order, many=True)
            order_data = order_serializer.data

        else:

            order_data = []

    elif types == "All":

        try:
            order = Order.objects.filter(is_seller=True, user_id=seller_id)

        except:

            order = None

        if order:

            order_serializer = PurchaseInvoiceSerializer(order, many=True)
            order_data = order_serializer.data

        else:

            order_data = []

    else:

        order_data = []

    if order_data == []:

        return JsonResponse({"success": False, "message": "Data doesnt exist"})

    else:

        return JsonResponse({"success": True, "message": "Data is shown", "data": order_data})


@api_view(['GET', ])
def seller_individual_invoice(request, invoice_id):

    # data = {'order_id': order_id}

    # invoice_serializer = InvoiceSerializer(data=data)
    # if invoice_serializer.is_valid():
    #     invoice_serializer.save()

    #     invoice_data = invoice_serializer.data

    # fetch the company Info
    print("fhbdufbdwufbdufbbw")
    user_id = 0
    # print(order_id)
    try:
        invoice = Invoice.objects.get(id=invoice_id)

    except:

        invoice = None

    print('Invoice')

    print(invoice)

    if invoice:

        order_id = invoice.order_id

        reference_id = invoice.ref_invoice

        invoice_serializer = InvoiceSerializer(invoice, many=False)

        invoice_data = invoice_serializer.data

        try:

            company_info = CompanyInfo.objects.all()[0:1].get()

        except:

            company_info = None

        if company_info:

            company_info_serializer = CompanyInfoSerializer(
                company_info, many=False)
            company_data = company_info_serializer.data

        else:

            company_data = {}

        # Fetch the seller info

        # try:
        #     user_info = User.objects.get(id=)

        # Fetch the orderdetails

        try:

            specific_order = Order.objects.get(
                id=order_id)

        except:

            specific_order = None

        if specific_order:

            user_id = specific_order.user_id

            if reference_id == 0:

                order_serializer = PurchaseInvoiceSerializer(
                    specific_order, many=False)
                order_data = order_serializer.data

            else:

                order_serializer = PurchaseInvoiceSerializer(
                    specific_order, many=False)
                order_data = order_serializer.data

        else:

            order_data = {}

        # Fetch the user_info

        try:

            user_info = User.objects.get(id=user_id)

        except:

            user_info = None

        if user_info:

            if user_info.email:

                seller_email = user_info.email

            else:

                seller_email = ""

            if user_info.phone_number:

                seller_phone = user_info.phone_number

            else:

                seller_phone = ""

        else:
            seller_email = ""

            seller_phone = ""

        seller_info = {"seller_email": seller_email,
                       "seller_phone": seller_phone}

        # Fetch the billing address

        # try:

        #     order_info = OrderInfo.objects.get(order_id=order_id)

        # except:

        #     order_info = None

        # if order_info:

        #     billing_address_id = order_info.billing_address_id

        #     try:

        #         billing_address = BillingAddress.objects.get(
        #             id=billing_address_id)

        #     except:

        #         billing_address = None

        #     if billing_address:

        #         billing_address_serializer = BillingAddressSerializer(
        #             billing_address, many=False)
        #         billing_address_data = billing_address_serializer.data

        #     else:

        #         billing_address_data = {}

        # else:

        #     billing_address_data = {}

        return JsonResponse({'success': True, 'message': 'Invoice created successfully', 'invoice_data': invoice_data, 'order_data': order_data,  'seller_info': seller_info, 'company_info': company_data})

    else:

        return JsonResponse({'sucess': False, 'message': 'Invoice does not exist'})


@api_view(['POST', ])
def admin_seller_invoices(request):

    data = request.data

    types = data["type"]

    print(types)

    if types == "Pending":

        try:
            order = Order.objects.filter(
                is_seller=True, admin_status="Processing")

        except:

            order = None

        if order:

            order_serializer = PurchaseInvoiceSerializer(order, many=True)
            order_data = order_serializer.data

        else:

            order_data = []

    elif types == "Approved":

        try:
            order = Order.objects.filter(
                is_seller=True, admin_status="Confirmed")

        except:

            order = None

        if order:

            order_serializer = PurchaseInvoiceSerializer(order, many=True)
            order_data = order_serializer.data

        else:

            order_data = []

    elif types == "Cancelled":

        try:
            order = Order.objects.filter(
                is_seller=True, admin_status="Cancelled")

        except:

            order = None

        if order:

            order_serializer = PurchaseInvoiceSerializer(order, many=True)
            order_data = order_serializer.data

        else:

            order_data = []

    elif types == "All":

        try:
            order = Order.objects.filter(is_seller=True)

        except:

            order = None

        print(order)

        if order:

            order_serializer = PurchaseInvoiceSerializer(order, many=True)
            order_data = order_serializer.data

        else:

            order_data = []

    else:

        order_data = []

    if order_data == []:

        return JsonResponse({"success": False, "message": "Data doesnt exist"})

    else:

        return JsonResponse({"success": True, "message": "Data is shown", "data": order_data})


# This shows the information of the a specific
@api_view(['POST', ])
def individual_orders(request):

    # user_id = request.data.get('user_id')
    # non_verified_user_id = request.data.get('non_verified_user_id')
    # if user_id is not None:
    # 	user_id = int(user_id)
    # 	non_verified_user_id =0

    # else:
    # 	non_verified_user_id = int(non_verified_user_id)
    # 	user_id = 0

    # if non_verified_user_id == 0:

    try:
        search_by = request.data.get("searchBy")
        search = request.data.get("search")

        if search_by == "Invoice Number":

            search_number = int(search)

            try:
                invoice = Invoice.objects.get(id=search_number)
            except:
                invoice = None

            if invoice:
                if invoice.order_id:
                    order_id = invoice.order_id
                else:
                    order_id = 0

                try:
                    specific_order = Order.objects.get(id=order_id)
                except:
                    specific_order = None

                if specific_order:
                    order_serializer = OrderSerializer(
                        specific_order, many=False)
                    order_data = [order_serializer.data]
                    return JsonResponse({"success": True, "message": "Data is shown", "data": order_data})

                else:
                    return JsonResponse({"success": False, "message": "This order does not exist"})

            else:
                return JsonResponse({"success": False, "message": "This invoice does not exist"})

        elif search_by == "Phone Number":

            print("phone number dise")

            try:

                billing_addresses = BillingAddress.objects.filter(
                    phone_number=search)

            except:

                billing_addresses = None

            if billing_addresses:

                billing_address_ids = list(
                    billing_addresses.values_list('id', flat=True))

            else:

                billing_address_ids = []

            try:
                order_infos = OrderInfo.objects.filter(
                    billing_address_id__in=billing_address_ids)

            except:
                order_infos = None

            if order_infos:

                order_ids = list(
                    order_infos.values_list('order_id', flat=True))

            else:

                order_ids = []

            try:
                orders = Order.objects.filter(id__in=order_ids)

            except:
                orders = None

            if orders:

                order_serializer = OrderSerializer(orders, many=True)
                order_data = order_serializer.data
                return JsonResponse({"success": True, "message": "Data is shown", "data": order_data})

            else:
                return JsonResponse({"success": False, "message": "There are no orders to show"})

    except:
        return JsonResponse({"success": False, "message": "Something went wrong"})


@api_view(['POST', ])
def checkout_data(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=True).last()
        except:
            specific_order = None

        if specific_order:
            order_id = specific_order.id

            orderserializer = OrderSerializer3(specific_order, many=False)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]
            #Make mothersite order
       
            mothersite_data = find_mother_products(order_id)
            print(mothersite_data)
            mothersite_data = json.dumps(mothersite_data)
            print(mothersite_data)
 
            url = site_path + "Cart/create_childsite_orders/" 
            headers = {'Content-Type': 'application/json'}
            mother_response = requests.post(url = url, headers=headers, data= mothersite_data)
            response_status = str(mother_response)
            if response_status == "<Response [200]>":
                mother_response = mother_response.json()
                if mother_response["success"] == True:
                    return JsonResponse({'success': True, 'message': 'The products in your orders are shown', 'data': orderserializer.data}, safe=False)

                else:
                    return JsonResponse({"success":False,"message":"Mothersite order could not be created"})

            else:
                return JsonResponse({"success":False,"message":"Mothersite did not respond"})


  
            

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})

    else:

        try:
            specific_order = Order.objects.filter(
                non_verified_user_id=non_verified_user_id, checkout_status=True).last()
        except:
            specific_order = None
            

        if specific_order:

            order_id = specific_order.order

            orderserializer = OrderSerializer3(specific_order, many=False)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

            #orders = [orderserializer.data , orderdetailserializer.data]

            mothersite_data = find_mother_products(order_id)
            mothersite_data = json.dumps(mothersite_data)
 
            url = site_path + "Cart/create_childsite_orders/" 
            headers = {'Content-Type': 'application/json'}
            mother_response = requests.post(url = url, headers=headers ,data= mothersite_data)
            response_status = str(mother_response)
            if response_status == "<Response [200]>":
                mother_response = mother_response.json()
                if mother_response["success"] == True:
                    return JsonResponse({'success': True, 'message': 'The products in your orders are shown', 'data': orderserializer.data}, safe=False)

                else:
                    return JsonResponse({"success":False,"message":"Mothersite order could not be created"})

            else:
                return JsonResponse({"success":False,"message":"Mothersite did not respond"})
      

            

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})


# @api_view(['POST', ])
# def checkout(request):


#     user_id = request.data.get('user_id')
#     billing_address_id = request.data.get('billing_address')
#     #coupon_code = request.data.get('coupon_code')
#     # print(type(coupon_code))
#     non_verified_user_id = request.data.get('non_verified_user_id')
#     if user_id is not None:
#         user_id = int(user_id)
#         non_verified_user_id = 0

#     else:
#         non_verified_user_id = int(non_verified_user_id)
#         user_id = 0

#     flag = False
#     product_name = ""
#     product_quantity = 0
#     current_quantity = 0
#     current_color = ""
#     current_size = ""
#     current_unit = ""

#     if non_verified_user_id == 0:

#         try:
#             # Fetching the specific order of the specific user that hasnt been checked out
#             specific_order = Order.objects.filter(
#                 user_id=user_id, checkout_status=False)[0:1].get()

#         except:
#             specific_order = None

#         if specific_order is not None:

#             # specific_order.checkout_status = True
#             # specific_order.order_status = "Unpaid"
#             # specific_order.delivery_status = "To pay"
#             # specific_order.ordered_date = datetime.now()
#             # specific_order.save()
#             order_id = specific_order.id
#             order_details = OrderDetails.objects.filter(
#                 order_id=order_id, is_removed=False)
#             order_ids = order_details.values_list('id', flat=True)
#             order_products = order_details.values_list('product_id', flat=True)
#             order_specs = order_details.values_list(
#                 'specification_id', flat=True)
#             order_colors = order_details.values_list(
#                 'product_color', flat=True)
#             order_sizes = order_details.values_list('product_size', flat=True)
#             #order_units = order_details.values_list('product_unit',flat = True)
#             order_names = order_details.values_list('product_name', flat=True)
#             order_quantity = order_details.values_list(
#                 'total_quantity', flat=True)
#             print(order_ids)
#             for i in range(len(order_ids)):
#                 print("dhuklam")
#                 print(order_sizes[i])
#                 print(order_colors[i])
#                 # print(order_units[i])
#                 product = ProductSpecification.objects.get(id=order_specs[i])
#                 if product:
#                     product_quantity = product.quantity

#                 else:
#                     product_quantity = 0

#                 print("Ashchi")
#                 # print(product.title)
#                 # print(product.quantity)
#                 product_name = order_names[i]
#                 product_color = order_colors[i]
#                 product_size = order_sizes[i]
#                 #product_unit = order_units[i]
#                 if order_quantity[i] > product_quantity:
#                     current_quantity = product_quantity
#                     current_name = product_name
#                     current_color = product_color
#                     current_size = product_size
#                     #current_unit = product_unit
#                     flag = False
#                     break
#                 else:
#                     flag = True

#             print(flag)

#             if flag == True:
#                 print("cjeck kora possible")

#                 # change the coupon
#                 # if coupon_code == '':
#                 #     specific_order.coupon_code =
#                 # else:
#                 #     specific_order.coupon = True

#                 # user can checkout
#                 #specific_order.coupon_code = coupon_code
#                 specific_order.checkout_status = True
#                 specific_order.order_status = "Unpaid"
#                 specific_order.delivery_status = "To ship"
#                 specific_order.ordered_date = timezone.now()
#                 specific_order.save()

#                 for i in range(len(order_products)):
#                     product = ProductSpecification.objects.get(
#                         id=order_specs[i])
#                     product_quantity = product.quantity
#                     product.quantity -= order_quantity[i]
#                     product.save()
#                     productserializer = ProductSpecificationSerializer(
#                         product, data=request.data)
#                     print("fuhfuwhuhfuewhewuhew")
#                     if productserializer.is_valid():
#                         print("ffbwybwbfywefbweyfbefb")
#                         productserializer.save()

#                         sales_count = 0
#                         try:
#                             product_impression = ProductImpression.objects.filter(
#                                 product_id=order_products[i])[0:1].get()
#                             print(product_impression)
#                         except:
#                             product_impression = None

#                         if ProductImpression is None:
#                             print("hochche na")
#                             pass
#                         else:
#                             print("hochche")
#                             product_impression.sales_count += order_quantity[i]
#                             product_impression.save()

#                             print(product_impression.sales_count)
#                     else:
#                         print("erroesssss")
#                         return JsonResponse(productserializer.errors)

#                 return JsonResponse({'success': True, 'message': 'The items have been checked out'})

#             else:

#                 message = "You cannot checkout.We only have "+str(current_quantity)+" of item "+str(
#                     current_name)+" of color "+str(current_color)+" of size "+str(current_size)+" in our stock currently."
#                 return JsonResponse({'success': False, 'message': message})

#         else:
#             return JsonResponse({'success': False, 'message': 'This order does not exist'})

#     else:

#         try:
#             # Fetching the specific order of the specific user that hasnt been checked out
#             specific_order = Order.objects.filter(
#                 non_verified_user_id=non_verified_user_id, checkout_status=False)[0:1].get()

#         except:
#             specific_order = None

#         if specific_order is not None:

#             # specific_order.checkout_status = True
#             # specific_order.order_status = "Unpaid"
#             # specific_order.delivery_status = "To pay"
#             # specific_order.ordered_date = datetime.now()
#             # specific_order.save()
#             order_id = specific_order.id
#             order_details = OrderDetails.objects.filter(
#                 order_id=order_id, is_removed=False)
#             order_products = order_details.values_list('product_id', flat=True)
#             order_colors = order_details.values_list(
#                 'product_color', flat=True)
#             order_sizes = order_details.values_list('product_size', flat=True)
#             order_specs = order_details.values_list(
#                 'specification_id', flat=True)

#             #order_units = order_details.values_list('product_unit',flat = True)
#             order_names = order_details.values_list('product_name', flat=True)
#             order_quantity = order_details.values_list(
#                 'total_quantity', flat=True)
#             for i in range(len(order_products)):
#                 product = ProductSpecification.objects.get(id=order_specs[i])
#                 if product:
#                     product_quantity = product.quantity

#                 else:
#                     product_quantity = 0
#                 # print(product.title)
#                 # print(product.quantity)
#                 product_name = order_names[i]
#                 product_color = order_colors[i]
#                 product_size = order_sizes[i]
#                 #product_unit = order_units[i]
#                 if order_quantity[i] > product_quantity:
#                     current_quantity = product_quantity
#                     current_name = product_name
#                     current_color = product_color
#                     current_size = product_size
#                     #current_unit = product_unit
#                     flag = False
#                     break
#                 else:
#                     flag = True

#             if flag == True:

#                 # change the coupon
#                 # if coupon_code == '':
#                 #     specific_order.coupon_code =
#                 # else:
#                 #     specific_order.coupon = True

#                 # user can checkout
#                 #specific_order.coupon_code = coupon_code
#                 specific_order.checkout_status = True
#                 specific_order.order_status = "Unpaid"
#                 specific_order.delivery_status = "To ship"
#                 specific_order.ordered_date = timezone.now()
#                 specific_order.save()

#                 for i in range(len(order_products)):
#                     product = ProductSpecification.objects.get(
#                         id=order_specs[i])
#                     product_quantity = product.quantity
#                     product.quantity -= order_quantity[i]
#                     product.save()
#                     productserializer = ProductSpecificationSerializer(
#                         product, data=request.data)
#                     print("fuhfuwhuhfuewhewuhew")
#                     if productserializer.is_valid():
#                         print("ffbwybwbfywefbweyfbefb")
#                         productserializer.save()

#                         sales_count = 0
#                         try:
#                             product_impression = ProductImpression.objects.filter(
#                                 product_id=order_products[i])[0:1].get()
#                         except:
#                             product_impression = None

#                         if ProductImpression is None:
#                             pass
#                         else:
#                             product_impression.sales_count += order_quantity[i]
#                             product_impression.save()

#                     else:
#                         print("erroesssss")
#                         return JsonResponse(productserializer.errors)

#                 return JsonResponse({'success': True, 'message': 'The items have been checked out'})

#             else:

#                 message = "You cannot checkout.We only have "+str(current_quantity)+" of item "+str(
#                     current_name)+" of color "+str(current_color)+" of size "+str(current_size)+" in our stock currently."
#                 return JsonResponse({'success': False, 'message': message})

#         else:
#              return JsonResponse({'success': False, 'message': 'This order does not exist'})

        # else:

        #     return JsonResponse({'success': False, 'message': 'This order does not exist'}
# @api_view(["GET", "POST"])
def test_data(data, order_data):
    # if request.method == 'POST':
    store_info = 'My7117@info.inistapay.mymarket'
    api_key = 'inista732962My Market'

    user = paymentInformation(store_info=store_info, api_key=api_key)

    page_url = 'https://mymarket.com.bd'

    user.store_page_url_info(success_page_url=page_url, unsuccess_page_url=page_url,
                             cancel_page_url=page_url, failure_page_url=page_url,
                             special_notification_url=page_url)

    user.customer_information(name=data['name'], email=data['email'], address=data['address'], city=data['city'],
                              post_code=data['post_code'], country=data['country'], phone=data['phone'])

    # test_data = [
    #     {
    #         'product_name': "Noodles 1",
    #         'total_price': '250.00',
    #         'product_color': 'Red',
    #         'product_barcode': 'api_1020_2014',
    #         'product_size': 'None',
    #         'product_unit': 'Kg',
    #         'unit_price': '25',
    #         'total_quantity': '5'
    #     },
    #         {
    #         'product_name': "Noodles 2",
    #         'total_price': '250.00',
    #         'product_color': 'Red',
    #         'product_barcode': 'api_1020_2014',
    #         'product_size': 'None',
    #         'product_unit': 'Kg',
    #         'unit_price': '25',
    #         'total_quantity': '5'
    #     },
    #         {
    #         'product_name': "Noodles 3",
    #         'total_price': '250.00',
    #         'product_color': 'Red',
    #         'product_barcode': 'api_1020_2014',
    #         'product_size': 'None',
    #         'product_unit': 'Kg',
    #         'unit_price': '25',
    #         'total_quantity': '5'
    #     }
    # ]

    user.payment_information(total_amount=data['total_amount'], currency=data['currency'], product_category=data['product_category'],
                             number_of_items=data['number_of_items'], shipping_method=data[
                                 'shipping_method'], invoice_number=data['invoice'],
                                   product_details=order_data)

    val = user.validate_user()
    return val


@api_view(['POST', ])
def checkout(request, order_id):
    payment_method = request.data.get("payment_method")
    data = request.data
    if payment_method == "COD":

        try:
            specific_order = Order.objects.get(id=order_id)
        except:
            specific_order = None

        if specific_order:
            specific_order.checkout_status = True
            specific_order.ordered_date = timezone.now()
            specific_order.payment_method = payment_method
            specific_order.save()
            return JsonResponse({"success": True, "message": "The items have been checked out", "payment_method": payment_method})

        else:
            return JsonResponse({"success": False, "message": "This order does not exist"})

    else:
        try:
            specific_order = Order.objects.get(id=order_id)
        except:
            specific_order = None

        if specific_order:
            order_serializer = OrderSerializer3(specific_order, many=False)
            order_info = order_serializer.data
            order_data = order_info["orders"]

            payment_check = test_data(data, order_data)
            if payment_check['success'] == True:
                specific_order.checkout_status = True
                specific_order.ordered_date = timezone.now()
                specific_order.payment_method = payment_method
                specific_order.transaction_id = payment_check['transaction']
                url = payment_check['url_path']
                return JsonResponse({"success": True, "message": "The items have been checked out ", "url": url, "payment_method": payment_method})
            else:
                return JsonResponse({"success": False, "message": "Payment is not successful"})

        else:
            return JsonResponse({"success": False, "message": "The order does not exist"})


@api_view(['POST', ])
def create_pos_order(request):

    data = { "order" : 	{

                    "invoice_no" : "S/30/11/20/001",
                    "terminal_id" :1,
                    "API_key": "W1Z1X1234Y6372",
                    "pos_user_id": 4,

                    "user" :  {

                                "id" : -1,

                                "username" : "rabby009",

                                "email" : "",

                                "phone_number": "0173dfef13608200578"

                            },

                    "items" : [

                                    {

                                        "specification_id" : 378,

                                        "quantity" : 5

                                    }

                                    ,

                                    {

                                        "specification_id" : 377,

                                        "quantity" : 3

                                    }

                            ]

                            ,

                    "sub_total" : 320.00,

                    "additional_discount" : 10.00,

                    "additional_discount_type" : "amount",

                    "grand_total" : 300.00,

                    "payment" : 500.00,

                    "changes" : 200.00,

                    "due" : 0.00,

                    "vat" : 0.00,

                    "num_items": 2,

                    "users": {}

                }
    }

    data = request.data

    data = data["order"]
    print(data)
    print(data["API_key"])
    # print(data["user"]["id"])

    # Checking if the API key matches
    try:
        terminal = Terminal.objects.get(id=int(data["terminal_id"]))
    except:
        terminal = None

    if terminal:
        print("this terminal exists")
        if data["API_key"] == terminal.API_key:
            print("API key exists")
            # return JsonResponse({"success":True,"message":"kaaj kortese"})
            if data["user"] == {}:
                #guest in user
                user_id = 97
                role = "PoS Customer"
                print("guestuser")
                phone_number = ""
                username = ""
                try:
                    user_info = User.objects.get(id=user_id)
                except:
                    user_info = None 
                if user_info:
                    email = user_info.email
                else:
                    email = ""
            elif data["user"]["id"] == -1:
                # the user is not registered and has to be registered
                # Regsiter the user
                #Check if the phone number already exists

                phone_number = data["user"]["phone_number"]

                if data["user"]["email"] == "":
                    email = phone_number + "@gmail.com"
                else:
                    email = data["user"]["email"]
                username = data["user"]["username"]


                try:
                    userzzz = User.objects.filter(phone_number=phone_number,role="PoS Customer")
                except:
                    userzzz = None 

                if userzzz:
                    userzz_phones = list(userzzz.values_list('phone_number', flat=True))
                else:
                    userzz_phones = []

                try:
                    userzz = User.objects.all()
                except:
                    userzz = None

                if userzz:
                    users_email = list(userzz.values_list('email', flat=True))
                else:
                    users_email = []




                if phone_number in userzz_phones:
                    if email in users_email:
                        return JsonResponse({"success":False,"message":"Both the phone number and the email already exists.Please provide alternative phone numbers and email addresses."})

                    else:
                        return JsonResponse({"success":False,"message":"The phone number already exists.Please provide another phone number."})

                    
                else:
                    if email in users_email:
                        return JsonResponse({"success":False,"message":"The email already exists.Please provide another email address."})
                    else:
                        customer = User.objects.create(
                            email=email, phone_number=phone_number, username=username, password="12345678", role="PoS Customer")
                        customer.save()
                        user_id = customer.id
                        print("user create hochche")

            else:
                print("userase")
                user_id = data["user"]["id"]
                email = data["user"]["email"]
                phone_number = data["user"]["phone_number"]
                username = data["user"]["username"]
                
                try:
                    userzzz = User.objects.filter(phone_number=phone_number,role="PoS Customer")
                except:
                    userzzz = None 

                if userzzz:
                    userzz_phones = list(userzzz.values_list('phone_number', flat=True))
                else:
                    userzz_phones = []

                try:
                    userzz = User.objects.all()
                except:
                    userzz = None

                if userzz:
                    users_email = list(userzz.values_list('email', flat=True))
                else:
                    users_email = []
                print(users_email)
                try:
                    userz = User.objects.get(id=user_id)
                except:
                    userz = None
                print(userz)
                if userz:
                    if userz.email == email:
                        pass
                    else:
                        #check if the email already exists
                        if email in users_email:
                            if userz.phone_number == phone_number:                            
                                return JsonResponse({"success":False,"message":"The email provided already exists. Please provide another email."})
                            else:
                                if phone_number in userzz_phones:
                                    return JsonResponse({"success":False,"message":"Both the phone number provided and the email address already exists. Please provide alternatives."})

                                else:
                                    return JsonResponse({"success":False,"message":"The email provided already exists. Please provide another email."})

                        else:
                            if userz.phone_number == phone_number:
                                userz.email = email
                            else:
                                if phone_number in userzz_phones:
                                    return JsonResponse({"success":False,"message":"The phone number already exists.Please provide another phone number"})
                                else:
                                    userz.email = email
                                    userz.phone_number = phone_number

                    userz.username = username
                    # userz.phone_number = phone_number
                    userz.save()

                else:
                    return JsonResponse({"success":False,"message":"The user id provided does not exist"})




            user_object = {"id": user_id, "email": email, "phone_number": phone_number,
                           "username": username, "role": "PoS Customer"}
            # return JsonResponse({"success":True,"message":"kaaj kortese","data":user_object})

            # Create an order for the user

            pos_additional_discount = data["additional_discount"]
            # print(pos_additional_discount)
            # print(type(pos_additional_discount))
            pos_additional_discount_type = data["additional_discount_type"]
            # print(type(pos_additional_discount_type))
            sub_total = data["sub_total"]
            # print(type(sub_total))
            grand_total = data["grand_total"]
            # print(type(grand_total))
            payment = data["payment"]
            # print(type(payment))
            changes = data["changes"]
            # print(type(changes))
            due = data["due"]
            # print(type(due))
            vat = data["vat"]
            # print(type(vat))
            num_items = data["num_items"]
            # print(type(num_items))
            # print(type(data["pos_user_id"]))
            # print(type(user_id))

            order = Order.objects.create(user_id=user_id, checkout_status=True, order_status="Paid", delivery_status="Delivered", admin_status="Confirmed",
                                         admin_id=data["pos_user_id"],terminal_id = data["terminal_id"], is_pos=True, pos_additional_discount_type=pos_additional_discount_type, pos_additional_discount=pos_additional_discount, sub_total=sub_total, grand_total=grand_total, payment=payment, changes=changes, due=due, vat=vat, num_items=num_items)
            order.save()
            order_id = order.id

            # Create the order details objects
            count = len(data["items"])
            items = data["items"]
            stock_info = []
            for i in range(count):
                specification_id = items[i]["specification_id"]
                quantity = items[i]["quantity"]
                try:
                    product = ProductSpecification.objects.get(
                        id=specification_id)
                except:
                    product = None
                if product:
                    product_id = product.product_id
                    product_color = product.color
                    product_size = product.size
                    product_weight = product.weight
                    product_unit = product.unit
                else:
                    product_id = -1
                    product_color = ""
                    product_size = ""
                    product_weight = 0.0
                    product_unit = ""
                # Fetch the product name
                try:
                    products = Product.objects.get(id=product_id)
                except:
                    products = None
                if products:
                    product_name = products.title
                else:
                    product_name = ""

                # Fetch the price

                try:
                    p_price = ProductPrice.objects.filter(
                        specification_id=specification_id).last()
                except:
                    p_price = None
                if p_price:
                    price = p_price.price
                else:
                    price = 0.0

                unit_price = price
                total_price = price * quantity

                # Fetching the product points
                try:
                    product_point = ProductPoint.objects.filter(
                        specification_id=specification_id).last()
                except:
                    product_point = None

                if product_point is not None:

                    if product_point.point:
                        p_point = product_point.point

                    else:
                        p_point = 0
                    current_date = timezone.now().date()
                    start_date = current_date
                    end_date = current_date

                    if product_point.start_date:
                        start_date = product_point.start_date
                    else:
                        start_date = current_date

                    if product_point.end_date:
                        end_date = product_point.end_date

                    else:
                        end_date = current_date

                    if (current_date >= start_date) and (current_date <= end_date):
                        total_point = p_point * quantity
                        unit_point = p_point

                    else:
                        total_point = 0
                        unit_point = 0

                else:

                    total_point = 0
                    unit_point = 0
                
                # print(type(quantity))
                # print(type(unit_price))
                # print(type(unit_point))
                # print(type(total_price))
                # print(type(total_point))
                unit_point = float(unit_point)
                total_point = float(total_point)
                # print(type(product_weight))

                order_details = OrderDetails.objects.create(order_id=order_id, specification_id=specification_id, product_id=product_id, total_quantity=quantity, quantity=quantity, unit_price=unit_price, total_price=total_price, unit_point=unit_point,
                                                            total_point=total_point, product_name=product_name, product_color=product_color, product_size=product_size, product_weight=product_weight, product_unit=product_unit, admin_status="Approved", product_status="None")
                order_details.save()
                # Adjusting the quantity
                terminal_id = data["terminal_id"]
                try:
                    terminal = Terminal.objects.get(id=terminal_id)
                except:
                    terminal = None
                if terminal:

                    warehouse_id = terminal.warehouse_id
                    shop_id = terminal.shop_id

                    if warehouse_id == -1:
                        print("shop is there")
                        inventory_id = shop_id
                        print(shop_id)
                        print(specification_id)
                        try:
                            shop_info = ShopInfo.objects.get(
                                shop_id=shop_id, specification_id=specification_id)
                        except:
                            shop_info = None

                        print(shop_info)

                        if shop_info:
                            shop_info.quantity -= quantity
                            shop_info.save()
                            stock_data = {"id": shop_info.id, "shop_id": shop_info.shop_id,
                                          "specification_id": shop_info.specification_id, "quantity": shop_info.quantity, "place": "shop"}
                            stock_info.append(stock_data)

                            # making entries in the inventory_report table
                            inventory = inventory_report.objects.create(
                                product_id=product_id, specification_id=specification_id, shop_id=shop_id, requested=quantity, admin_id=data["pos_user_id"])
                            inventory.save()

                            # making entries in the subtraction log table
                            sub_track = subtraction_track.objects.create(
                                order_id=order_id, specification_id=specification_id, shop_id=shop_id, debit_quantity=quantity, admin_id=data["pos_user_id"])
                            sub_track.save()

                        else:
                            pass

                    elif shop_id == -1:
                        print("warehouse is there")
                        inventory_id = warehouse_id
                        try:
                            shop_info = WarehouseInfo.objects.get(
                                warehouse_id=warehouse_id, specification_id=specification_id)
                        except:
                            shop_info = None

                        print(shop_info)

                        if shop_info:
                            shop_info.quantity -= quantity
                            shop_info.save()
                            print("warehouse theke minus hoise")
                            stock_data = {"id": shop_info.id, "warehouse_id": shop_info.warehouse_id,
                                          "specification_id": shop_info.specification_id, "quantity": shop_info.quantity, "place": "warehouse"}
                            stock_info.append(stock_data)

                            # making entries in the inventory_report table
                            inventory = inventory_report.objects.create(
                                product_id=product_id, specification_id=specification_id, warehouse_id=warehouse_id, requested=quantity, admin_id=data["pos_user_id"])
                            inventory.save()

                            # making entries in the subtraction log table
                            sub_track = subtraction_track.objects.create(
                                order_id=order_id, specification_id=specification_id, warehouse_id=warehouse_id, debit_quantity=quantity, admin_id=data["pos_user_id"])
                            sub_track.save()

                        else:
                            pass
                    else:
                        print("elseeeee")
                        inventory_id = -1

            order_serializer = PoSOrderSerializer(order, many=False)
            order_data = order_serializer.data

            # Create an invoice for the order
            invoice = Invoice.objects.create(
                order_id=order_id, admin_id=data["pos_user_id"], invoice_no=data["invoice_no"])
            invoice.save()

            invoice_serializer = PoSInvoiceSerializer(invoice, many=False)
            invoice_data = invoice_serializer.data

            # Decrease the quantity from warehouse or shop
            main_data = {"user": user_object, "order_data": order_data,
                         "invoice": invoice_data, "stock": stock_info}

            return JsonResponse({"success": True, "message": "Data is shown", "order": main_data})

        else:
            return JsonResponse({"success": True, "message": "The API key does not match"})

    else:
        return JsonResponse({"success": True, "message": "The terminal does not exist"})


@api_view(['POST', ])
def check_user(request):

    data = {


        "user":  {

            "username": "sammm",

            "email": "flyzoneaman@gmail.com",

            "phone_number": "01731360828"

        }


    }
    data = request.data

    data = data["user"]
    try:
        userz = User.objects.all()
    except:
        userz = None

    if userz:
        users_email = list(userz.values_list('email', flat=True))
    else:
        users_email = []

    phone_number = data["phone_number"]
    print(phone_number)
    role = "PoS Customer"
    email = data["email"]
    email_flag = 0
    if email == "-":
        email_flag = 0
        
    else:
        email_flag = 1

    username = data["username"]
    username_flag = 0
    if username == "-":
        username_flag = 0
    else:
        username_flag = 1



    try:


        users = User.objects.filter(phone_number=phone_number, role=role).last()

    except:
        users = None

    print("users")
    print(users)

    if users:
        if email_flag == 1:
            #checking if the email exists in the database
            if email in users_email:
                return JsonResponse({"success":False,"message":"The user exists but the email address address provided cannot be used. Please enter another email address."})
            else:
                users.email = email

        if username_flag == 1:
            users.username = username

        users.save()
        user_id = users.id
        user_email = users.email
        user_username = users.username
        user_phone_number = users.phone_number

        data_user = {"user_id": user_id, "email": user_email,
                     "username": user_username, "phone_number": user_phone_number, "role": role}
        return JsonResponse({"success": True, "message": "The user exists", "data": data_user})

    else:
        return JsonResponse({"success": False, "message": "The user does not exist"})


def check_test(data):

    pay = paymentInformation(
        'My7117@info.inistapay.mymarket', 'inista732962My Market')
    pay.store_page_url_info(success_page_url='https://mymarket.com.bd', unsuccess_page_url='https://mymarket.com.bd',
                            cancel_page_url='https://mymarket.com.bd', failure_page_url='https://mymarket.com.bd',
                            special_notification_url='https://mymarket.com.bd')
    pay.customer_information(name=data['name'], email=data['email'], address=data['address'], city=data['city'],
                             post_code=data['post_code'], country=data['country'], phone=data['phone'])
    pay.payment_information(total_amount=data['total_amount'], currency=data['currency'], product_category=data['product_category'],
                            number_of_items=data['number_of_items'], shipping_method=data['shipping_method'], invoice_number=data['invoice'], payment_medium=data['pay_medium'])
    val = pay.validate_user()
    return val



# @api_view(['POST', ])
# def verify_payment(request):

#     medium = request.data.get("medium")

#     if medium:
#         payment_reference_id = request.data.get("payment_reference_id")
#         print(payment_reference_id)
#         url_info = "http://instapay.com.bd/check_pay/"

#         post_data = {"pay_id":payment_reference_id}
#         print(post_data)
#         headers = {'Content-Type': 'application/json',}
#         payment_results = requests.post(url = url_info, data = post_data) 
#         #print(payment_result.json())
#         print(payment_results)
#         print(type(payment_results))
#         p_result = str(payment_results)
#         print(p_result)
#         print(type(p_result))
#         payment_result = payment_results.json()
#         print(payment_result)
#         # payment_result = {
#         #                     "success": True,
#         #                     "data": {
#         #                         "paymentID": "UQ87UZA1609153599863",
#         #                         "createTime": "2020-12-28T05:36:34:221 GMT+0000",
#         #                         "updateTime": "2020-12-28T05:37:02:433 GMT+0000",
#         #                         "trxID": "7LS004GNPW",
#         #                         "transactionStatus": "Completed",
#         #                         "amount": "2.00",
#         #                         "currency": "BDT",
#         #                         "intent": "sale",
#         #                         "merchantInvoiceNumber": "00000168",
#         #                         "refundAmount": "0"
#         #                     }
#         #                 }



#         if payment_result["success"] == True:
#             payment_result = payment_result["data"]

#             merchant_invoice_number = payment_result["merchantInvoiceNumber"]
#             order_id = int(merchant_invoice_number[5:])
            

#             # Store the payment info
#             # Fetch the transaction id
#             try:
#                 specific_order = Order.objects.get(id=order_id)
#             except:
#                 specific_order = None
#             if specific_order:
                
#                 payment_method = specific_order.payment_method
#                 specific_order.order_status = "Paid"
#                 specific_order.save()
#             else:
#                 return JsonResponse({"success": False, "message": "This order does not exist"})

#             info = BkashPaymentInfo.objects.create(order_id=order_id, payment_method=payment_method, payment_id = payment_result["paymentID"], create_time = payment_result["createTime"], update_time = payment_result["updateTime"], transaction_id = payment_result["trxID"], transaction_status = payment_result["transactionStatus"], amount = payment_result["amount"], intent = payment_result["intent"],currency = payment_result["currency"], refund_amount = payment_result["refundAmount"],merchant_invoice_number = merchant_invoice_number,payment_reference_id=payment_reference_id)
#             info.save()
#             return JsonResponse({"success":True,"message":"Payment is successful"}) 

#         else:
#             merchant_invoice_number = payment_result["merchantInvoiceNumber"]
#             order_id = int(merchant_invoice_number[5:])
#             try:
#                 specific_order = Order.objects.get(id=order_id)
#             except:
#                 specific_order = None
#             if specific_order:
                
#                 payment_method = specific_order.payment_method
#                 specific_order.order_status = "Unpaid"
#                 specific_order.save()
#             else:
#                 return JsonResponse({"success": False, "message": "This order does not exist"})

#             info = BkashPaymentInfo.objects.create(order_id=order_id, payment_method=payment_method, payment_id = payment_result["paymentID"], create_time = payment_result["createTime"], update_time = payment_result["updateTime"], transaction_id = payment_result["trxID"], transaction_status = payment_result["transactionStatus"], amount = payment_result["amount"], intent = payment_result["intent"],currency = payment_result["currency"], refund_amount = payment_result["refundAmount"],merchant_invoice_number = merchant_invoice_number,payment_reference_id=payment_reference_id)
#             info.save()
#             return JsonResponse({"success":False,"message":"Payment is not successful"}) 

    
        

#     else:

#         order_id = request.data.get("order_id")
#         order_id = int(order_id)
#         payment_reference_id = request.data.get("payment_reference_id")

#         # payment_result = {
#         #     "success": True,
#         #     "data": [
#         #         True,
#         #         {
#         #             "merchantId": "683002007104225",
#         #             "orderId": "k00459145",
#         #             "paymentRefId": "MTIwODExMjQ0Nzc2NS42ODMwMDIwMDcxMDQyMjUuazAwNDU5MTQ1LmFkOWE5MGY4NjhlMGJlMTcyMmJl",
#         #             "amount": "1",
#         #             "clientMobileNo": "015****0171",
#         #             "merchantMobileNo": "01300200710",
#         #             "orderDateTime": "2020-12-08 11:24:47.0",
#         #             "issuerPaymentDateTime": "2020-12-08 11:26:00.0",
#         #             "issuerPaymentRefNo": "00004EBQ",
#         #             "additionalMerchantInfo": "{\"ProductName\":\"Mixed\"}",
#         #             "status": "Success",
#         #             "statusCode": "000",
#         #             "cancelIssuerDateTime": "sfdsfdsfdsf",
#         #             "cancelIssuerRefNo": "dsfdsfdsfdsf"
#         #         }
#         #     ]

#         # }

#         url_info = "http://instapay.com.bd/pay_verification/"
#         url = url_info + payment_reference_id

#         payment_results = requests.get(url = url) 
#         #print(payment_result.json())
#         payment_result = payment_results.json()

#         # Check if the payment reference id matches
#         print(payment_reference_id)
#         print(payment_result["data"][1]["paymentRefId"])
#         if payment_reference_id == payment_result["data"][1]["paymentRefId"]:
#             print("successful")

#             if payment_result["data"][0] == True:
#                 # Store the payment info
#                 # Fetch the transaction id
#                 try:
#                     specific_order = Order.objects.get(id=order_id)
#                 except:
#                     specific_order = None
#                 if specific_order:
#                     transaction_id = specific_order.transaction_id
#                     payment_method = specific_order.payment_method
#                     specific_order.order_status = "Paid"
#                     specific_order.save()
#                 else:
#                     return JsonResponse({"success": False, "message": "This order does not exist"})

#                 info = BkashPaymentInfo.objects.create(order_id=order_id, transaction_id=transaction_id, payment_method=payment_method, merchant_id=payment_result["data"][1]["merchantId"],payment_reference_id=payment_result["data"][1]["paymentRefId"], amount=payment_result["data"][1]["amount"], 
#                                                 client_mobile_number=payment_result["data"][1]["clientMobileNo"], order_datetime=payment_result["data"][1]["orderDateTime"], issuer_payment_datetime=payment_result["data"][1]["issuerPaymentDateTime"], 
#                                                 issuer_payment_ref_no=payment_result["data"][1]["issuerPaymentRefNo"], additional_merchant_info=payment_result["data"][1]["additionalMerchantInfo"], 
#                                                 status=payment_result["data"][1]["status"], status_code=payment_result["data"][1]["statusCode"], cancelissuer_datetime=payment_result["data"][1]["cancelIssuerDateTime"], cancelissuer_ref_no=payment_result["data"][1]["cancelIssuerRefNo"])

#                 info.save()
#                 return JsonResponse({"success":True,"message":"Payment is successful"})

#             else:
#                 # Store the payment info
#                 # Fetch the transaction id
#                 try:
#                     specific_order = Order.objects.get(id=order_id)
#                 except:
#                     specific_order = None
#                 if specific_order:
#                     transaction_id = specific_order.transaction_id
#                     payment_method = specific_order.payment_method
#                     specific_order.order_status = "Unpaid"
#                     specific_order.save()
#                 else:
#                     return JsonResponse({"success": False, "message": "This order does not exist"})

#                 info = PaymentInfo.objects.create(order_id=order_id, transaction_id=transaction_id, payment_method=payment_method, merchant_id=payment_result["data"][1]["merchantId"], payment_reference_id=payment_result["data"][1]["paymentRefId"], amount=payment_result["data"][1]["amount"], 
#                                                 client_mobile_number=payment_result["data"][1]["clientMobileNo"], order_datetime=payment_result["data"][1]["orderDateTime"], issuer_payment_datetime=payment_result["data"][1]["issuerPaymentDateTime"], 
#                                                 issuer_payment_ref_no=payment_result["data"][1]["issuerPaymentRefNo"], additional_merchant_info=payment_result["data"][1]["additionalMerchantInfo"], 
#                                                 status=payment_result["data"][1]["status"], status_code=payment_result["data"][1]["statusCode"], cancelissuer_datetime=payment_result["data"][1]["cancelIssuerDateTime"], cancelissuer_ref_no=payment_result["data"][1]["cancelIssuerRefNo"])

#                 info.save()
#                 return JsonResponse({"success":False,"message":"Payment is not successful"})


                


#         else:

#             return JsonResponse({"success": False, "message": "The reference ids dont match"})



@api_view(['POST', ])
def verify_payment(request):

    medium = request.data.get("medium")

    if medium:
        payment_reference_id = request.data.get("payment_reference_id")
        print(payment_reference_id)
        url_info = "http://instapay.com.bd/check_pay/"

        post_data = {"pay_id":payment_reference_id}
        print(post_data)
        headers = {'Content-Type': 'application/json',}
        payment_results = requests.post(url = url_info, data = post_data) 
        #print(payment_result.json())
        print(payment_results)
        print(type(payment_results))
        p_result = str(payment_results)
        print(p_result)
        print(type(p_result))
        payment_result = payment_results.json()
        print(payment_result)
        # payment_result = {
        #                     "success": True,
        #                     "data": {
        #                         "paymentID": "UQ87UZA1609153599863",
        #                         "createTime": "2020-12-28T05:36:34:221 GMT+0000",
        #                         "updateTime": "2020-12-28T05:37:02:433 GMT+0000",
        #                         "trxID": "7LS004GNPW",
        #                         "transactionStatus": "Completed",
        #                         "amount": "2.00",
        #                         "currency": "BDT",
        #                         "intent": "sale",
        #                         "merchantInvoiceNumber": "00000168",
        #                         "refundAmount": "0"
        #                     }
        #                 }



        if payment_result["success"] == True:
            payment_result = payment_result["data"]

            merchant_invoice_number = payment_result["merchantInvoiceNumber"]
            order_id = int(merchant_invoice_number[5:])
            

            # Store the payment info
            # Fetch the transaction id
            try:
                specific_order = Order.objects.get(id=order_id)
            except:
                specific_order = None
            if specific_order:
                
                payment_method = specific_order.payment_method
                specific_order.order_status = "Paid"
                specific_order.save()
                try:
                    order_details = OrderDetails.objects.filter(order_id=order_id)
                except:
                    order_details = None 
                if order_details:
                    #find all the item ids

                    order_details_ids = list(order_details.values_list('id', flat=True))

                    for k in range(len(order_details_ids)):
                        try:
                            specific_item = OrderDetails.objects.get(order_details_ids[k])
                        except:
                            specific_item = None 

                        if specific_item:
                            specific_item.order_status = "Paid"

                            specific_item.save()
            else:
                return JsonResponse({"success": False, "message": "This order does not exist"})

            info = BkashPaymentInfo.objects.create(order_id=order_id, payment_method=payment_method, payment_id = payment_result["paymentID"], create_time = payment_result["createTime"], update_time = payment_result["updateTime"], transaction_id = payment_result["trxID"], transaction_status = payment_result["transactionStatus"], amount = payment_result["amount"], intent = payment_result["intent"],currency = payment_result["currency"], refund_amount = payment_result["refundAmount"],merchant_invoice_number = merchant_invoice_number,payment_reference_id=payment_reference_id)
            info.save()
            return JsonResponse({"success":True,"message":"Payment is successful"}) 

        else:
            merchant_invoice_number = payment_result["merchantInvoiceNumber"]
            order_id = int(merchant_invoice_number[5:])
            try:
                specific_order = Order.objects.get(id=order_id)
            except:
                specific_order = None
            if specific_order:
                
                payment_method = specific_order.payment_method
                specific_order.order_status = "Unpaid"
                specific_order.save()
                try:
                    order_details = OrderDetails.objects.filter(order_id=order_id)
                except:
                    order_details = None 
                if order_details:
                    #find all the item ids

                    order_details_ids = list(order_details.values_list('id', flat=True))

                    for k in range(len(order_details_ids)):
                        try:
                            specific_item = OrderDetails.objects.get(order_details_ids[k])
                        except:
                            specific_item = None 

                        if specific_item:
                            specific_item.order_status = "Unpaid"

                            specific_item.save()
            else:
                return JsonResponse({"success": False, "message": "This order does not exist"})

            info = BkashPaymentInfo.objects.create(order_id=order_id, payment_method=payment_method, payment_id = payment_result["paymentID"], create_time = payment_result["createTime"], update_time = payment_result["updateTime"], transaction_id = payment_result["trxID"], transaction_status = payment_result["transactionStatus"], amount = payment_result["amount"], intent = payment_result["intent"],currency = payment_result["currency"], refund_amount = payment_result["refundAmount"],merchant_invoice_number = merchant_invoice_number,payment_reference_id=payment_reference_id)
            info.save()
            return JsonResponse({"success":False,"message":"Payment is not successful"}) 

    
        

    else:

        order_id = request.data.get("order_id")
        order_id = int(order_id)
        payment_reference_id = request.data.get("payment_reference_id")

        # payment_result = {
        #     "success": True,
        #     "data": [
        #         True,
        #         {
        #             "merchantId": "683002007104225",
        #             "orderId": "k00459145",
        #             "paymentRefId": "MTIwODExMjQ0Nzc2NS42ODMwMDIwMDcxMDQyMjUuazAwNDU5MTQ1LmFkOWE5MGY4NjhlMGJlMTcyMmJl",
        #             "amount": "1",
        #             "clientMobileNo": "015****0171",
        #             "merchantMobileNo": "01300200710",
        #             "orderDateTime": "2020-12-08 11:24:47.0",
        #             "issuerPaymentDateTime": "2020-12-08 11:26:00.0",
        #             "issuerPaymentRefNo": "00004EBQ",
        #             "additionalMerchantInfo": "{\"ProductName\":\"Mixed\"}",
        #             "status": "Success",
        #             "statusCode": "000",
        #             "cancelIssuerDateTime": "sfdsfdsfdsf",
        #             "cancelIssuerRefNo": "dsfdsfdsfdsf"
        #         }
        #     ]

        # }

        url_info = "http://instapay.com.bd/pay_verification/"
        url = url_info + payment_reference_id

        payment_results = requests.get(url = url) 
        #print(payment_result.json())
        payment_result = payment_results.json()

        # Check if the payment reference id matches
        print(payment_reference_id)
        print(payment_result["data"][1]["paymentRefId"])
        if payment_reference_id == payment_result["data"][1]["paymentRefId"]:
            print("successful")

            if payment_result["data"][0] == True:
                # Store the payment info
                # Fetch the transaction id
                try:
                    specific_order = Order.objects.get(id=order_id)
                except:
                    specific_order = None
                if specific_order:
                    transaction_id = specific_order.transaction_id
                    payment_method = specific_order.payment_method
                    specific_order.order_status = "Paid"
                    specific_order.save()
                    try:
                        order_details = OrderDetails.objects.filter(order_id=order_id)
                    except:
                        order_details = None 
                    if order_details:
                        #find all the item ids

                        order_details_ids = list(order_details.values_list('id', flat=True))

                        for k in range(len(order_details_ids)):
                            try:
                                specific_item = OrderDetails.objects.get(order_details_ids[k])
                            except:
                                specific_item = None 

                            if specific_item:
                                specific_item.order_status = "Paid"

                                specific_item.save()
                else:
                    return JsonResponse({"success": False, "message": "This order does not exist"})

                info = BkashPaymentInfo.objects.create(order_id=order_id, transaction_id=transaction_id, payment_method=payment_method, merchant_id=payment_result["data"][1]["merchantId"],payment_reference_id=payment_result["data"][1]["paymentRefId"], amount=payment_result["data"][1]["amount"], 
                                                client_mobile_number=payment_result["data"][1]["clientMobileNo"], order_datetime=payment_result["data"][1]["orderDateTime"], issuer_payment_datetime=payment_result["data"][1]["issuerPaymentDateTime"], 
                                                issuer_payment_ref_no=payment_result["data"][1]["issuerPaymentRefNo"], additional_merchant_info=payment_result["data"][1]["additionalMerchantInfo"], 
                                                status=payment_result["data"][1]["status"], status_code=payment_result["data"][1]["statusCode"], cancelissuer_datetime=payment_result["data"][1]["cancelIssuerDateTime"], cancelissuer_ref_no=payment_result["data"][1]["cancelIssuerRefNo"])

                info.save()
                return JsonResponse({"success":True,"message":"Payment is successful"})

            else:
                # Store the payment info
                # Fetch the transaction id
                try:
                    specific_order = Order.objects.get(id=order_id)
                except:
                    specific_order = None
                if specific_order:
                    transaction_id = specific_order.transaction_id
                    payment_method = specific_order.payment_method
                    specific_order.order_status = "Unpaid"
                    specific_order.save()
                    try:
                        order_details = OrderDetails.objects.filter(order_id=order_id)
                    except:
                        order_details = None 
                    if order_details:
                        #find all the item ids

                        order_details_ids = list(order_details.values_list('id', flat=True))

                        for k in range(len(order_details_ids)):
                            try:
                                specific_item = OrderDetails.objects.get(order_details_ids[k])
                            except:
                                specific_item = None 

                            if specific_item:
                                specific_item.order_status = "Unpaid"

                                specific_item.save()
                else:
                    return JsonResponse({"success": False, "message": "This order does not exist"})

                info = PaymentInfo.objects.create(order_id=order_id, transaction_id=transaction_id, payment_method=payment_method, merchant_id=payment_result["data"][1]["merchantId"], payment_reference_id=payment_result["data"][1]["paymentRefId"], amount=payment_result["data"][1]["amount"], 
                                                client_mobile_number=payment_result["data"][1]["clientMobileNo"], order_datetime=payment_result["data"][1]["orderDateTime"], issuer_payment_datetime=payment_result["data"][1]["issuerPaymentDateTime"], 
                                                issuer_payment_ref_no=payment_result["data"][1]["issuerPaymentRefNo"], additional_merchant_info=payment_result["data"][1]["additionalMerchantInfo"], 
                                                status=payment_result["data"][1]["status"], status_code=payment_result["data"][1]["statusCode"], cancelissuer_datetime=payment_result["data"][1]["cancelIssuerDateTime"], cancelissuer_ref_no=payment_result["data"][1]["cancelIssuerRefNo"])

                info.save()
                return JsonResponse({"success":False,"message":"Payment is not successful"})


                


        else:

            return JsonResponse({"success": False, "message": "The reference ids dont match"})

# @api_view(['POST', ])
# def get_last_order_address(request):

#     user_id = request.data.get('user_id')
#     non_verified_user_id = request.data.get('non_verified_user_id')
#     if user_id is not None:
#         user_id = int(user_id)
#         non_verified_user_id = 0

#     else:
#         non_verified_user_id = int(non_verified_user_id)
#         user_id = 0

#     if non_verified_user_id == 0:

#         try:
#             specific_order = Order.objects.filter(
#                 user_id=user_id, checkout_status=True).order_by('-ordered_date')
#         except:
#             specific_order = None

#         if specific_order:

#             orderserializer = OrderSerializer(specific_order, many=True)
#             #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)
#             order_data = orderserializer.data
#             order_data = json.loads(json.dumps(order_data, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
#             order_id = order_data[0]["id"]
#             try:
#                 order_info = OrderInfo.objects.filter(order_id=order_id).last()

#             except:
#                 order_info = None 

#             if order_info:
#                 billing_address_id = order_info.billing_address_id

#             else:
#                 billing_address_id = 0

#             try:
#                 billing_address = BillingAddress.objects.get(id=billing_address_id)
#             except:
#                 billing_address = None 

#             if billing_address:
#                 billing_address_serializer = BillingAddressSerializer(billing_address,many=False)
#                 return JsonResponse({"scuccess":True,"message":"The billing address is shown","billing_data":billing_address_serializer.data,"order_data":orderserializer.data})

#             else:
#                 return JsonResponse({"scuccess":False,"message":"There is no address to show","order_data":orderserializer.data})


#             #orders = [orderserializer.data , orderdetailserializer.data]
#             #return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

#         else:
#             return JsonResponse({'success': False, 'message': 'You have no orders'})

#     else:

#         try:
#             specific_order = Order.objects.filter(
#                 non_verified_user_id = non_verified_user_id, checkout_status=True).order_by('-ordered_date')
#         except:
#             specific_order = None

#         if specific_order:

#             orderserializer = OrderSerializer(specific_order, many=True)
#             #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)
#             order_data = orderserializer.data

#             order_data = json.loads(json.dumps(order_data, sort_keys=True, indent=1, cls=DjangoJSONEncoder))

#             print(order_data)



           
        
#             order_id = int(order_data[0]["id"])
#             try:
#                 order_info = OrderInfo.objects.filter(order_id=order_id).last()

#             except:
#                 order_info = None 

#             if order_info:
#                 billing_address_id = order_info.billing_address_id

#             else:
#                 billing_address_id = 0

#             try:
#                 billing_address = BillingAddress.objects.get(id=billing_address_id)
#             except:
#                 billing_address = None 

#             if billing_address:
#                 billing_address_serializer = BillingAddressSerializer(billing_address,many=False)
#                 return JsonResponse({"scuccess":True,"message":"The billing address is shown","billing_data":billing_address_serializer.data,"order_data":orderserializer.data})

#             else:
#                 return JsonResponse({"scuccess":False,"message":"There is no address to show","order_data":orderserializer.data})


#             #orders = [orderserializer.data , orderdetailserializer.data]
#             #return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

#         else:
#             return JsonResponse({'success': False, 'message': 'You have no orders'})



@api_view(['POST', ])
def get_last_order_address(request):


    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id = 0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:

        try:
            specific = Order.objects.filter(
                user_id=user_id, checkout_status=True).order_by('-ordered_date').count()

        except:
            specific = None 

        print("specific")
        print(specific)

        if specific > 1:
            order_count = True

        else:
            order_count = False

        

        try:
            specific_order = Order.objects.filter(
                user_id=user_id, checkout_status=True).last()
        except:
            specific_order = None

        if specific_order:

            order_id = specific_order.id

            # order_ids = list(specific_order.values_list('id',flat=True))

            # order_count = len(order_ids)

            # if order_count > 1:

            #     order_flag = True

            # else:
            #     order_flag = False

            # print(order_count)

            # print(order_flag)


            orderserializer = OrderSerializer(specific_order, many=False)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)
            order_data = orderserializer.data
            # print(order_data)
            # order_data = json.loads(json.dumps(order_data, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
            # order_id = order_data[0]["id"]
            try:
                order_info = OrderInfo.objects.filter(order_id=order_id).last()

            except:
                order_info = None 

            if order_info:
                billing_address_id = order_info.billing_address_id

            else:
                billing_address_id = 0

            try:
                billing_address = BillingAddress.objects.get(id=billing_address_id)
            except:
                billing_address = None 

            if billing_address:
                billing_address_serializer = BillingAddressSerializer(billing_address,many=False)
                return JsonResponse({"success":True,"message":"The billing address is shown","billing_data":billing_address_serializer.data,"order_data":orderserializer.data,"order_count":order_count})

            else:
                return JsonResponse({"success":False,"message":"There is no address to show","order_data":orderserializer.data})


            #orders = [orderserializer.data , orderdetailserializer.data]
            #return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})

    else:

        try:
            specific = Order.objects.filter(
                non_verified_user_id= non_verified_user_id, checkout_status=True).order_by('-ordered_date').count()

        except:
            specific = None 

        print("specific")
        print(specific)

        if specific > 1:
            order_count = True

        else:
            order_count = False

        

        try:
            specific_order = Order.objects.filter(
                non_verified_user_id= non_verified_user_id, checkout_status=True).last()
        except:
            specific_order = None

        if specific_order:

            order_id = specific_order.id

            # order_ids = list(specific_order.values_list('id',flat=True))

            # order_count = len(order_ids)

            # if order_count > 1:

            #     order_flag = True

            # else:
            #     order_flag = False

            # print(order_count)

            # print(order_flag)


            orderserializer = OrderSerializer(specific_order, many=False)
            #orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)
            order_data = orderserializer.data
            # print(order_data)
            # order_data = json.loads(json.dumps(order_data, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
            # order_id = order_data[0]["id"]
            try:
                order_info = OrderInfo.objects.filter(order_id=order_id).last()

            except:
                order_info = None 

            if order_info:
                billing_address_id = order_info.billing_address_id

            else:
                billing_address_id = 0

            try:
                billing_address = BillingAddress.objects.get(id=billing_address_id)
            except:
                billing_address = None 

            if billing_address:
                billing_address_serializer = BillingAddressSerializer(billing_address,many=False)
                return JsonResponse({"success":True,"message":"The billing address is shown","billing_data":billing_address_serializer.data,"order_data":orderserializer.data,"order_count":order_count})

            else:
                return JsonResponse({"success":False,"message":"There is no address to show","order_data":orderserializer.data})


            #orders = [orderserializer.data , orderdetailserializer.data]
            #return JsonResponse({'success': True, 'message': 'The products in your order are shown', 'data': orderserializer.data}, safe=False)

        else:
            return JsonResponse({'success': False, 'message': 'You have no orders'})








@api_view(['GET', ])
def change_order_date(request,order_id):

    try:
        specific_order  = Order.objects.get(id=order_id)
    except:
        specific_order = None 

    if specific_order:
        specific_order.ordered_date = "2020-12-22"
        specific_order.save()
        return JsonResponse({"success":True})

    else:
        return JsonResponse({"success":False})



@api_view(['GET', ])
def get_terminal_users(request,terminal_id):

    users = []
    all_users = {
                    "id": 0,
                    "email": "-",
                    "password": "-",
                    "role": "All Users",
                    "phone_number": "-",
                    "username": "All Users",
                    "is_active": True
                }


    try:
        terminal_users = TerminalUsers.objects.filter(terminal_id = terminal_id ,is_active = True)

    except:
        terminal_users = None 

    if terminal_users:

        user_ids = list(terminal_users.values_list('user_id',flat=True).distinct())
        statuses = list(terminal_users.values_list('is_active',flat=True))

        
        
        for j in range(len(user_ids)):

           

            

            try:
                specific_user = User.objects.get(id = user_ids[j])
            except:

                specific_user = None

            print("specificuser")
            #print(specific_user.email)
            

            # user_data = {"email"}

            if specific_user:
                pass
                # user_serializer = UserSerializer(specific_user,many=False)
                # print(user_serializer)
                # user_data = user_serializer.data
                if specific_user.email:
                    email = specific_user.email
                else:
                    email = ""
                if specific_user.pwd:
                    pwd = specific_user.pwd
                else:
                    pwd = ""
                if specific_user.role:
                    role = specific_user.role
                else:
                    role = ""

                if specific_user.phone_number:
                    phone_number = specific_user.phone_number

                else:
                    phone_number = ""


                if specific_user.username:
                    username = specific_user.username

                else:
                    username = ""
                
                

                user_data = {"id":specific_user.id,"email":email,"password":pwd,"role":role,"phone_number":phone_number,"username":username,"is_active":True}
                users.append(user_data)
            else:
                pass

        users.append(all_users)
       
     
        
        return JsonResponse({"succcess":True,"message":"The data is shown","data":users})
    
    else:
        return JsonResponse({"succcess":False,"message":"There are no users"})
        


@api_view(['GET', ])
def pos_report(request,terminal_id,user_id):

    if user_id == 0:
        user_flag = True

    else:
        user_flag = False


    if user_flag == True:

        print("all users")

        try:
            orders = Order.objects.filter(is_pos=True,terminal_id=terminal_id)

        except:
            orders = None

    elif user_flag == False:

        try:
            orders = Order.objects.filter(is_pos=True,terminal_id=terminal_id,admin_id=user_id)

        except:
            orders = None

    else:
        orders = None 


    if orders:

        order_serializer = PoSOrderSerializer(orders,many=True)
        order_data = order_serializer.data

        try:
            terminal = Terminal.objects.get(id=terminal_id)

        except:
            terminal = None 

        if terminal:
            terminal_name = terminal.terminal_name
            w_id = terminal.warehouse_id
            s_id = terminal.shop_id

            if w_id == -1:
                store_id = s_id
                store_type = "Shop"
                store_name = ""
                store_location = ""

                try:
                    shop = Shop.objects.get(id=store_id)
                except:
                    shop = None 

                if shop:
                    store_name = shop.shop_name
                    store_location = shop.shop_location


            else:
                store_id = w_id
                store_type = "Warehouse"
                store_name = ""
                store_location = ""

                try:
                    shop = Warehouse.objects.get(id=store_id)
                except:
                    shop = None 

                if shop:
                    store_name = shop.warehouse_name
                    store_location = shop.warehouse_location


            store_info = {"store_id":store_id,"store_type":store_type,"store_name":store_name,"store_location":store_location}

        else:
            store_info = {"store_id":-1,"store_type":"","store_name":"","store_location":""}


        return JsonResponse({"success":True,"message":"The data is shown as follows","order_data":order_data,"store_data":store_info})

    else:
        return JsonResponse({"success":False,"message":"No Order data exists"})



@api_view(['GET', ])
def pos_invoice(request, order_id):

    # data = {'order_id': order_id}

    # invoice_serializer = InvoiceSerializer(data=data)
    # if invoice_serializer.is_valid():
    #     invoice_serializer.save()

    #     invoice_data = invoice_serializer.data

    # fetch the company Info
    print("fhbdufbdwufbdufbbw")
    # print(order_id)
    user_id = 0
    try:
        invoice = Invoice.objects.filter(order_id=order_id).last()

    except:

        invoice = None

    if invoice:

        order_id = invoice.order_id

        reference_id = invoice.ref_invoice

        invoice_serializer = InvoiceSerializer(invoice, many=False)

        invoice_data = invoice_serializer.data

        try:

            company_info = CompanyInfo.objects.all()[0:1].get()

        except:

            company_info = None

        if company_info:

            company_info_serializer = CompanyInfoSerializer(
                company_info, many=False)
            company_data = company_info_serializer.data

        else:

            company_data = {}

        # Fetch the orderdetails

        try:

            specific_order = Order.objects.get(id=order_id)

        except:

            specific_order = None

        print("specific_orderrrrrrrrr")

        print(specific_order)

        if specific_order:

            user_id = specific_order.user_id  

            
            order_serializer = PoSOrderSerializer(specific_order,many=False)
            order_data = order_serializer.data



        else:

            order_data = {}

        # Fetch the username, email, phonenumber

        try:
            userz = User.objects.get(id=user_id)
        except:
            userz = None 

        if userz:
            username = userz.username
            user_email = userz.email
            user_phone_number = userz.phone_number
            user_role = userz.role

            user_data = {"user_id":user_id,"user_email":user_email,"user_phone_number":user_phone_number,"username":username,"user_role":user_role}


        else:
            user_data = {"user_id":-1,"user_email":"","user_phone_number":"","username":"","user_role":""}




        return JsonResponse({'success': True, 'message': 'Invoice created successfully', 'invoice_data': invoice_data, 'order_data': order_data, 'user_data': user_data, 'company_data': company_data})

    else:

        return JsonResponse({'sucess': False, 'message': 'Invoice does not exist'})



# def find_mother_products(order_id):

#     mother_specification_infos = {}
#     billing_address_info = {}
#     mother_infos = []

#     try:
#         order = Order.objects.get(id = order_id)
#     except:
#         order = None


#     print(order)



#     # if order_info:
#     #     billing_address_id = order_info.billing_address_id
#     #     try:
#     #         billingaddress = BillingAddress.objects.get(id=billing_address_id)
#     #     except:



#     if order:
#         #Find all the mother site items and their quantities


#         try:
#             order_info = OrderInfo.objects.filter(order_id = order_id).last()
#         except:
#             order_info = None

#         print(order_info)

#         if order_info:
#             billing_address_id = order_info.billing_address_id

#             try:
#                 billingaddress = BillingAddress.objects.get(id=billing_address_id)
#             except:
#                 billingaddress = None

#             print(billingaddress)

#             if billingaddress:
#                 billingaddress_serializer = BillingAddressSerializer(billingaddress,many=False)
#                 billing_address_info = billingaddress_serializer.data

#                 # order_items = list(order.values_list('id',flat=True))
#                 # print(order_items)
#                 order_details = OrderDetails.objects.filter(order_id = order_id)
#                 owned = list(order_details.values_list('is_own',flat=True))
#                 order_quantities = list(order_details.values_list('total_quantity',flat=True))
#                 specification_ids = list(order_details.values_list('specification_id',flat=True))
#                 print(owned)
#                 print(order_quantities)
#                 print(specification_ids)

#                 for i in range(len(specification_ids)):
#                     if owned[i] == False:
#                         print(owned[i])
#                         try:
#                             specific_item = ProductSpecification.objects.get(id=specification_ids[i])
#                         except:
#                             specific_item = None 

#                         if specific_item:
#                             if specific_item.is_own == False:
#                                 mother_specification_id = specific_item.mother_specification_id
#                                 quantity = order_quantities[i]
#                                 mother_info = {"mother_specification_id":mother_specification_id,"quantity":quantity}
#                                 mother_infos.append(mother_info)
                
#                 print(mother_infos)

                    
#                 if len(mother_infos) > 0:
#                     print(mother_infos)
#                     print(billing_address_info)
#                     try:
#                         company= CompanyInfo.objects.all()
#                     except:
#                         company = None 

#                     if company:
#                         company = company[0]
#                         site_id = company.site_identification
#                     else:
#                         site_id = ""

#                     info_data = {"billing_address_info":billing_address_info,"mother_infos":mother_infos,"site_id":site_id}
#                     data = {"success":True,"message":"The data is shown much","data" :info_data}
#                     return data
#                 else:
#                     data = {"success":False,"message":"There are no mother site products in the order","data":{}}
#                     return data

            

#             else:
#                 data = {"success":False,"message":"The billing address does not exist","data" :{}}
#                 return data


#         else:
#             data = {"success":False,"message":"The order info does not exist","data" :{}}
#             return data


#         order_items = OrderDetails.objects.filter(order_id = order_id)

#     else:
#         data = {"success":False,"message":"The order does not exist","data" :{}}
#         return data



def find_mother_products(order_id):

    mother_specification_infos = {}
    billing_address_info = {}
    mother_infos = []

    try:
        order = Order.objects.get(id = order_id)
    except:
        order = None


    print(order)



    # if order_info:
    #     billing_address_id = order_info.billing_address_id
    #     try:
    #         billingaddress = BillingAddress.objects.get(id=billing_address_id)
    #     except:



    if order:
        #Find all the mother site items and their quantities


        try:
            order_info = OrderInfo.objects.filter(order_id = order_id).last()
        except:
            order_info = None

        print(order_info)

        if order_info:
            billing_address_id = order_info.billing_address_id

            try:
                billingaddress = BillingAddress.objects.get(id=billing_address_id)
            except:
                billingaddress = None

            print(billingaddress)

            if billingaddress:
                billingaddress_serializer = BillingAddressSerializer(billingaddress,many=False)
                billing_address_info = billingaddress_serializer.data

                # order_items = list(order.values_list('id',flat=True))
                # print(order_items)
                order_details = OrderDetails.objects.filter(order_id = order_id)
                owned = list(order_details.values_list('is_own',flat=True))
                order_quantities = list(order_details.values_list('total_quantity',flat=True))
                specification_ids = list(order_details.values_list('specification_id',flat=True))
                print(owned)
                print(order_quantities)
                print(specification_ids)

                for i in range(len(specification_ids)):
                    if owned[i] == False:
                        print(owned[i])
                        try:
                            specific_item = ProductSpecification.objects.get(id=specification_ids[i])
                        except:
                            specific_item = None 

                        if specific_item:
                            if specific_item.is_own == False:
                                mother_specification_id = specific_item.mother_specification_id
                                quantity = order_quantities[i]
                                mother_info = {"mother_specification_id":mother_specification_id,"quantity":quantity}
                                mother_infos.append(mother_info)
                
                print(mother_infos)

                    
                if len(mother_infos) > 0:
                    print(mother_infos)
                    print(billing_address_info)
                    try:
                        company= CompanyInfo.objects.all()
                    except:
                        company = None 

                    if company:
                        company = company[0]
                        company_serializer  = CompanyInfoSerializer1(company,many=False)
                        company_data = company_serializer.data
                        site_id = company.site_identification
                    else:
                        site_id = ""
                        company_data = {}

                    info_data = {"billing_address_info":billing_address_info,"mother_infos":mother_infos,"site_info":site_id,"site_data":company_data,"order_id":order_id}
                    data = {"success":True,"message":"The data is shown much","data" :info_data}
                    return data
                else:
                    data = {"success":False,"message":"There are no mother site products in the order","data":{}}
                    return data

            

            else:
                data = {"success":False,"message":"The billing address does not exist","data" :{}}
                return data


        else:
            data = {"success":False,"message":"The order info does not exist","data" :{}}
            return data


        order_items = OrderDetails.objects.filter(order_id = order_id)

    else:
        data = {"success":False,"message":"The order does not exist","data" :{}}
        return data


#Create billing addre
@api_view(['POST', ])
def create_mothersite_orders(request):

    # data = {'success': True, 
    #         'message': 'The data is shown much', 
    #         'data': {'billing_address_info': {'id': 26, 'user_id': 81, 'date_created': '2020-11-25T11:24:14.384000+06:00', 'date_updated': '2020-11-25T11:24:14.384000+06:00', 'non_verified_user_id': -1, 'ip_address': '', 'phone_number': '01757047579', 'name': 'Rabby hossain', 'address': 'Moghbazar,Dhaka', 'area': 'Dhaka', 'location': 'BimanBandar'}, 
    #         'mother_infos': [{'mother_specification_id': 345, 'quantity': 7}], 
    #         'site_id': '1234'}}\

    data = {'billing_data': {'name': 'Mother site', 'phone_number': '01731360828', 'address': 'Dhaka,Motijheel','area': 'Dhaka', 'location': 'Gulshan'}, 
        'order_data': [{'id': 365, 'is_own': False, 'child_site_id': '1234', 'child_domain': 'http://127.0.0.1:8000/', 'child_specification_id': 375, 'quantity': 1},
                     {'id': 365, 'is_own': False, 'child_site_id': '1234', 'child_domain': 'http://127.0.0.1:8000/', 'child_specification_id': 376, 'quantity': 1}]}


    data = request.data
    print(data)

    items = data["order_data"]
    mother_order_id = data["mother_order_id"]

    #create an order
    order = Order.objects.create(is_mother = True, checkout_status =True,mother_site_order_id = mother_order_id)
    order.save()
    order_id = order.id
    try:
        specific_order = Order.objects.get(id=order_id)
    except:
        specific_order = None 

    if not specific_order:
        return JsonResponse({"success":False,"message":"Some error occurred.Order could not be created"})
        
    for i in range(len(items)):
        specification_id = items[i]["child_specification_id"]
        quantity = items[i]["quantity"]
        try:
            product = ProductSpecification.objects.get(
                id=specification_id)
        except:
            product = None
        if product:
            product_id = product.product_id
            product_color = product.color
            product_size = product.size
            product_weight = product.weight
            product_unit = product.unit
        else:
            product_id = -1
            product_color = ""
            product_size = ""
            product_weight = 0.0
            product_unit = ""
        # Fetch the product name
        try:
            products = Product.objects.get(id=product_id)
        except:
            products = None
        if products:
            product_name = products.title
        else:
            product_name = ""

        # Fetch the price

        try:
            p_price = SpecificationPrice.objects.filter(
                specification_id=specification_id,status = "Single").last()
        except:
            p_price = None
        if p_price:
            price = p_price.selling_price
        else:
            price = 0.0

        unit_price = price
        total_price = price * quantity

        # Fetching the product points
        try:
            product_point = ProductPoint.objects.filter(
                specification_id=specification_id).last()
        except:
            product_point = None

        if product_point is not None:

            if product_point.point:
                p_point = product_point.point

            else:
                p_point = 0
            current_date = timezone.now().date()
            start_date = current_date
            end_date = current_date

            if product_point.start_date:
                start_date = product_point.start_date
            else:
                start_date = current_date

            if product_point.end_date:
                end_date = product_point.end_date

            else:
                end_date = current_date

            if (current_date >= start_date) and (current_date <= end_date):
                total_point = p_point * quantity
                unit_point = p_point

            else:
                total_point = 0
                unit_point = 0

        else:

            total_point = 0
            unit_point = 0
        
        # print(type(quantity))
        # print(type(unit_price))
        # print(type(unit_point))
        # print(type(total_price))
        # print(type(total_point))
        unit_point = float(unit_point)
        total_point = float(total_point)
        order_details = OrderDetails.objects.create(order_id=order_id, specification_id=specification_id, product_id=product_id, total_quantity=quantity, quantity=quantity, unit_price=unit_price, total_price=total_price, unit_point=unit_point,
                                                            total_point=total_point, product_name=product_name, product_color=product_color, product_size=product_size, product_weight=product_weight, product_unit=product_unit,is_own=True)
        order_details.save()


    
    #Create a billing address
    # {'billing_address_info': {'id': 26, 'user_id': 81, 'date_created': '2020-11-25T11:24:14.384000+06:00', 'date_updated': '2020-11-25T11:24:14.384000+06:00', 'non_verified_user_id': -1, 
    #  'ip_address': '', 'phone_number': '01757047579', 'name': 'Rabby hossain', 'address': 'Moghbazar,Dhaka', 'area': 'Dhaka', 'location': 'BimanBandar'}
    try:
        order_details = OrderDetails.objects.filter(order_id=order_id)
    except:
        order_details = None 
    billing_info = data["billing_data"] 
    billing_address = BillingAddress.objects.create(phone_number = billing_info["phone_number"],name=billing_info["name"],address=billing_info["address"],area=billing_info["area"],location=billing_info["location"])
    billing_address.save()
    billing_address_id = billing_address.id

    try:
        specific_billing_address = BillingAddress.objects.get(id=billing_address_id)
    except:
        specific_billing_address = None 

    if not specific_billing_address:
        #Delete the order and order infos
        specific_order.delete()
        if order_details:
            order_details.delete()

        return JsonResponse({"success":False,"message":"Some error occurred. Billing address could not be created"})

    
    #Create an orderinfo
    order_info = OrderInfo.objects.create(order_id = order_id, billing_address_id = billing_address_id)
    order_info.save()
    order_info_id = order_info.id


    try:
        specific_order_info = OrderInfo.objects.get(id=order_info_id)
    except:
        specific_order_info = None 

    if not specific_order_info:
        specific_billing_address.delete()
        specific_order.delete()
        if order_details:
            order_details.delete()
        return JsonResponse({"success":False,"message":"Some error occurred. Order info could not be created"})

        
    #Create the purchase invoice
    return JsonResponse({"success": True, "message":"Order has been created"})



# def create_purchase_invoice(request,data):


@api_view(['POST', ])
def create_mothersite_orders_purchase_invoice(request):

    data = {
        "order_data": {
            "id": 187,
            "date_created": "2021-01-04T11:27:29.285735+06:00",
            "order_status": "Unpaid",
            "delivery_status": "Pending",
            "admin_status": "Confirmed",
            "user_id": -1,
            "non_verified_user_id": -1,
            "ip_address": "",
            "checkout_status": True,
            "price_total": "-900.00",
            "coupon_code": "",
            "coupon_percentage": "0 %",
            "point_total": "0.00",
            "ordered_date": "2021-01-04",
            "invoice_id": 123,
            "orders": [
                {
                    "id": 451,
                    "order_status": "Unpaid",
                    "delivery_status": "Pending",
                    "order_id": 187,
                    "product_id": 334,
                    "specification_id": 359,
                    "quantity": 1,
                    "date_added": "2021-01-04T05:27:29.349Z",
                    "is_removed": False,
                    "delivery_removed": False,
                    "total_quantity": 1,
                    "unit_price": 0.0,
                    "total_price": 0.0,
                    "unit_point": 0.0,
                    "total_point": 0.0,
                    "product_name": "PURITO Defence Barrier Ph Cleanser",
                    "product_color": "none",
                    "product_size": "none",
                    "product_weight": 1.0,
                    "product_unit": "pcs",
                    "product_images": [
                        "https://tes.com.bd/media/PURITO_Defence_Barrier_Ph_Cleanser0.png",
                        "https://tes.com.bd/media/PURITO_Defence_Barrier_Ph_Cleanser1.png",
                        "https://tes.com.bd/media/PURITO_Defence_Barrier_Ph_Cleanser2.png"
                    ],
                    "remaining": 0,
                    "admin_status": "Approved",
                    "mother_admin_status": "Pending",
                    "child_admin_status": "Approved",
                    "is_own": False,
                    "product_status": "None",
                    "product_barcode": "M-1234-1-334-359-1076",
                    "can_be_added": True
                },
                {
                    "id": 452,
                    "order_status": "Unpaid",
                    "delivery_status": "Pending",
                    "order_id": 187,
                    "product_id": 8,
                    "specification_id": 345,
                    "quantity": 1,
                    "date_added": "2021-01-04T05:27:29.364Z",
                    "is_removed": False,
                    "delivery_removed": False,
                    "total_quantity": 1,
                    "unit_price": 700.0,
                    "total_price": 700.0,
                    "unit_point": 0.0,
                    "total_point": 0.0,
                    "product_name": "Kangaroo Hard Excellent",
                    "product_color": "none",
                    "product_size": "none",
                    "product_weight": 3.0,
                    "product_unit": "pcs",
                    "product_images": [
                        "https://tes.com.bd/media/hard_excellent.01.jpg",
                        "https://tes.com.bd/media/hard_excellent.02.jpg",
                        "https://tes.com.bd/media/hard_excellent.03.jpg",
                        "https://tes.com.bd/media/hard_excellent.04.jpg"
                    ],
                    "remaining": 0,
                    "admin_status": "Approved",
                    "mother_admin_status": "Pending",
                    "child_admin_status": "Approved",
                    "is_own": False,
                    "product_status": "None",
                    "product_barcode": "M-1234-1-8-345-1089",
                    "can_be_added": True
                },
                {
                    "id": 453,
                    "order_status": "Unpaid",
                    "delivery_status": "Pending",
                    "order_id": 187,
                    "product_id": 41,
                    "specification_id": 365,
                    "quantity": 1,
                    "date_added": "2021-01-04T05:27:29.370Z",
                    "is_removed": False,
                    "delivery_removed": False,
                    "total_quantity": 1,
                    "unit_price": 0.0,
                    "total_price": 0.0,
                    "unit_point": 0.0,
                    "total_point": 0.0,
                    "product_name": "Baking Powder Pore Cleansing Foam",
                    "product_color": "none",
                    "product_size": "none",
                    "product_weight": 1.0,
                    "product_unit": "pcs",
                    "product_images": [
                        "https://tes.com.bd/media/Baking-powder-pore-cleansing-foam-001.jpg",
                        "https://tes.com.bd/media/Baking-powder-pore-cleansing-foam-02.jpg",
                        "https://tes.com.bd/media/Baking-powder-pore-cleansing-foam-03.jpg",
                        "https://tes.com.bd/media/Baking-powder-pore-cleansing-foam-04.jpg"
                    ],
                    "remaining": 0,
                    "admin_status": "Approved",
                    "mother_admin_status": "Pending",
                    "child_admin_status": "Approved",
                    "is_own": False,
                    "product_status": "None",
                    "product_barcode": "M-1234-1-41-365-1099",
                    "can_be_added": True
                }
            ],
            "all_orders": [
                {
                    "id": 451,
                    "order_status": "Unpaid",
                    "delivery_status": "Pending",
                    "order_id": 187,
                    "product_id": 334,
                    "specification_id": 359,
                    "quantity": 1,
                    "date_added": "2021-01-04T05:27:29.349Z",
                    "is_removed": False,
                    "delivery_removed": False,
                    "total_quantity": 1,
                    "unit_price": 0.0,
                    "total_price": 0.0,
                    "unit_point": 0.0,
                    "total_point": 0.0,
                    "product_name": "PURITO Defence Barrier Ph Cleanser",
                    "product_color": "none",
                    "product_size": "none",
                    "product_weight": 1.0,
                    "product_unit": "pcs",
                    "product_images": [
                        "https://tes.com.bd/media/PURITO_Defence_Barrier_Ph_Cleanser0.png",
                        "https://tes.com.bd/media/PURITO_Defence_Barrier_Ph_Cleanser1.png",
                        "https://tes.com.bd/media/PURITO_Defence_Barrier_Ph_Cleanser2.png"
                    ],
                    "remaining": 0,
                    "admin_status": "Approved",
                    "mother_admin_status": "Pending",
                    "child_admin_status": "Approved",
                    "is_own": False,
                    "product_status": "None",
                    "product_barcode": "M-1234-1-334-359-1076",
                    "can_be_added": True
                },
                {
                    "id": 452,
                    "order_status": "Unpaid",
                    "delivery_status": "Pending",
                    "order_id": 187,
                    "product_id": 8,
                    "specification_id": 345,
                    "quantity": 1,
                    "date_added": "2021-01-04T05:27:29.364Z",
                    "is_removed": False,
                    "delivery_removed": False,
                    "total_quantity": 1,
                    "unit_price": 700.0,
                    "total_price": 700.0,
                    "unit_point": 0.0,
                    "total_point": 0.0,
                    "product_name": "Kangaroo Hard Excellent",
                    "product_color": "none",
                    "product_size": "none",
                    "product_weight": 3.0,
                    "product_unit": "pcs",
                    "product_images": [
                        "https://tes.com.bd/media/hard_excellent.01.jpg",
                        "https://tes.com.bd/media/hard_excellent.02.jpg",
                        "https://tes.com.bd/media/hard_excellent.03.jpg",
                        "https://tes.com.bd/media/hard_excellent.04.jpg"
                    ],
                    "remaining": 0,
                    "admin_status": "Approved",
                    "mother_admin_status": "Pending",
                    "child_admin_status": "Approved",
                    "is_own": False,
                    "product_status": "None",
                    "product_barcode": "M-1234-1-8-345-1089",
                    "can_be_added": True
                },
                {
                    "id": 453,
                    "order_status": "Unpaid",
                    "delivery_status": "Pending",
                    "order_id": 187,
                    "product_id": 41,
                    "specification_id": 365,
                    "quantity": 1,
                    "date_added": "2021-01-04T05:27:29.370Z",
                    "is_removed": False,
                    "delivery_removed": False,
                    "total_quantity": 1,
                    "unit_price": 0.0,
                    "total_price": 0.0,
                    "unit_point": 0.0,
                    "total_point": 0.0,
                    "product_name": "Baking Powder Pore Cleansing Foam",
                    "product_color": "none",
                    "product_size": "none",
                    "product_weight": 1.0,
                    "product_unit": "pcs",
                    "product_images": [
                        "https://tes.com.bd/media/Baking-powder-pore-cleansing-foam-001.jpg",
                        "https://tes.com.bd/media/Baking-powder-pore-cleansing-foam-02.jpg",
                        "https://tes.com.bd/media/Baking-powder-pore-cleansing-foam-03.jpg",
                        "https://tes.com.bd/media/Baking-powder-pore-cleansing-foam-04.jpg"
                    ],
                    "remaining": 0,
                    "admin_status": "Approved",
                    "mother_admin_status": "Pending",
                    "child_admin_status": "Approved",
                    "is_own": False,
                    "product_status": "None",
                    "product_barcode": "M-1234-1-41-365-1099",
                    "can_be_added": True
                }
            ],
            "reference_id": 0,
            "is_seller": False,
            "phone_number": "01731360828",
            "discount": "900.00",
            "sub_price": "0.00",
            "coupon_discount": "-0.00",
            "overall_discount": "900.00",
            "transaction_id": "",
            "payment_method": "",
            "can_be_cancelled": False,
            "reference_order_id": -1,
            "child_site_order_id": 174
        },
        "billing_data": {
            "name": "Mother site",
            "phone_number": "01731360828",
            "area": "Dhaka",
            "location": "Gulshan",
            "address": "Dhanmondi,Dhaka"
        }
    }

    data = request.data

    print("DATATATA ashtese")
    print(data)

    all_orders = data["order_data"]["all_orders"]
    # site_id = data["site_id"]
    order_data = data["order_data"]
    billing_data = data["billing_data"]

    order = Order.objects.create(is_purchase=True,is_mother=True,reference_order_id = order_data["child_site_order_id"],mother_site_order_id = order_data["id"])
    order.save()
    order_id = order.id

    try:
        specific_order = Order.objects.get(id = order_id)

    except:
        specific_order = None 

    if specific_order:
        #Create the order details
        for i in range(len(all_orders)):

            all_order = all_orders[i]
            
            mother_specification_id = all_order["specification_id"]
            specification_id = find_child_specification_id(mother_specification_id)
            quantity = all_order["total_quantity"]
            admin_status = all_order["admin_status"]
            product_status = all_order["product_status"]
            delivery_status = all_order["delivery_status"]
            is_own = False
            try:
                product = ProductSpecification.objects.get(
                    id=specification_id)
            except:
                product = None
            if product:
                product_id = product.product_id
                product_color = product.color
                product_size = product.size
                product_weight = product.weight
                product_unit = product.unit
            else:
                product_id = -1
                product_color = ""
                product_size = ""
                product_weight = 0.0
                product_unit = ""
            # Fetch the product name
            try:
                products = Product.objects.get(id=product_id)
            except:
                products = None
            if products:
                product_name = products.title
            else:
                product_name = ""

            # Fetch the price

            try:
                p_price = MotherSpecificationPrice.objects.filter(
                specification_id=specification_id,status = "Single").last()

        
            except:
                p_price = None

            print("PRICEEEE")
            print(p_price)
            if p_price:
                price = p_price.purchase_price
            else:
                price = 0.0


            unit_price = price
            total_price = price * quantity

            order_details = OrderDetails.objects.create(order_id=order_id, specification_id=specification_id, product_id=product_id, total_quantity=quantity, quantity=quantity, unit_price=unit_price, total_price=total_price, 
                                                         product_name=product_name, product_color=product_color, product_size=product_size, product_weight=product_weight, product_unit=product_unit,is_own=is_own,product_status=product_status,mother_admin_status=admin_status,delivery_status=delivery_status)

            order_details.save()



        try:
            order_details = OrderDetails.objects.filter(order_id=order_id)
        except:
            order_details = None 

        

        # try:
        #     child_address = ChildAddress.objects.filter(site_identification=site_id).last()
        # except:
        #     child_address = None 
        # if child_address:
            
        billing_address = BillingAddress.objects.create(phone_number = billing_data["phone_number"],name= billing_data["name"], address=billing_data["address"], area = billing_data["area"], location = billing_data["location"])
        billing_address.save()
        billing_address_id = billing_address.id

        try:
            specific_billing_address = BillingAddress.objects.get(id=billing_address_id)
        except:
            specific_billing_address = None 

        if not specific_billing_address:
            #Delete the order and order infos
            specific_order.delete()
            if order_details:
                order_details.delete()

            return JsonResponse({"success":False,"message":"Some error occurred. Billing address could not be created"})

        # else:
        #     specific_order.delete()
        #     if order_details:
        #         order_details.delete()

        #     return JsonResponse({"success":False,"message":"Some error occurred. Billing address could not be created since child address was not found"})

        
        #Create an orderinfo
        order_info = OrderInfo.objects.create(order_id = order_id, billing_address_id = billing_address_id)
        order_info.save()
        order_info_id = order_info.id


        try:
            specific_order_info = OrderInfo.objects.get(id=order_info_id)
        except:
            specific_order_info = None 

        if not specific_order_info:
            specific_billing_address.delete()
            specific_order.delete()
            if order_details:
                order_details.delete()
            return JsonResponse({"success":False,"message":"Some error occurred. Order info could not be created"})


        data = {'order_id':order_id, 'ref_invoice':0, 'is_active':True}
        invoice_serializer = InvoiceSerializer(data=data)
        if invoice_serializer.is_valid():
            invoice_serializer.save()
            #Change the statuses of the original order
            change_the_original_status = change_original(order_id)
            print("AAAAAAAAAA")
            print(change_the_original_status)
            return JsonResponse({"success": True, "message":"Order and invoice has been created"})

        else:
            specific_order_info.delete()
            specific_billing_address.delete()
            specific_order.delete()
            if order_details:
                order_details.delete()
            return JsonResponse({"success":False,"message":"Some error occurred. Order info could not be created"})


            
        #Create the purchase invoice
            
    else:

        return JsonResponse({"success":False,"message":"The order could not be created"})



def find_child_specification_id(mother_specification_id):
    print("dhukse")


    try:
        product_spec = ProductSpecification.objects.filter(mother_specification_id = mother_specification_id).last()
    except:
        product_spec = None

    print(product_spec) 

    if product_spec:
        specification_id = product_spec.id
    else:
        specification_id = -1 

    return specification_id





def change_original(order_id):

    print("METHODDDDD")

    try:
        order = Order.objects.get(id = order_id)

    except:
        order = None 

    

    all_item_data = []

    if order:
        # order.admin_status = "Confirmed"
        # order.save()
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
                item_data = {"specification_id":specific_item.specification_id,"product_status":specific_item.product_status,"admin_status":specific_item.admin_status,"mother_admin_status":specific_item.mother_admin_status,"delivery_status":specific_item.delivery_status}
                all_item_data.append(item_data)

            else:
                pass


        main_data = {"order_id":order_id,"info":all_item_data }
        print(main_data)
        change_statuses = change_orderdetails_statuses(main_data)
        return {"success":True,"message":"This invoice hass been approved","data":main_data}

            
    
    else:
        return {"success":False,"message":"This order does not exist"}



def change_orderdetails_statuses(data):

    # data = {
    #     "order_id": 195,
    #     "info": [
    #         {
    #             "specification_id": 345,
    #             "product_status": "None",
    #             "admin_status": "Pending",
    #             "child_admin_status": "Pending"
    #         },
    #         {
    #             "specification_id": 359,
    #             "product_status": "None",
    #             "admin_status": "Pending",
    #             "child_admin_status": "Pending"
    #         }
    #     ]
    # }

    order_id = data["order_id"]
    specification_infos = data["info"]
    order_details = []

    try:
        order = Order.objects.get(id=order_id)
    except:
        order = None 

    if order:
        reference_order_id = order.reference_order_id

        print(reference_order_id)

        try:
            all_items = OrderDetails.objects.filter(order_id=reference_order_id)
        except:
            all_items = None 

        print(all_items)

        if all_items:
            order_details_ids = list(all_items.values_list('id', flat=True))
        else:
            order_details_ids = []

        print(order_details_ids)

        for i in range(len(order_details_ids)):
            try:
                specific_item = OrderDetails.objects.get(id = order_details_ids[i])
            except:
                specific_item = None 

            if specific_item:
                print(specific_item)
                print(specification_infos)
                print(specific_item.specification_id)
                for j in range(len(specification_infos)):
                    if specific_item.specification_id == specification_infos[j]["specification_id"]:
                        print("ashtese")

                        specific_item.admin_status =  specification_infos[j]["admin_status"]
                        specific_item.mother_admin_status = specification_infos[j]["mother_admin_status"]
                        specific_item.product_status = specification_infos[j]["product_status"]
                        specific_item.delivery_status = specification_infos[j]["delivery_status"]
                        specific_item.save()
                        specific_data = {"specification_id":specific_item.specification_id,"product_status":specific_item.product_status,"admin_status":specific_item.admin_status,"mother_admin_status":specific_item.mother_admin_status,"delivery_status":specific_item.delivery_status}
                        order_details.append(specific_data)

    
    return order_details


@api_view(['GET', ])
def show_purchase_invoices(request):

    try:
        invoices = Order.objects.filter(is_purchase = True)

    except:
        invoices = None 

    if invoices:
        order_serializer = OrderSerializer(invoices,many=True)
        order_data = order_serializer.data

        return JsonResponse({"success":True,"message":"The data is shown","data":order_serializer.data})

    else:
        return JsonResponse({"success":False,"message":"There is no data to show."}) 


