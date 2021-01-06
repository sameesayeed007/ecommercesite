from rest_framework import serializers

from django.contrib.auth.models import User
from Intense.models import Product,Order,OrderDetails, PaymentInfo, ProductCode,ProductPrice,Userz,BillingAddress,ProductPoint,ProductSpecification,ProductImage,OrderInfo,Invoice
from Intense.models import discount_product,Cupons
from django.utils import timezone
from colour import Color

# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','title','quantity')

class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInfo
        fields = "__all__"

class OrderSerializerz(serializers.ModelSerializer):
    price_total = serializers.SerializerMethodField(method_name='get_price')
    point_total = serializers.SerializerMethodField(method_name='get_point')
    orders = serializers.SerializerMethodField(method_name='order_details')

   
    class Meta:
        model = Order
        #fields ='__all__'
        fields = ('id','date_created','order_status','delivery_status','user_id','non_verified_user_id','ip_address','checkout_status','price_total','point_total','ordered_date','orders')


    #This method is to calculate the total price
    def get_price(self,instance):
        sum_total = 0
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,product_status="None")
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('product_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(product_id=order_prices[i]).last()
                except:
                    product_price = None
                try:

                    product_discount = discount_product.objects.filter(product_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:
                    p_discount = product_discount.amount
                    start_date = product_discount.start_date
                    end_date = product_discount.end_date
                    current_date = timezone.now().date()


                    if (current_date >= start_date) and (current_date <= end_date):
                        total_discount = p_discount * order_quantity[i]
                        total_price = (p_price * order_quantity[i]) - total_discount
                        sum_total += total_price

                    else:

                        total_discount = 0
                        total_price = (p_price * order_quantity[i]) - total_discount
                        sum_total += total_price

                else:

                   
                    total_price = (p_price * order_quantity[i])
                    sum_total += total_price

        else:
            sum_total = 0

        float_total = format(sum_total, '0.2f')
        return float_total

    def get_point(self,instance):
        sum_total = 0
        try:
            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False)

        except:
            order_details = None
        if order_details is not None:

            order_prices = order_details.values_list('product_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
           
            for i in range(len(order_quantity)):
                try:
                    product_point = ProductPoint.objects.filter(product_id=order_prices[i]).last()
                except:
                    product_point = None

                if product_point is not None:
                    p_point = product_point.point
                    start_date = product_point.start_date
                    end_date = product_point.end_date
                    current_date = timezone.now().date()
                    if (current_date >= start_date) and (current_date <= end_date):
                        total_point = p_point * order_quantity[i]
                        sum_total += total_point

                else:
                    sum_total = sum_total


        else:
            sum_total = 0
               

        float_total = format(sum_total, '0.2f')
        return float_total

    def order_details(self,instance):
        details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        list_result = [entry for entry in details]
       

        return list_result



class OrderSerializerzz(serializers.ModelSerializer):
    price_total = serializers.SerializerMethodField(method_name='get_price')
    point_total = serializers.SerializerMethodField(method_name='get_point')
    orders = serializers.SerializerMethodField(method_name='order_details')
    specification = serializers.SerializerMethodField(method_name='specifications')

   
    class Meta:
        model = Order
        #fields ='__all__'
        fields = ('id','date_created','order_status','delivery_status','user_id','non_verified_user_id','ip_address','checkout_status','price_total','point_total','ordered_date','orders','specification')


    #This method is to calculate the total price
    def get_price(self,instance):
        sum_total = 0
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False)
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('product_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(product_id=order_prices[i]).last()
                except:
                    product_price = None
                try:

                    product_discount = discount_product.objects.filter(product_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:
                    p_discount = product_discount.amount
                    start_date = product_discount.start_date
                    end_date = product_discount.end_date
                    current_date = timezone.now().date()


                    if (current_date >= start_date) and (current_date <= end_date):
                        total_discount = p_discount * order_quantity[i]
                        total_price = (p_price * order_quantity[i]) - total_discount
                        sum_total += total_price

                    else:

                        total_discount = 0
                        total_price = (p_price * order_quantity[i]) - total_discount
                        sum_total += total_price

                else:

                   
                    total_price = (p_price * order_quantity[i])
                    sum_total += total_price

        else:
            sum_total = 0

        float_total = format(sum_total, '0.2f')
        return float_total

    def get_point(self,instance):
        sum_total = 0
        try:
            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False)

        except:
            order_details = None
        if order_details is not None:

            order_prices = order_details.values_list('product_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
           
            for i in range(len(order_quantity)):
                try:
                    product_point = ProductPoint.objects.filter(product_id=order_prices[i]).last()
                except:
                    product_point = None

                if product_point is not None:
                    p_point = product_point.point
                    start_date = product_point.start_date
                    end_date = product_point.end_date
                    current_date = timezone.now().date()
                    if (current_date >= start_date) and (current_date <= end_date):
                        total_point = p_point * order_quantity[i]
                        sum_total += total_point

                else:
                    sum_total = sum_total


        else:
            sum_total = 0
               

        float_total = format(sum_total, '0.2f')
        return float_total

    def order_details(self,instance):
        details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        list_result = [entry for entry in details]
       

        return list_result


    def specifications(self,instance):

        num =-1

        arr = {
        "id": num ,
        "product_id":num ,
        "color": [

        ],
        "size": [
         
        ],
        "unit": [
                    ],
        "weight": ""
    }

        try:
            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False)

        except:

            order_details = None

        if order_details is not None:
            order_products = order_details.values_list('product_id',flat = True)
            for i in range(len(order_products)):
                try:
                    spec = ProductSpecification.objects.filter(product_id=order_products[i]).last()
                except:
                    spec = None

            if spec is not None:
                arr = {
                        "id": spec.id ,
                        "product_id":spec.product_id,
                        "color": spec.color,
                        "size" : spec.size,
                        "weight": spec.weight
                    }


            return arr
     




       



# class OrderSerializer(serializers.ModelSerializer):
#     price_total = serializers.SerializerMethodField(method_name='get_price')
#     point_total = serializers.SerializerMethodField(method_name='get_point')
#     orders = serializers.SerializerMethodField(method_name='order_details')
#     #orders = serializers.SerializerMethodField(method_name='order_details')
#     coupon_percentage = serializers.SerializerMethodField(method_name='get_coupon')
#     #product = serializers.SerializerMethodField(method_name='get_coupon')

   
#     class Meta:
#         model = Order
#         #fields ='__all__'
#         fields = ('id','date_created','order_status','delivery_status','admin_status','user_id','non_verified_user_id','ip_address','checkout_status','price_total','coupon_code','coupon_percentage','point_total','ordered_date','orders')


#     #This method is to calculate the total price
#     def get_price(self,instance):
#         sum_total = 0
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False)
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('product_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(product_id=order_prices[i]).last()
#                 except:
#                     product_price = None
#                 try:

#                     product_discount = discount_product.objects.filter(product_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:
#                     p_discount = product_discount.amount
#                     current_date = timezone.now().date()
#                     start_date = current_date
#                     end_date = current_date
                   

#                     if product_discount.start_date:
#                         start_date = product_discount.start_date
#                     else:
#                         start_date = current_date

#                     if product_discount.end_date:
#                         end_date = product_discount.end_date

#                     else:

#                         end_date = current_date


#                     if (current_date >= start_date) and (current_date <= end_date):
#                         total_discount = p_discount * order_quantity[i]
#                         total_price = (p_price * order_quantity[i]) - total_discount
#                         sum_total += total_price

#                     else:

#                         total_discount = 0
#                         total_price = (p_price * order_quantity[i]) - total_discount
#                         sum_total += total_price

#                 else:

                   
#                     total_price = (p_price * order_quantity[i])
#                     sum_total += total_price

#         else:
#             sum_total = 0

#         current_date = timezone.now().date()
#         coupon_percent = 0


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break


#             coupon_amount = (sum_total * coupon_percent)/100
#             sum_total = sum_total - coupon_amount

#         else:

#             sum_total = sum_total

#         float_total = format(sum_total, '0.2f')
#         return float_total


#     def get_coupon(self,instance):

#         current_date = timezone.now().date()
#         coupon_percent = 0


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break

#         else:
#             coupon_percent = 0


#         coupon_percentage = str(coupon_percent)+" %"

#         return coupon_percentage


#     def get_point(self,instance):
#         sum_total = 0
#         try:
#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False)

#         except:
#             order_details = None
#         if order_details is not None:

#             order_prices = order_details.values_list('product_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
           
#             for i in range(len(order_quantity)):
#                 try:
#                     product_point = ProductPoint.objects.filter(product_id=order_prices[i]).last()
#                 except:
#                     product_point = None

#                 if product_point is not None:
#                     p_point = product_point.point
#                     current_date = timezone.now().date()

#                     start_date = current_date
#                     end_date = current_date

#                     if product_point.start_date:
#                         start_date = product_point.start_date
#                     else:
#                         start_date = current_date

#                     if product_point.end_date:
#                         end_date = product_point.end_date

#                     else:

#                         end_date = current_date
                   
#                     if (current_date >= start_date) and (current_date <= end_date):
#                         total_point = p_point * order_quantity[i]
#                         sum_total += total_point

#                 else:
#                     sum_total = sum_total


#         else:
#             sum_total = 0
               

#         float_total = format(sum_total, '0.2f')
#         return float_total


#     def order_details(self,instance):
#         details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).order_by('date_added').values()
#         list_result = [entry for entry in details]
#         for i in range(len(list_result)):
#             product_id = list_result[i]['product_id']
#             try:
#                 product_images = ProductImage.objects.filter(product_id = product_id)
#             except:
#                 product_images = None

#             images= []

#             if product_images:
#                 images= list(product_images.values_list('image_url',flat=True).distinct())

#             list_result[i]['product_images'] = images

       

#         return list_result

class OrderSerializer3(serializers.ModelSerializer):
    price_total = serializers.SerializerMethodField(method_name='get_price')
    point_total = serializers.SerializerMethodField(method_name='get_point')
    orders = serializers.SerializerMethodField(method_name='order_details')
    all_orders = serializers.SerializerMethodField(method_name='order_detailz')
    #orders = serializers.SerializerMethodField(method_name='order_details')
    coupon_percentage = serializers.SerializerMethodField(method_name='get_coupon')
    #product = serializers.SerializerMethodField(method_name='get_coupon')
    invoice_id = serializers.SerializerMethodField(method_name='get_invoice_id')
    reference_id = serializers.SerializerMethodField(method_name='get_reference')
    phone_number = serializers.SerializerMethodField(method_name='get_phone_number')

   
    class Meta:
        model = Order
        #fields ='__all__'
        fields = ('id','date_created','order_status','delivery_status','admin_status','user_id','non_verified_user_id','ip_address','checkout_status','price_total','coupon_code','coupon_percentage','point_total','ordered_date','invoice_id','orders','all_orders','reference_id','is_seller','phone_number','transaction_id','payment_method')

    
    def get_phone_number(self,instance):

        phone_number = ""

        try:
            order_info = OrderInfo.objects.get(order_id=instance.id)

        except:
            order_info = None 

        print("order_info")
        print(order_info)

        if order_info:

            if order_info.billing_address_id:
                billing_address_id = order_info.billing_address_id

            else:
                billing_address_id = 0




            try:
                billing_address = BillingAddress.objects.get(id=billing_address_id)
            except:
                billing_address = None 


            print("billingaddress")
            print(billing_address)

            if billing_address:
                if billing_address.phone_number:
                    phone_number = billing_address.phone_number

                else:
                    phone_number = ""

            else:
                phone_number = ""

        else:
            phone_number = ""

        return phone_number
            


    #This method is to calculate the total price
    def get_price(self,instance):
        sum_total = 0
        print("price")
        
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,delivery_removed=False,product_status="None",admin_status="Pending")|OrderDetails.objects.filter(order_id = instance.id,is_removed=False,delivery_removed=False,product_status="None",admin_status="Approved")
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        print()

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price


                    elif product_discount.discount_type == "percentage":

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                    else:

                        total_price = (p_price * order_quantity[i])
                        sum_total += total_price


                else:

                   
                    total_price = (p_price * order_quantity[i])
                    sum_total += total_price


                print("sum total")


                print(sum_total)

        else:
            sum_total = 0

        current_date = timezone.now().date()
        coupon_percent = 0


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break


            coupon_amount = (sum_total * coupon_percent)/100
            sum_total = sum_total - coupon_amount

        else:

            sum_total = sum_total

        float_total = format(sum_total, '0.2f')
        return float_total


    def get_coupon(self,instance):

        current_date = timezone.now().date()
        coupon_percent = 0


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break

        else:
            coupon_percent = 0


        coupon_percentage = str(coupon_percent)+" %"

        return coupon_percentage


    def get_point(self,instance):
        sum_total = 0
        try:
            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,delivery_removed=False,product_status="None",admin_status="Pending")|OrderDetails.objects.filter(order_id = instance.id,is_removed=False,delivery_removed=False,product_status="None",admin_status="Approved")

        except:
            order_details = None
        if order_details is not None:

            order_prices = order_details.values_list('product_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
           
            for i in range(len(order_quantity)):
                try:
                    product_point = ProductPoint.objects.filter(product_id=order_prices[i]).last()
                except:
                    product_point = None

                if product_point is not None:
                    p_point = product_point.point
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
                        total_point = p_point * order_quantity[i]
                        sum_total += total_point

                else:
                    sum_total = sum_total


        else:
            sum_total = 0
               

        float_total = format(sum_total, '0.2f')
        return float_total


    def order_details(self,instance):
        print("yuuuuuuu")
        # print(self.id)
        details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,delivery_removed=False,product_status="None").order_by('date_added').values()
        list_result = [entry for entry in details]
        for i in range(len(list_result)):
            product_id = list_result[i]['product_id']
            specification_id = list_result[i]['specification_id']
            print("specccc")
            print(specification_id)
            try:
                product_images = ProductImage.objects.filter(product_id = product_id)
            except:
                product_images = None

            images= []

            if product_images:
                images= list(product_images.values_list('image_url',flat=True).distinct())

            list_result[i]['product_images'] = images

            try:
                barcode = ProductCode.objects.filter(specification_id=specification_id).last()

            except:
                barcode = None 

            print(barcode)

            product_barcode = ""

            if barcode:
                print("ashtese")
                print(barcode.Barcode)
                product_barcode = barcode.Barcode
                print(product_barcode)

            list_result[i]['product_barcode'] = product_barcode
        

       

        return list_result


    def get_invoice_id(self,instance):

        try:

            invoice = Invoice.objects.filter(order_id=instance.id).last()

        except:

            invoice = None 

        if invoice:

            if invoice.id:

                invoice_id = invoice.id

            else:

                invoice_id = 0 

        else:

            invoice_id = 0 


        return invoice_id


    def get_reference(self,instance):

        try:

            invoice = Invoice.objects.filter(order_id=instance.id).last()

        except:

            invoice = None 

        if invoice:

            if invoice.ref_invoice:

                invoice_id = invoice.ref_invoice

            else:

                invoice_id = 0 

        else:

            invoice_id = 0 


        return invoice_id


    def order_detailz(self,instance):
        details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).order_by('date_added').values()
        list_result = [entry for entry in details]
        for i in range(len(list_result)):
            product_id = list_result[i]['product_id']
            specification_id = list_result[i]['specification_id']
            try:
                product_images = ProductImage.objects.filter(product_id = product_id)
            except:
                product_images = None

            images= []

            if product_images:
                images= list(product_images.values_list('image_url',flat=True).distinct())

            list_result[i]['product_images'] = images

            try:
                barcode = ProductCode.objects.filter(specification_id=specification_id).last()

            except:
                barcode = None 

            product_barcode = ""

            if barcode:
                product_barcode = barcode.Barcode

            list_result[i]['product_barcode'] = product_barcode

       

        return list_result

class OrderSerializer(serializers.ModelSerializer):
    price_total = serializers.SerializerMethodField(method_name='get_price')
    point_total = serializers.SerializerMethodField(method_name='get_point')
    orders = serializers.SerializerMethodField(method_name='order_details')
    all_orders = serializers.SerializerMethodField(method_name='order_detailz')
    #orders = serializers.SerializerMethodField(method_name='order_details')
    coupon_percentage = serializers.SerializerMethodField(method_name='get_coupon')
    #product = serializers.SerializerMethodField(method_name='get_coupon')
    invoice_id = serializers.SerializerMethodField(method_name='get_invoice_id')
    reference_id = serializers.SerializerMethodField(method_name='get_reference')
    phone_number = serializers.SerializerMethodField(method_name='get_phone_number')
    discount = serializers.SerializerMethodField(method_name='get_discount')
    sub_price = serializers.SerializerMethodField(method_name='get_sub_price')
    coupon_discount = serializers.SerializerMethodField(method_name='get_coupon_discount')
    overall_discount = serializers.SerializerMethodField(method_name='get_overall_discount')
    can_be_cancelled = serializers.SerializerMethodField(method_name='get_cancel_status')

   
    class Meta:
        model = Order
        #fields ='__all__'
        fields = ('id','order_status','delivery_status','admin_status','user_id','non_verified_user_id','ip_address','checkout_status','price_total','coupon_code','coupon_percentage','point_total','ordered_date','invoice_id','orders','all_orders','reference_id','is_seller','phone_number','discount','sub_price','coupon_discount','overall_discount','transaction_id','payment_method','can_be_cancelled','mother_site_order_id')

    def get_cancel_status(self,instance):

        flag = True

        try:
            order_details = OrderDetails.objects.filter(order_id = instance.id)
        except:
            order_details = None 

        if order_details:

            is_owns =  list(order_details.values_list('is_own',flat=True))

        else:
            is_owns = []


        if False in is_owns:
            return False

        else:
            return True
            
    
    def get_phone_number(self,instance):

        phone_number = ""

        try:
            order_info = OrderInfo.objects.get(order_id=instance.id)

        except:
            order_info = None 

        print("order_info")
        print(order_info)

        if order_info:

            if order_info.billing_address_id:
                billing_address_id = order_info.billing_address_id

            else:
                billing_address_id = 0




            try:
                billing_address = BillingAddress.objects.get(id=billing_address_id)
            except:
                billing_address = None 


            print("billingaddress")
            print(billing_address)

            if billing_address:
                if billing_address.phone_number:
                    phone_number = billing_address.phone_number

                else:
                    phone_number = ""

            else:
                phone_number = ""

        else:
            phone_number = ""

        return phone_number
            


    #This method is to calculate the total price
    def get_price(self,instance):
        sum_total = 0
        admin = ["Pending","Approved"]
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,delivery_removed=False,product_status="None",admin_status__in=admin)
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
            print("totalprice")
            print(len(order_quantity))
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        print()

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price


                    elif product_discount.discount_type == "percentage":

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                    else:

                        total_price = (p_price * order_quantity[i])
                        sum_total += total_price


                else:

                   
                    total_price = (p_price * order_quantity[i])
                    sum_total += total_price


                print("sum total")


                print(sum_total)

        else:
            sum_total = 0

        current_date = timezone.now().date()
        coupon_percent = 0


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break


            coupon_amount = (sum_total * coupon_percent)/100
            sum_total = sum_total - coupon_amount

        else:

            sum_total = sum_total

        float_total = format(sum_total, '0.2f')
        return float_total


    def get_coupon(self,instance):

        current_date = timezone.now().date()
        coupon_percent = 0


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break

        else:
            coupon_percent = 0


        coupon_percentage = str(coupon_percent)+" %"

        return coupon_percentage


    def get_point(self,instance):
        sum_total = 0
        admin = ["Pending","Approved"]
        try:
            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,delivery_removed=False,product_status="None",admin_status__in=admin)

        except:
            order_details = None
        if order_details is not None:

            order_prices = order_details.values_list('product_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            print("point_total")
            print(len(order_quantity))
           
            for i in range(len(order_quantity)):
                try:
                    product_point = ProductPoint.objects.filter(product_id=order_prices[i]).last()
                except:
                    product_point = None

                if product_point is not None:
                    p_point = product_point.point
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
                        total_point = p_point * order_quantity[i]
                        sum_total += total_point

                else:
                    sum_total = sum_total


        else:
            sum_total = 0
               

        float_total = format(sum_total, '0.2f')
        return float_total


    def order_details(self,instance):
        details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,delivery_removed=False,product_status="None").order_by('date_added').values()
        list_result = [entry for entry in details]
        for i in range(len(list_result)):
            product_id = list_result[i]['product_id']
            specification_id = list_result[i]['specification_id']
            try:
                product_images = ProductImage.objects.filter(product_id = product_id)
            except:
                product_images = None

            images= []

            if product_images:
                images= list(product_images.values_list('image_url',flat=True).distinct())

            list_result[i]['product_images'] = images

            try:
                barcode = ProductCode.objects.filter(specification_id=specification_id).last()

            except:
                barcode = None 

            product_barcode = ""

            if barcode:
                product_barcode = barcode.Barcode

            list_result[i]['product_barcode'] = product_barcode
            list_result[i]['date_added'] = ""

       

        return list_result


    def get_invoice_id(self,instance):

        try:

            invoice = Invoice.objects.filter(order_id=instance.id).last()

        except:

            invoice = None 

        if invoice:

            if invoice.id:

                invoice_id = invoice.id

            else:

                invoice_id = 0 

        else:

            invoice_id = 0 


        return invoice_id


    def get_reference(self,instance):

        try:

            invoice = Invoice.objects.filter(order_id=instance.id).last()

        except:

            invoice = None 

        if invoice:

            if invoice.ref_invoice:

                invoice_id = invoice.ref_invoice

            else:

                invoice_id = 0 

        else:

            invoice_id = 0 


        return invoice_id


    def order_detailz(self,instance):
        details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,delivery_removed=False).order_by('date_added').values()
        list_result = [entry for entry in details]
        for i in range(len(list_result)):
            product_id = list_result[i]['product_id']
            specification_id = list_result[i]['specification_id']
            try:
                product_images = ProductImage.objects.filter(product_id = product_id)
            except:
                product_images = None

            images= []

            if product_images:
                images= list(product_images.values_list('image_url',flat=True).distinct())

            list_result[i]['product_images'] = images

            
            try:
                barcode = ProductCode.objects.filter(specification_id=specification_id).last()

            except:
                barcode = None 

            product_barcode = ""

            if barcode:
                product_barcode = barcode.Barcode

            list_result[i]['product_barcode'] = product_barcode
            list_result[i]['date_added'] = ""

           

       

        return list_result


        #This method is to calculate the total price
    def get_sub_price(self,instance):
        sum_total = 0
        admin = ["Pending","Approved"]
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in = admin,product_status="None",delivery_removed=False)
        except:
            order_details = None

        # print("sub price")
        # print(len(order_quantity))

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
            print("sub price")
            print(len(order_quantity))
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                # try:

                #     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                # except:
                #     product_discount = None
               

                if product_price:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                # if product_discount is not None:

                #     if product_discount.discount_type == "amount":

                #         print()

                #         if product_discount.amount:
                #             p_discount = product_discount.amount
                #         else:
                #             p_discount = 0

                   
                #         current_date = timezone.now().date()
                #         start_date = current_date
                #         end_date = current_date
                       

                #         if product_discount.start_date:
                #             start_date = product_discount.start_date
                #         else:
                #             start_date = current_date

                #         if product_discount.end_date:
                #             end_date = product_discount.end_date

                #         else:

                #             end_date = current_date


                #         if (current_date >= start_date) and (current_date <= end_date):
                #             total_discount = p_discount * order_quantity[i]
                #             total_price = (p_price * order_quantity[i]) - total_discount
                #             sum_total += total_price

                #         else:

                #             total_discount = 0
                #             total_price = (p_price * order_quantity[i]) - total_discount
                #             sum_total += total_price


                #     elif product_discount.discount_type == "percentage":

                #         if product_discount.amount:
                #             p_discount = product_discount.amount
                #             p_discount = (p_discount * p_price)/100
                #         else:
                #             p_discount = 0

                   
                #         current_date = timezone.now().date()
                #         start_date = current_date
                #         end_date = current_date
                       

                #         if product_discount.start_date:
                #             start_date = product_discount.start_date
                #         else:
                #             start_date = current_date

                #         if product_discount.end_date:
                #             end_date = product_discount.end_date

                #         else:

                #             end_date = current_date


                #         if (current_date >= start_date) and (current_date <= end_date):
                #             total_discount = p_discount * order_quantity[i]
                #             total_price = (p_price * order_quantity[i]) - total_discount
                #             sum_total += total_price

                #         else:

                #             total_discount = 0
                #             total_price = (p_price * order_quantity[i]) - total_discount
                #             sum_total += total_price

                #     else:

                #         total_price = (p_price * order_quantity[i])
                #         sum_total += total_price


                # else:

                   
                total_price = (p_price * order_quantity[i])
                sum_total += total_price


                print("sum total")


                print(sum_total)

        else:
            sum_total = 0

        # current_date = timezone.now().date()
        # coupon_percent = 0


        float_total = format(sum_total, '0.2f')
        return float_total




        # try:
        #     order = Order.objects.get(pk=instance.id)

        # except:
        #     order = None

        # if order:

        #     coupon_code = order.coupon_code

        #     coupons = Cupons.objects.all()
        #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
        #     coupon_amounts = list(coupons.values_list('amount',flat=True))
        #     coupon_start = list(coupons.values_list('start_from',flat=True))
        #     coupon_end = list(coupons.values_list('valid_to',flat=True))
        #     coupon_validity = list(coupons.values_list('is_active',flat=True))

        #     for i in range(len(coupon_codes)):
        #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
        #             coupon_percent = coupon_amounts[i]
        #             break


        #     coupon_amount = (sum_total * coupon_percent)/100
        #     sum_total = sum_total - coupon_amount

        # else:

        #     sum_total = sum_total



        #This method is to calculate the total price
    def get_discount(self,instance):
        sum_total = 0
        discount_total = 0 
        admin = ["Pending","Approved"]
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in=admin,product_status="None",delivery_removed=False)
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
            print("discount")
            print(len(order_quantity))
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount


                    elif product_discount.discount_type == "percentage":

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount

                    else:

                        total_price = (p_price * order_quantity[i])
                        # sum_total += total_price
                        discount_total += 0 


                else:

                   
                    # total_price = (p_price * order_quantity[i])
                    #sum_total += total_discount
                    discount_total += 0 


                print("sum total")


                # print(sum_total)

        else:
            discount_total = 0

        # current_date = timezone.now().date()
        # coupon_percent = 0


        # try:
        #     order = Order.objects.get(pk=instance.id)

        # except:
        #     order = None

        # if order:

        #     coupon_code = order.coupon_code

        #     coupons = Cupons.objects.all()
        #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
        #     coupon_amounts = list(coupons.values_list('amount',flat=True))
        #     coupon_start = list(coupons.values_list('start_from',flat=True))
        #     coupon_end = list(coupons.values_list('valid_to',flat=True))
        #     coupon_validity = list(coupons.values_list('is_active',flat=True))

        #     for i in range(len(coupon_codes)):
        #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
        #             coupon_percent = coupon_amounts[i]
        #             break


        #     coupon_amount = (sum_total * coupon_percent)/100
        #     sum_total = sum_total - coupon_amount

        # else:

        #     sum_total = sum_total

        float_total = format(discount_total, '0.2f')
        return float_total



        #This method is to calculate the total price
    def get_coupon_discount(self,instance):
        sum_total = 0
        admin = ["Pending","Approved"]
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in =admin,product_status="None",delivery_removed=False)
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        print()

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price


                    elif product_discount.discount_type == "percentage":

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                    else:

                        total_price = (p_price * order_quantity[i])
                        sum_total += total_price


                else:

                   
                    total_price = (p_price * order_quantity[i])
                    sum_total += total_price


                print("sum total")


                print(sum_total)

        else:
            sum_total = 0

        current_date = timezone.now().date()
        coupon_percent = 0
        coupon_amount = 0 


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break


            coupon_amount = (sum_total * coupon_percent)/100
            #sum_total = sum_total - coupon_amount
            # sum_total = coupon_amount

        else:

            sum_total = sum_total
            coupon_amount = 0 

        float_total = format(coupon_amount, '0.2f')
        return float_total



    def get_overall_discount(self,instance):
        sum_total = 0
        discount_total = 0
        admin = ["Pending","Approved"]
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in = admin,product_status="None",delivery_removed=False)
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            discount_total = 0 
            p_price = 0
            print("overalldiscount")
            print(len(order_quantity))
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None

                print("product_discount")

                # print(product_discount.specification_id)
                # print(product_discount.amount)
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        print("amount ey dhuktese")

                        

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount


                    elif product_discount.discount_type == "percentage":


                        print("percentage ey dhuktese")

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount

                    else:

                        total_discount = 0 

                        total_price = (p_price * order_quantity[i])
                        sum_total += total_price
                        discount_total += total_discount


                else:

                   
                    total_price = (p_price * order_quantity[i])
                    sum_total += total_price
                    total_discount = 0 
                    discount_total += total_discount


                print("sum total")


                print(discount_total)

        else:
            discount_total = 0
            sum_total = 0

        current_date = timezone.now().date()
        coupon_percent = 0
        coupon_amount = 0
        coupon_total = 0 


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break


            coupon_amount = (sum_total * coupon_percent)/100
            #sum_total = sum_total - coupon_amount
            # sum_total = coupon_amount

        else:

            sum_total = sum_total
            coupon_amount = 0 

        total = coupon_amount + discount_total

        float_total = format(total, '0.2f')
        return float_total










# class OrderInvoiceSerializer(serializers.ModelSerializer):
#     price_total = serializers.SerializerMethodField(method_name='get_price')
#     point_total = serializers.SerializerMethodField(method_name='get_point')
#     orders = serializers.SerializerMethodField(method_name='order_details')
#     #orders = serializers.SerializerMethodField(method_name='order_details')
#     coupon_percentage = serializers.SerializerMethodField(method_name='get_coupon')
#     #product = serializers.SerializerMethodField(method_name='get_coupon')
#     invoice_id = serializers.SerializerMethodField(method_name='get_invoice_id')
#     reference_id = serializers.SerializerMethodField(method_name='get_reference')
#     discount = serializers.SerializerMethodField(method_name='get_discount')
#     sub_price = serializers.SerializerMethodField(method_name='get_sub_price')
#     coupon_discount = serializers.SerializerMethodField(method_name='get_coupon_discount')
#     overall_discount = serializers.SerializerMethodField(method_name='get_overall_discount')
#     all_orders = serializers.SerializerMethodField(method_name='all_order_details')

   
#     class Meta:
#         model = Order
#         #fields ='__all__'
#         fields = ('id','date_created','order_status','delivery_status','admin_status','user_id','non_verified_user_id','ip_address','checkout_status','sub_price','discount','coupon_discount','overall_discount','price_total','coupon_code','coupon_percentage','point_total','ordered_date','invoice_id','reference_id','orders','all_orders')

#     # def get_discount(self,instance):

#     #     pass



#     def get_reference(self,instance):

#         try:

#             invoice = Invoice.objects.filter(order_id=instance.id).last()

#         except:

#             invoice = None 

#         if invoice:

#             if invoice.ref_invoice:

#                 invoice_id = invoice.ref_invoice

#             else:

#                 invoice_id = 0 

#         else:

#             invoice_id = 0 


#         return invoice_id


#     #This method is to calculate the total price
#     def get_sub_price(self,instance):
#         sum_total = 0
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",product_status="None",delivery_removed=False)
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 # try:

#                 #     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 # except:
#                 #     product_discount = None
               

#                 if product_price:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 # if product_discount is not None:

#                 #     if product_discount.discount_type == "amount":

#                 #         print()

#                 #         if product_discount.amount:
#                 #             p_discount = product_discount.amount
#                 #         else:
#                 #             p_discount = 0

                   
#                 #         current_date = timezone.now().date()
#                 #         start_date = current_date
#                 #         end_date = current_date
                       

#                 #         if product_discount.start_date:
#                 #             start_date = product_discount.start_date
#                 #         else:
#                 #             start_date = current_date

#                 #         if product_discount.end_date:
#                 #             end_date = product_discount.end_date

#                 #         else:

#                 #             end_date = current_date


#                 #         if (current_date >= start_date) and (current_date <= end_date):
#                 #             total_discount = p_discount * order_quantity[i]
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price

#                 #         else:

#                 #             total_discount = 0
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price


#                 #     elif product_discount.discount_type == "percentage":

#                 #         if product_discount.amount:
#                 #             p_discount = product_discount.amount
#                 #             p_discount = (p_discount * p_price)/100
#                 #         else:
#                 #             p_discount = 0

                   
#                 #         current_date = timezone.now().date()
#                 #         start_date = current_date
#                 #         end_date = current_date
                       

#                 #         if product_discount.start_date:
#                 #             start_date = product_discount.start_date
#                 #         else:
#                 #             start_date = current_date

#                 #         if product_discount.end_date:
#                 #             end_date = product_discount.end_date

#                 #         else:

#                 #             end_date = current_date


#                 #         if (current_date >= start_date) and (current_date <= end_date):
#                 #             total_discount = p_discount * order_quantity[i]
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price

#                 #         else:

#                 #             total_discount = 0
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price

#                 #     else:

#                 #         total_price = (p_price * order_quantity[i])
#                 #         sum_total += total_price


#                 # else:

                   
#                 total_price = (p_price * order_quantity[i])
#                 sum_total += total_price


#                 print("sum total")


#                 print(sum_total)

#         else:
#             sum_total = 0

#         # current_date = timezone.now().date()
#         # coupon_percent = 0


#         float_total = format(sum_total, '0.2f')
#         return float_total




#         # try:
#         #     order = Order.objects.get(pk=instance.id)

#         # except:
#         #     order = None

#         # if order:

#         #     coupon_code = order.coupon_code

#         #     coupons = Cupons.objects.all()
#         #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#         #     coupon_amounts = list(coupons.values_list('amount',flat=True))
#         #     coupon_start = list(coupons.values_list('start_from',flat=True))
#         #     coupon_end = list(coupons.values_list('valid_to',flat=True))
#         #     coupon_validity = list(coupons.values_list('is_active',flat=True))

#         #     for i in range(len(coupon_codes)):
#         #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#         #             coupon_percent = coupon_amounts[i]
#         #             break


#         #     coupon_amount = (sum_total * coupon_percent)/100
#         #     sum_total = sum_total - coupon_amount

#         # else:

#         #     sum_total = sum_total



#         #This method is to calculate the total price
#     def get_discount(self,instance):
#         sum_total = 0
#         discount_total = 0 
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",product_status="None",delivery_removed=False)
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

#                         print()

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount


#                     elif product_discount.discount_type == "percentage":

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount

#                     else:

#                         total_price = (p_price * order_quantity[i])
#                         # sum_total += total_price
#                         discount_total += 0 


#                 else:

                   
#                     # total_price = (p_price * order_quantity[i])
#                     #sum_total += total_discount
#                     discount_total += 0 


#                 print("sum total")


#                 # print(sum_total)

#         else:
#             discount_total = 0

#         # current_date = timezone.now().date()
#         # coupon_percent = 0


#         # try:
#         #     order = Order.objects.get(pk=instance.id)

#         # except:
#         #     order = None

#         # if order:

#         #     coupon_code = order.coupon_code

#         #     coupons = Cupons.objects.all()
#         #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#         #     coupon_amounts = list(coupons.values_list('amount',flat=True))
#         #     coupon_start = list(coupons.values_list('start_from',flat=True))
#         #     coupon_end = list(coupons.values_list('valid_to',flat=True))
#         #     coupon_validity = list(coupons.values_list('is_active',flat=True))

#         #     for i in range(len(coupon_codes)):
#         #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#         #             coupon_percent = coupon_amounts[i]
#         #             break


#         #     coupon_amount = (sum_total * coupon_percent)/100
#         #     sum_total = sum_total - coupon_amount

#         # else:

#         #     sum_total = sum_total

#         float_total = format(discount_total, '0.2f')
#         return float_total



#         #This method is to calculate the total price
#     def get_coupon_discount(self,instance):
#         sum_total = 0
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",product_status="None",delivery_removed=False)
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

#                         print()

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price


#                     elif product_discount.discount_type == "percentage":

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                     else:

#                         total_price = (p_price * order_quantity[i])
#                         sum_total += total_price


#                 else:

                   
#                     total_price = (p_price * order_quantity[i])
#                     sum_total += total_price


#                 print("sum total")


#                 print(sum_total)

#         else:
#             sum_total = 0

#         current_date = timezone.now().date()
#         coupon_percent = 0
#         coupon_amount = 0 


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break


#             coupon_amount = (sum_total * coupon_percent)/100
#             #sum_total = sum_total - coupon_amount
#             # sum_total = coupon_amount

#         else:

#             sum_total = sum_total
#             coupon_amount = 0 

#         float_total = format(coupon_amount, '0.2f')
#         return float_total



#     def get_overall_discount(self,instance):
#         sum_total = 0
#         discount_total = 0
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",product_status="None",delivery_removed=False)
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             discount_total = 0 
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

#                         print()

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount


#                     elif product_discount.discount_type == "percentage":

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount

#                     else:

#                         total_price = (p_price * order_quantity[i])
#                         sum_total += total_price
#                         discount_total += total_discount


#                 else:

                   
#                     total_price = (p_price * order_quantity[i])
#                     sum_total += total_price
#                     total_discount = 0 
#                     discount_total += total_discount


#                 print("sum total")


#                 print(sum_total)

#         else:
#             discount_total = 0
#             sum_total = 0

#         current_date = timezone.now().date()
#         coupon_percent = 0
#         coupon_amount = 0
#         coupon_total = 0 


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break


#             coupon_amount = (sum_total * coupon_percent)/100
#             #sum_total = sum_total - coupon_amount
#             # sum_total = coupon_amount

#         else:

#             sum_total = sum_total
#             coupon_amount = 0 

#         total = coupon_amount + discount_total

#         float_total = format(total, '0.2f')
#         return float_total











#     #This method is to calculate the total price
#     def get_price(self,instance):
#         sum_total = 0
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",product_status="None",delivery_removed=False)
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

#                         print()

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price


#                     elif product_discount.discount_type == "percentage":

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                     else:

#                         total_price = (p_price * order_quantity[i])
#                         sum_total += total_price


#                 else:

                   
#                     total_price = (p_price * order_quantity[i])
#                     sum_total += total_price


#                 print("sum total")


#                 print(sum_total)

#         else:
#             sum_total = 0

#         current_date = timezone.now().date()
#         coupon_percent = 0


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break


#             coupon_amount = (sum_total * coupon_percent)/100
#             sum_total = sum_total - coupon_amount

#         else:

#             sum_total = sum_total

#         float_total = format(sum_total, '0.2f')
#         return float_total


#     def get_coupon(self,instance):

#         current_date = timezone.now().date()
#         coupon_percent = 0


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break

#         else:
#             coupon_percent = 0


#         coupon_percentage = str(coupon_percent)+" %"

#         return coupon_percentage


#     def get_point(self,instance):
#         sum_total = 0
#         try:
#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",product_status="None",delivery_removed=False)

#         except:
#             order_details = None
#         if order_details is not None:

#             order_prices = order_details.values_list('product_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
           
#             for i in range(len(order_quantity)):
#                 try:
#                     product_point = ProductPoint.objects.filter(product_id=order_prices[i]).last()
#                 except:
#                     product_point = None

#                 if product_point is not None:
#                     p_point = product_point.point
#                     current_date = timezone.now().date()

#                     start_date = current_date
#                     end_date = current_date

#                     if product_point.start_date:
#                         start_date = product_point.start_date
#                     else:
#                         start_date = current_date

#                     if product_point.end_date:
#                         end_date = product_point.end_date

#                     else:

#                         end_date = current_date
                   
#                     if (current_date >= start_date) and (current_date <= end_date):
#                         total_point = p_point * order_quantity[i]
#                         sum_total += total_point

#                 else:
#                     sum_total = sum_total


#         else:
#             sum_total = 0
               

#         float_total = format(sum_total, '0.2f')
#         return float_total


#     def order_details(self,instance):
#         details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,product_status="None",admin_status="Approved",delivery_removed=False).order_by('date_added').values()
#         list_result = [entry for entry in details]
#         for i in range(len(list_result)):
#             product_id = list_result[i]['product_id']
#             try:
#                 product_images = ProductImage.objects.filter(product_id = product_id)
#             except:
#                 product_images = None

#             images= []

#             if product_images:
#                 images= list(product_images.values_list('image_url',flat=True).distinct())

#             list_result[i]['product_images'] = images

       

#         return list_result


#     def all_order_details(self,instance):
#         details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,delivery_removed=False).order_by('date_added').values()
#         list_result = [entry for entry in details]
#         for i in range(len(list_result)):
#             product_id = list_result[i]['product_id']
#             try:
#                 product_images = ProductImage.objects.filter(product_id = product_id)
#             except:
#                 product_images = None

#             images= []

#             if product_images:
#                 images= list(product_images.values_list('image_url',flat=True).distinct())

#             list_result[i]['product_images'] = images

       

#         return list_result


#     def get_invoice_id(self,instance):

#         try:

#             invoice = Invoice.objects.filter(order_id=instance.id).last()

#         except:

#             invoice = None 

#         if invoice:

#             if invoice.id:

#                 invoice_id = invoice.id

#             else:

#                 invoice_id = 0 

#         else:

#             invoice_id = 0 


#         return invoice_id



# class OrderInvoiceSerializer1(serializers.ModelSerializer):
#     price_total = serializers.SerializerMethodField(method_name='get_price')
#     point_total = serializers.SerializerMethodField(method_name='get_point')
#     orders = serializers.SerializerMethodField(method_name='order_details')
#     #orders = serializers.SerializerMethodField(method_name='order_details')
#     coupon_percentage = serializers.SerializerMethodField(method_name='get_coupon')
#     #product = serializers.SerializerMethodField(method_name='get_coupon')
#     invoice_id = serializers.SerializerMethodField(method_name='get_invoice_id')
#     reference_id = serializers.SerializerMethodField(method_name='get_reference')
#     discount = serializers.SerializerMethodField(method_name='get_discount')
#     sub_price = serializers.SerializerMethodField(method_name='get_sub_price')
#     coupon_discount = serializers.SerializerMethodField(method_name='get_coupon_discount')
#     overall_discount = serializers.SerializerMethodField(method_name='get_overall_discount')
#     all_orders = serializers.SerializerMethodField(method_name='all_order_details')

   
#     class Meta:
#         model = Order
#         #fields ='__all__'
#         fields = ('id','date_created','order_status','delivery_status','admin_status','user_id','non_verified_user_id','ip_address','checkout_status','sub_price','discount','coupon_discount','overall_discount','price_total','coupon_code','coupon_percentage','point_total','ordered_date','invoice_id','reference_id','orders','all_orders')

#     # def get_discount(self,instance):

#     #     pass



#     def get_reference(self,instance):

#         try:

#             invoice = Invoice.objects.filter(order_id=instance.id).last()

#         except:

#             invoice = None 

#         if invoice:

#             if invoice.ref_invoice:

#                 invoice_id = invoice.ref_invoice

#             else:

#                 invoice_id = 0 

#         else:

#             invoice_id = 0 


#         return invoice_id


#     #This method is to calculate the total price
#     def get_sub_price(self,instance):
#         sum_total = 0
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",delivery_removed=False,product_status="None")
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 # try:

#                 #     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 # except:
#                 #     product_discount = None
               

#                 if product_price:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 # if product_discount is not None:

#                 #     if product_discount.discount_type == "amount":

#                 #         print()

#                 #         if product_discount.amount:
#                 #             p_discount = product_discount.amount
#                 #         else:
#                 #             p_discount = 0

                   
#                 #         current_date = timezone.now().date()
#                 #         start_date = current_date
#                 #         end_date = current_date
                       

#                 #         if product_discount.start_date:
#                 #             start_date = product_discount.start_date
#                 #         else:
#                 #             start_date = current_date

#                 #         if product_discount.end_date:
#                 #             end_date = product_discount.end_date

#                 #         else:

#                 #             end_date = current_date


#                 #         if (current_date >= start_date) and (current_date <= end_date):
#                 #             total_discount = p_discount * order_quantity[i]
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price

#                 #         else:

#                 #             total_discount = 0
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price


#                 #     elif product_discount.discount_type == "percentage":

#                 #         if product_discount.amount:
#                 #             p_discount = product_discount.amount
#                 #             p_discount = (p_discount * p_price)/100
#                 #         else:
#                 #             p_discount = 0

                   
#                 #         current_date = timezone.now().date()
#                 #         start_date = current_date
#                 #         end_date = current_date
                       

#                 #         if product_discount.start_date:
#                 #             start_date = product_discount.start_date
#                 #         else:
#                 #             start_date = current_date

#                 #         if product_discount.end_date:
#                 #             end_date = product_discount.end_date

#                 #         else:

#                 #             end_date = current_date


#                 #         if (current_date >= start_date) and (current_date <= end_date):
#                 #             total_discount = p_discount * order_quantity[i]
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price

#                 #         else:

#                 #             total_discount = 0
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price

#                 #     else:

#                 #         total_price = (p_price * order_quantity[i])
#                 #         sum_total += total_price


#                 # else:

                   
#                 total_price = (p_price * order_quantity[i])
#                 sum_total += total_price


#                 print("sum total")


#                 print(sum_total)

#         else:
#             sum_total = 0

#         # current_date = timezone.now().date()
#         # coupon_percent = 0


#         float_total = format(sum_total, '0.2f')
#         return float_total




#         # try:
#         #     order = Order.objects.get(pk=instance.id)

#         # except:
#         #     order = None

#         # if order:

#         #     coupon_code = order.coupon_code

#         #     coupons = Cupons.objects.all()
#         #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#         #     coupon_amounts = list(coupons.values_list('amount',flat=True))
#         #     coupon_start = list(coupons.values_list('start_from',flat=True))
#         #     coupon_end = list(coupons.values_list('valid_to',flat=True))
#         #     coupon_validity = list(coupons.values_list('is_active',flat=True))

#         #     for i in range(len(coupon_codes)):
#         #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#         #             coupon_percent = coupon_amounts[i]
#         #             break


#         #     coupon_amount = (sum_total * coupon_percent)/100
#         #     sum_total = sum_total - coupon_amount

#         # else:

#         #     sum_total = sum_total



#         #This method is to calculate the total price
#     def get_discount(self,instance):
#         sum_total = 0
#         discount_total = 0 
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",delivery_removed=False,product_status="None")
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

#                         print()

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount


#                     elif product_discount.discount_type == "percentage":

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount

#                     else:

#                         total_price = (p_price * order_quantity[i])
#                         # sum_total += total_price
#                         discount_total += 0 


#                 else:

                   
#                     # total_price = (p_price * order_quantity[i])
#                     #sum_total += total_discount
#                     discount_total += 0 


#                 print("sum total")


#                 # print(sum_total)

#         else:
#             discount_total = 0

#         # current_date = timezone.now().date()
#         # coupon_percent = 0


#         # try:
#         #     order = Order.objects.get(pk=instance.id)

#         # except:
#         #     order = None

#         # if order:

#         #     coupon_code = order.coupon_code

#         #     coupons = Cupons.objects.all()
#         #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#         #     coupon_amounts = list(coupons.values_list('amount',flat=True))
#         #     coupon_start = list(coupons.values_list('start_from',flat=True))
#         #     coupon_end = list(coupons.values_list('valid_to',flat=True))
#         #     coupon_validity = list(coupons.values_list('is_active',flat=True))

#         #     for i in range(len(coupon_codes)):
#         #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#         #             coupon_percent = coupon_amounts[i]
#         #             break


#         #     coupon_amount = (sum_total * coupon_percent)/100
#         #     sum_total = sum_total - coupon_amount

#         # else:

#         #     sum_total = sum_total

#         float_total = format(discount_total, '0.2f')
#         return float_total



#         #This method is to calculate the total price
#     def get_coupon_discount(self,instance):
#         sum_total = 0
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",delivery_removed=False,product_status="None")
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

#                         print()

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price


#                     elif product_discount.discount_type == "percentage":

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                     else:

#                         total_price = (p_price * order_quantity[i])
#                         sum_total += total_price


#                 else:

                   
#                     total_price = (p_price * order_quantity[i])
#                     sum_total += total_price


#                 print("sum total")


#                 print(sum_total)

#         else:
#             sum_total = 0

#         current_date = timezone.now().date()
#         coupon_percent = 0
#         coupon_amount = 0 


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break


#             coupon_amount = (sum_total * coupon_percent)/100
#             #sum_total = sum_total - coupon_amount
#             # sum_total = coupon_amount

#         else:

#             sum_total = sum_total
#             coupon_amount = 0 

#         float_total = format(coupon_amount, '0.2f')
#         return float_total



#     def get_overall_discount(self,instance):
#         sum_total = 0
#         discount_total = 0
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",delivery_removed=False,product_status="None")
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             discount_total = 0 
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

#                         print()

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount


#                     elif product_discount.discount_type == "percentage":

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount

#                     else:

#                         total_price = (p_price * order_quantity[i])
#                         sum_total += total_price
#                         discount_total += total_discount


#                 else:

                   
#                     total_price = (p_price * order_quantity[i])
#                     sum_total += total_price
#                     total_discount = 0 
#                     discount_total += total_discount


#                 print("sum total")


#                 print(sum_total)

#         else:
#             discount_total = 0
#             sum_total = 0

#         current_date = timezone.now().date()
#         coupon_percent = 0
#         coupon_amount = 0
#         coupon_total = 0 


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break


#             coupon_amount = (sum_total * coupon_percent)/100
#             #sum_total = sum_total - coupon_amount
#             # sum_total = coupon_amount

#         else:

#             sum_total = sum_total
#             coupon_amount = 0 

#         total = coupon_amount + discount_total

#         float_total = format(total, '0.2f')
#         return float_total











#     #This method is to calculate the total price
#     def get_price(self,instance):
#         sum_total = 0
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",delivery_removed=False,product_status="None")
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

#                         print()

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price


#                     elif product_discount.discount_type == "percentage":

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                     else:

#                         total_price = (p_price * order_quantity[i])
#                         sum_total += total_price


#                 else:

                   
#                     total_price = (p_price * order_quantity[i])
#                     sum_total += total_price


#                 print("sum total")


#                 print(sum_total)

#         else:
#             sum_total = 0

#         current_date = timezone.now().date()
#         coupon_percent = 0


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break


#             coupon_amount = (sum_total * coupon_percent)/100
#             sum_total = sum_total - coupon_amount

#         else:

#             sum_total = sum_total

#         float_total = format(sum_total, '0.2f')
#         return float_total


#     def get_coupon(self,instance):

#         current_date = timezone.now().date()
#         coupon_percent = 0


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break

#         else:
#             coupon_percent = 0


#         coupon_percentage = str(coupon_percent)+" %"

#         return coupon_percentage


#     def get_point(self,instance):
#         sum_total = 0
#         try:
#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status="Approved",delivery_removed=False,product_status="None")

#         except:
#             order_details = None
#         if order_details is not None:

#             order_prices = order_details.values_list('product_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
           
#             for i in range(len(order_quantity)):
#                 try:
#                     product_point = ProductPoint.objects.filter(product_id=order_prices[i]).last()
#                 except:
#                     product_point = None

#                 if product_point is not None:
#                     p_point = product_point.point
#                     current_date = timezone.now().date()

#                     start_date = current_date
#                     end_date = current_date

#                     if product_point.start_date:
#                         start_date = product_point.start_date
#                     else:
#                         start_date = current_date

#                     if product_point.end_date:
#                         end_date = product_point.end_date

#                     else:

#                         end_date = current_date
                   
#                     if (current_date >= start_date) and (current_date <= end_date):
#                         total_point = p_point * order_quantity[i]
#                         sum_total += total_point

#                 else:
#                     sum_total = sum_total


#         else:
#             sum_total = 0
               

#         float_total = format(sum_total, '0.2f')
#         return float_total


#     def order_details(self,instance):
#         details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,admin_status="Approved",delivery_removed=False,product_status="None").order_by('date_added').values()
#         list_result = [entry for entry in details]
#         for i in range(len(list_result)):
#             product_id = list_result[i]['product_id']
#             try:
#                 product_images = ProductImage.objects.filter(product_id = product_id)
#             except:
#                 product_images = None

#             images= []

#             if product_images:
#                 images= list(product_images.values_list('image_url',flat=True).distinct())

#             list_result[i]['product_images'] = images

       

#         return list_result


#     def all_order_details(self,instance):
#         details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,delivery_removed=False).order_by('date_added').values()
#         list_result = [entry for entry in details]
#         for i in range(len(list_result)):
#             product_id = list_result[i]['product_id']
#             try:
#                 product_images = ProductImage.objects.filter(product_id = product_id)
#             except:
#                 product_images = None

#             images= []

#             if product_images:
#                 images= list(product_images.values_list('image_url',flat=True).distinct())

#             list_result[i]['product_images'] = images

       

#         return list_result


#     def get_invoice_id(self,instance):

#         try:

#             invoice = Invoice.objects.filter(order_id=instance.id).last()

#         except:

#             invoice = None 

#         if invoice:

#             if invoice.id:

#                 invoice_id = invoice.id

#             else:

#                 invoice_id = 0 

#         else:

#             invoice_id = 0 


#         return invoice_id
           
           
class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    price_total = serializers.SerializerMethodField(method_name='get_price')
    point_total = serializers.SerializerMethodField(method_name='get_point')
    orders = serializers.SerializerMethodField(method_name='order_details')
    #orders = serializers.SerializerMethodField(method_name='order_details')
    coupon_percentage = serializers.SerializerMethodField(method_name='get_coupon')
    #product = serializers.SerializerMethodField(method_name='get_coupon')
    invoice_id = serializers.SerializerMethodField(method_name='get_invoice_id')
    reference_id = serializers.SerializerMethodField(method_name='get_reference')
    discount = serializers.SerializerMethodField(method_name='get_discount')
    sub_price = serializers.SerializerMethodField(method_name='get_price')
    coupon_discount = serializers.SerializerMethodField(method_name='get_coupon_discount')
    overall_discount = serializers.SerializerMethodField(method_name='get_overall_discount')

   
    class Meta:
        model = Order
        #fields ='__all__'
        fields = ('id','date_created','order_status','delivery_status','admin_status','user_id','non_verified_user_id','ip_address','checkout_status','sub_price','discount','coupon_discount','overall_discount','price_total','coupon_code','coupon_percentage','point_total','ordered_date','invoice_id','reference_id','orders')

    # def get_discount(self,instance):

    #     pass



    def get_reference(self,instance):

        try:

            invoice = Invoice.objects.filter(order_id=instance.id).last()

        except:

            invoice = None 

        if invoice:

            if invoice.ref_invoice:

                invoice_id = invoice.ref_invoice

            else:

                invoice_id = 0 

        else:

            invoice_id = 0 


        return invoice_id


    # #This method is to calculate the total price
    # def get_sub_price(self,instance):
    #     sum_total = 0
    #     try:

    #         order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,product_status="None")
    #     except:
    #         order_details = None

    #     if order_details is not None:

    #         order_prices = order_details.values_list('specification_id',flat = True)
    #         order_quantity = order_details.values_list('total_quantity',flat = True)
    #         sum_total= 0
    #         p_price = 0
       
    #         for i in range(len(order_quantity)):
    #             try:
    #                 product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
    #             except:
    #                 product_price = None

    #             print(product_price)
    #             # try:

    #             #     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

    #             # except:
    #             #     product_discount = None
               

    #             if product_price:
    #                 p_price = product_price.price

    #             else:
    #                 p_price = 0

               

         
    #             # if product_discount is not None:

    #             #     if product_discount.discount_type == "amount":

    #             #         print()

    #             #         if product_discount.amount:
    #             #             p_discount = product_discount.amount
    #             #         else:
    #             #             p_discount = 0

                   
    #             #         current_date = timezone.now().date()
    #             #         start_date = current_date
    #             #         end_date = current_date
                       

    #             #         if product_discount.start_date:
    #             #             start_date = product_discount.start_date
    #             #         else:
    #             #             start_date = current_date

    #             #         if product_discount.end_date:
    #             #             end_date = product_discount.end_date

    #             #         else:

    #             #             end_date = current_date


    #             #         if (current_date >= start_date) and (current_date <= end_date):
    #             #             total_discount = p_discount * order_quantity[i]
    #             #             total_price = (p_price * order_quantity[i]) - total_discount
    #             #             sum_total += total_price

    #             #         else:

    #             #             total_discount = 0
    #             #             total_price = (p_price * order_quantity[i]) - total_discount
    #             #             sum_total += total_price


    #             #     elif product_discount.discount_type == "percentage":

    #             #         if product_discount.amount:
    #             #             p_discount = product_discount.amount
    #             #             p_discount = (p_discount * p_price)/100
    #             #         else:
    #             #             p_discount = 0

                   
    #             #         current_date = timezone.now().date()
    #             #         start_date = current_date
    #             #         end_date = current_date
                       

    #             #         if product_discount.start_date:
    #             #             start_date = product_discount.start_date
    #             #         else:
    #             #             start_date = current_date

    #             #         if product_discount.end_date:
    #             #             end_date = product_discount.end_date

    #             #         else:

    #             #             end_date = current_date


    #             #         if (current_date >= start_date) and (current_date <= end_date):
    #             #             total_discount = p_discount * order_quantity[i]
    #             #             total_price = (p_price * order_quantity[i]) - total_discount
    #             #             sum_total += total_price

    #             #         else:

    #             #             total_discount = 0
    #             #             total_price = (p_price * order_quantity[i]) - total_discount
    #             #             sum_total += total_price

    #             #     else:

    #             #         total_price = (p_price * order_quantity[i])
    #             #         sum_total += total_price


    #             # else:

                   
    #             total_price = (p_price * order_quantity[i])
    #             sum_total += total_price


    #             print("sum total")


    #             print(sum_total)

    #     else:
    #         sum_total = 0

    #     # current_date = timezone.now().date()
    #     # coupon_percent = 0


    #     float_total = format(sum_total, '0.2f')
    #     return float_total




        # try:
        #     order = Order.objects.get(pk=instance.id)

        # except:
        #     order = None

        # if order:

        #     coupon_code = order.coupon_code

        #     coupons = Cupons.objects.all()
        #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
        #     coupon_amounts = list(coupons.values_list('amount',flat=True))
        #     coupon_start = list(coupons.values_list('start_from',flat=True))
        #     coupon_end = list(coupons.values_list('valid_to',flat=True))
        #     coupon_validity = list(coupons.values_list('is_active',flat=True))

        #     for i in range(len(coupon_codes)):
        #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
        #             coupon_percent = coupon_amounts[i]
        #             break


        #     coupon_amount = (sum_total * coupon_percent)/100
        #     sum_total = sum_total - coupon_amount

        # else:

        #     sum_total = sum_total



        #This method is to calculate the total price
    def get_discount(self,instance):
        sum_total = 0
        discount_total = 0 
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,product_status="None")
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        print()

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount


                    elif product_discount.discount_type == "percentage":

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount

                    else:

                        total_price = (p_price * order_quantity[i])
                        # sum_total += total_price
                        discount_total += 0 


                else:

                   
                    # total_price = (p_price * order_quantity[i])
                    #sum_total += total_discount
                    discount_total += 0 


                print("sum total")


                # print(sum_total)

        else:
            discount_total = 0

        # current_date = timezone.now().date()
        # coupon_percent = 0


        # try:
        #     order = Order.objects.get(pk=instance.id)

        # except:
        #     order = None

        # if order:

        #     coupon_code = order.coupon_code

        #     coupons = Cupons.objects.all()
        #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
        #     coupon_amounts = list(coupons.values_list('amount',flat=True))
        #     coupon_start = list(coupons.values_list('start_from',flat=True))
        #     coupon_end = list(coupons.values_list('valid_to',flat=True))
        #     coupon_validity = list(coupons.values_list('is_active',flat=True))

        #     for i in range(len(coupon_codes)):
        #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
        #             coupon_percent = coupon_amounts[i]
        #             break


        #     coupon_amount = (sum_total * coupon_percent)/100
        #     sum_total = sum_total - coupon_amount

        # else:

        #     sum_total = sum_total

        float_total = format(discount_total, '0.2f')
        return float_total



        #This method is to calculate the total price
    def get_coupon_discount(self,instance):
        sum_total = 0
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,product_status="None")
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        print()

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price


                    elif product_discount.discount_type == "percentage":

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                    else:

                        total_price = (p_price * order_quantity[i])
                        sum_total += total_price


                else:

                   
                    total_price = (p_price * order_quantity[i])
                    sum_total += total_price


                print("sum total")


                print(sum_total)

        else:
            sum_total = 0

        current_date = timezone.now().date()
        coupon_percent = 0
        coupon_amount = 0 


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break


            coupon_amount = (sum_total * coupon_percent)/100
            #sum_total = sum_total - coupon_amount
            # sum_total = coupon_amount

        else:

            sum_total = sum_total
            coupon_amount = 0 

        float_total = format(coupon_amount, '0.2f')
        return float_total



    def get_overall_discount(self,instance):
        sum_total = 0
        discount_total = 0
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,product_status="None")
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            discount_total = 0 
            p_price = 0
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        print()

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount


                    elif product_discount.discount_type == "percentage":

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount

                    else:

                        total_price = (p_price * order_quantity[i])
                        sum_total += total_price
                        discount_total += total_discount


                else:

                   
                    total_price = (p_price * order_quantity[i])
                    sum_total += total_price
                    total_discount = 0 
                    discount_total += total_discount


                print("sum total")


                print(sum_total)

        else:
            discount_total = 0
            sum_total = 0

        current_date = timezone.now().date()
        coupon_percent = 0
        coupon_amount = 0
        coupon_total = 0 


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break


            coupon_amount = (sum_total * coupon_percent)/100
            #sum_total = sum_total - coupon_amount
            # sum_total = coupon_amount

        else:

            sum_total = sum_total
            coupon_amount = 0 

        total = coupon_amount + discount_total

        float_total = format(total, '0.2f')
        return float_total











    #This method is to calculate the total price
    # def get_price(self,instance):
    #     sum_total = 0
    #     try:

    #         order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,product_status="None")
    #     except:
    #         order_details = None


    #     print("order_detailssssssssssss")
    #     print(order_details)

    #     if order_details is not None:

    #         order_prices = order_details.values_list('specification_id',flat = True)
    #         order_quantity = order_details.values_list('total_quantity',flat = True)
    #         sum_total= 0
    #         p_price = 0
       
    #         for i in range(len(order_quantity)):
    #             try:
    #                 product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
    #             except:
    #                 product_price = None

    #             print(product_price)
    #             try:

    #                 product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

    #             except:
    #                 product_discount = None
               

    #             if product_price is not None:
    #                 p_price = product_price.price

    #             else:
    #                 p_price = 0

               

         
    #             if product_discount is not None:

    #                 if product_discount.discount_type == "amount":

    #                     print()

    #                     if product_discount.amount:
    #                         p_discount = product_discount.amount
    #                     else:
    #                         p_discount = 0

                   
    #                     current_date = timezone.now().date()
    #                     start_date = current_date
    #                     end_date = current_date
                       

    #                     if product_discount.start_date:
    #                         start_date = product_discount.start_date
    #                     else:
    #                         start_date = current_date

    #                     if product_discount.end_date:
    #                         end_date = product_discount.end_date

    #                     else:

    #                         end_date = current_date


    #                     if (current_date >= start_date) and (current_date <= end_date):
    #                         total_discount = p_discount * order_quantity[i]
    #                         total_price = (p_price * order_quantity[i]) - total_discount
    #                         sum_total += total_price

    #                     else:

    #                         total_discount = 0
    #                         total_price = (p_price * order_quantity[i]) - total_discount
    #                         sum_total += total_price


    #                 elif product_discount.discount_type == "percentage":

    #                     if product_discount.amount:
    #                         p_discount = product_discount.amount
    #                         p_discount = (p_discount * p_price)/100
    #                     else:
    #                         p_discount = 0

                   
    #                     current_date = timezone.now().date()
    #                     start_date = current_date
    #                     end_date = current_date
                       

    #                     if product_discount.start_date:
    #                         start_date = product_discount.start_date
    #                     else:
    #                         start_date = current_date

    #                     if product_discount.end_date:
    #                         end_date = product_discount.end_date

    #                     else:

    #                         end_date = current_date


    #                     if (current_date >= start_date) and (current_date <= end_date):
    #                         total_discount = p_discount * order_quantity[i]
    #                         total_price = (p_price * order_quantity[i]) - total_discount
    #                         sum_total += total_price

    #                     else:

    #                         total_discount = 0
    #                         total_price = (p_price * order_quantity[i]) - total_discount
    #                         sum_total += total_price

    #                 else:

    #                     total_price = (p_price * order_quantity[i])
    #                     sum_total += total_price


    #             else:

                   
    #                 total_price = (p_price * order_quantity[i])
    #                 sum_total += total_price


    #             print("sum total")


    #             print(sum_total)

    #     else:
    #         sum_total = 0

    #     current_date = timezone.now().date()
    #     coupon_percent = 0


    #     try:
    #         order = Order.objects.get(pk=instance.id)

    #     except:
    #         order = None

    #     if order:

    #         coupon_code = order.coupon_code

    #         coupons = Cupons.objects.all()
    #         coupon_codes = list(coupons.values_list('cupon_code',flat=True))
    #         coupon_amounts = list(coupons.values_list('amount',flat=True))
    #         coupon_start = list(coupons.values_list('start_from',flat=True))
    #         coupon_end = list(coupons.values_list('valid_to',flat=True))
    #         coupon_validity = list(coupons.values_list('is_active',flat=True))

    #         for i in range(len(coupon_codes)):
    #             if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
    #                 coupon_percent = coupon_amounts[i]
    #                 break


    #         coupon_amount = (sum_total * coupon_percent)/100
    #         sum_total = sum_total - coupon_amount

    #     else:

    #         sum_total = sum_total

    #     float_total = format(sum_total, '0.2f')
    #     return float_total


    def get_coupon(self,instance):

        current_date = timezone.now().date()
        coupon_percent = 0


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break

        else:
            coupon_percent = 0


        coupon_percentage = str(coupon_percent)+" %"

        return coupon_percentage


    def get_point(self,instance):
        sum_total = 0
        try:
            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,product_status="None")

        except:
            order_details = None
        if order_details is not None:

            order_prices = order_details.values_list('product_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
           
            for i in range(len(order_quantity)):
                try:
                    product_point = ProductPoint.objects.filter(product_id=order_prices[i]).last()
                except:
                    product_point = None

                if product_point is not None:
                    p_point = product_point.point
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
                        total_point = p_point * order_quantity[i]
                        sum_total += total_point

                else:
                    sum_total = sum_total


        else:
            sum_total = 0
               

        float_total = format(sum_total, '0.2f')
        return float_total


    def order_details(self,instance):
        details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).order_by('date_added').values()
        list_result = [entry for entry in details]
        for i in range(len(list_result)):
            product_id = list_result[i]['product_id']
            try:
                product_images = ProductImage.objects.filter(product_id = product_id)
            except:
                product_images = None

            images= []

            if product_images:
                images= list(product_images.values_list('image_url',flat=True).distinct())

            list_result[i]['product_images'] = images

       

        return list_result


    def get_invoice_id(self,instance):

        try:

            invoice = Invoice.objects.filter(order_id=instance.id).last()

        except:

            invoice = None 

        if invoice:

            if invoice.id:

                invoice_id = invoice.id

            else:

                invoice_id = 0 

        else:

            invoice_id = 0 


        return invoice_id



    def get_price(self,instance):

        sum_total = 0
        try:
            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,product_status="None")

        except:
            order_details = None

        if order_details:

            order_ids = list(order_details.values_list('id',flat=True))

            total_price_list = list(order_details.values_list('total_price',flat=True))

            sum_total = sum(total_price_list)


        float_total = format(sum_total, '0.2f')
        return float_total

            # if int(len(order_ids)) > 0:

            #     for i in range(len(order_ids)):












class OrderDetailsSerializer(serializers.ModelSerializer):
    #price = serializers.SerializerMethodField(method_name='get_price')
    #points = serializers.SerializerMethodField(method_name='get_point')
    class Meta:
        model = OrderDetails
        fields = ('id','order_id','product_id','quantity','total_quantity','date_added','is_removed','delivery_removed','unit_price','total_price','unit_point','total_point','product_name','product_color','product_size','remaining','admin_status','product_status','specification_id')

    
   
    #This method is to calculate the price of the individual items
    def get_price(self,instance):
        product_price = ProductPrice.objects.filter(product_id=instance.product_id).last()
        p_price = product_price.price
     

        total_price = p_price * instance.total_quantity
        float_total = format(total_price, '0.2f')
        return float_total

    def get_point(self,instance):
        product_point = ProductPoint.objects.filter(product_id=instance.product_id).last()
        p_point = product_point.point
        start_date = product_point.start_date
        end_date = product_point.end_date
        current_date = timezone.now().date()
        if (current_date >= start_date) and (current_date <= end_date):
            total_point = p_point * instance.total_quantity

        else:
            total_point = 0
     
        float_total = format(total_point, '0.2f')
        return float_total





class OrderDetailsSerializer1(serializers.ModelSerializer):
    #price = serializers.SerializerMethodField(method_name='get_price')
    #points = serializers.SerializerMethodField(method_name='get_point')
    images = serializers.SerializerMethodField(method_name='get_images')
    class Meta:
        model = OrderDetails
        fields = ('id','order_id','product_id','quantity','total_quantity','date_added','is_removed','delivery_removed','unit_price','total_price','unit_point','total_point','product_name','product_color','product_size','remaining','admin_status','product_status','specification_id','images')
   
    #This method is to calculate the price of the individual items
    def get_price(self,instance):
        product_price = ProductPrice.objects.filter(product_id=instance.product_id).last()
        p_price = product_price.price
     

        total_price = p_price * instance.total_quantity
        float_total = format(total_price, '0.2f')
        return float_total

    def get_point(self,instance):
        product_point = ProductPoint.objects.filter(product_id=instance.product_id).last()
        p_point = product_point.point
        start_date = product_point.start_date
        end_date = product_point.end_date
        current_date = timezone.now().date()
        if (current_date >= start_date) and (current_date <= end_date):
            total_point = p_point * instance.total_quantity

        else:
            total_point = 0
     
        float_total = format(total_point, '0.2f')
        return float_total



    def get_images(self,instance):

        images=[]


        try:

            product_images = ProductImage.objects.filter(product_id = instance.product_id)

        except:
            product_images = None

        if product_images is not None:
            images = list(product_images.values_list('image_url' , flat = True))
            # images=[] 
            # for i in range(len(image_ids)):
            #     images += product_images.image


        else:
            images=[]

        return images


 



class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ('id','product_id','price','date_added','currency_id')


class ProductPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPoint
        fields = ('id','product_id','point','start_date','end_date')
   



class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields="__all__"


class UserzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userz
        fields="__all__"


class ProductSpecificationSerializer(serializers.ModelSerializer):
    #hexcolor = serializers.SerializerMethodField(method_name='get_color')
    class Meta:
        model = ProductSpecification
        fields = ('id','product_id','color','size','unit','weight')

    # def get_color(self,instance):
    #     product_color = ProductSpecification.objects.filter(id = instance.id).last()
    #     color = product_color.color
    #     colorhex = Color(color).hex
 
    #     return colorhex



class OrderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields="__all__"


# class InvoiceSerializer(serializers.ModelSerializer):
#     date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d") 
#     time = serializers.DateTimeField(read_only=True, format="%H:%M:%S") 
#     class Meta:
#         model = Invoice
#         fields=("id","order_id","date" , "time")


class InvoiceSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d") 
    time = serializers.DateTimeField(read_only=True, format="%H:%M:%S")
    child_invoice = serializers.SerializerMethodField(method_name='get_child') 
    class Meta:
        model = Invoice
        fields= ('id','order_id','date','time','ref_invoice','is_active','child_invoice')

    def get_child(self,instance):

        if instance.ref_invoice == 0:

            print("this is a mother invoice")

            try:
                invoices = Invoice.objects.all()
            except:
                invoices = None 

            if invoices:
                invoice_ids = list(invoices.values_list('id',flat=True))
                ref_ids = list(invoices.values_list('ref_invoice',flat=True))
                print("invoice_lengths")
                print(len(invoice_ids))
                print(len(ref_ids))
                print("lengthhh")
                print(instance.id)
                print(invoice_ids)
                print(ref_ids)

                for i in range(len(ref_ids)):

                    if instance.id == ref_ids[i]:

                        child = invoice_ids[i]
                        break
                    else:
                        child = 0

            else:
                child = 0 

        else:

            child = 0 


        return child 


class PoSInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields="__all__"




class SalesSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField(method_name='get_brand')
    warehouse_name = serializers.SerializerMethodField(method_name='get_warehouse')
    shop_name = serializers.SerializerMethodField(method_name='get_shop')
    discount = serializers.SerializerMethodField(method_name="get_discount")
    purchase_price= serializers.SerializerMethodField(method_name="get_purchase_price")
    vat= serializers.SerializerMethodField(method_name="get_vat")
    profit= serializers.SerializerMethodField(method_name="get_profit")
    loss= serializers.SerializerMethodField(method_name="get_loss")
    net_sale= serializers.SerializerMethodField(method_name="get_net_sale")
    date_added = serializers.DateTimeField(read_only=True, format="%d-%m-%Y")
    #total_price= serializers.SerializerMethodField(method_name="get_price")
   

    class Meta:
        model= OrderDetails
        fields = ('id','order_id','product_id',"vat","shop_name", "purchase_price","brand","profit","loss","net_sale",'quantity', "discount", "warehouse_name",'total_quantity','date_added','is_removed','unit_price','total_price','unit_point','total_point','product_name','product_color','product_size','remaining','admin_status' )
   


        def get_price(self,instance):
            product_price = ProductPrice.objects.filter(specification_id=instance.specification_id).last()
            p_price = product_price.price


            total_price = p_price * instance.total_quantity
            float_total = format(total_price, '0.2f')
            float_value= float(float_total)
            return float_value

         



    # def get_purchase_price(self,instance):

    #     product_price = ProductPrice.objects.filter(specification_id=instance.specification_id)
   
    #     p_price = product_price.purchase_price


    #     total_purchase_price = p_price * instance.total_quantity
    #     float_total = format(total_purchase_price, '0.2f')
    #     return float_total


    def get_purchase_price(self,instance):

        old_price = 0


        try:


            p_price = ProductPrice.objects.filter(specification_id = instance.specification_id).last()

        except:

            p_price = None


        if p_price:

            old_price =p_price.purchase_price

        else:
            old_price = 0


        total_price = old_price * instance.total_quantity
        float_total = format(total_price, '0.2f')
        float_value= float(float_total)
        return float_value


    def get_brand(self,instance):

        brand = ""

        try:

            product_brand = Product.objects.get(id=instance.id)
        except:

            product_brand = None

           
        if product_brand:

            brand = product_brand.brand


        return brand






    def get_warehouse(self , instance):

        warehouse=""

        try:
            warehouse_name = Warehouse.objects.get(id=instance.id)

        except:
            warehouse_name = None

        if warehouse_name:
            if warehouse_name.warehouse_name:
                warehouse = warehouse_name.warehouse_name

            else:
                warehouse = "N/A"
        else:
            warehouse = "N/A"
        return warehouse



    def get_shop(self , instance):

            shop=""

            try:
                shop_name = Shop.objects.get(id=instance.id)

            except:
                shop_name = None

            if shop_name:
                if shop_name.shop_name:
                    warehouse = shop_name.shop_name

                else:
                    shop = "N/A"
            else:
                shop = "N/A"
            return shop

    def get_discount (self,instance):

        old_price = 0


        try:


            v_price = discount_product.objects.filter(specification_id=instance.specification_id).last()

        except:

            v_price = None


        if v_price:

            old_price =v_price.amount

        else:
            old_price = 0

        total_price = old_price * instance.total_quantity
        float_total = format(total_price, '0.2f')
        float_value= float(float_total)
        return float_value


    def get_vat(self,instance):

        old_price = 0


        try:


            v_price = ProductSpecification.objects.filter(id=instance.id).last()

        except:

            v_price = None


        if v_price:

            if v_price.vat:

                old_price =v_price.vat

            else:
                old_price = 0

        else:
            old_price = 0


        float_total = format(old_price, '0.2f')
        float_value= float(float_total)
        return float_value




    def get_profit(self, instance):


        try:

            product_price = ProductPrice.objects.filter(specification_id=instance.specification_id).last()

        except:
            product_price = None

        if product_price:

            selling_price = product_price.price
            purchase_price = product_price.purchase_price

            #total_selling_price = selling_price*instance.total_quantity
            total_purchase_price = purchase_price*instance.total_quantity
           

            if instance.total_price > total_purchase_price:
                profit = instance.total_price- total_purchase_price

            else:
                profit = 0


            total_profit = format(profit, '0.2f')
            float_value= float(total_profit)
            return float_value

        else:

            return 0




    def get_loss(self, instance):


        try:

            product_price = ProductPrice.objects.filter(specification_id=instance.specification_id).last()

        except:
            product_price = None

        if product_price:

            selling_price = product_price.price
            purchase_price = product_price.purchase_price

            #total_selling_price = selling_price*instance.total_quantity
            total_purchase_price = purchase_price*instance.total_quantity
           

            if instance.total_price < total_purchase_price:
                loss = total_purchase_price - instance.total_price

            else:
                loss = 0

            total_loss = format(loss, '0.2f')
            float_value= float(total_loss)
            return float_value

        else:

            return 0





   

    def get_net_sale(self, instance):


        try:

            product_price = ProductPrice.objects.filter(specification_id=instance.specification_id).last()
            v_price = ProductSpecification.objects.filter(id=instance.specification_id).last()

        except:
            product_price = None

        if product_price:

            selling_price = product_price.price

            if v_price.vat:
                vat = v_price.vat

            else:

                vat =0.0

            #total_selling_price = selling_price*instance.total_quantity
            total_vat = vat*instance.total_quantity
           
         
            net_sale = instance.total_price - total_vat

       
            total_sale = format(net_sale, '0.2f')
            float_value= float(total_sale)
            return float_value

        else:

            return 0





class OrderInvoiceSerializer(serializers.ModelSerializer):
    price_total = serializers.SerializerMethodField(method_name='get_price')
    point_total = serializers.SerializerMethodField(method_name='get_point')
    orders = serializers.SerializerMethodField(method_name='order_details')
    all_orders = serializers.SerializerMethodField(method_name='order_detailz')
    #orders = serializers.SerializerMethodField(method_name='order_details')
    coupon_percentage = serializers.SerializerMethodField(method_name='get_coupon')
    #product = serializers.SerializerMethodField(method_name='get_coupon')
    invoice_id = serializers.SerializerMethodField(method_name='get_invoice_id')
    reference_id = serializers.SerializerMethodField(method_name='get_reference')
    phone_number = serializers.SerializerMethodField(method_name='get_phone_number')
    discount = serializers.SerializerMethodField(method_name='get_discount')
    sub_price = serializers.SerializerMethodField(method_name='get_sub_price')
    coupon_discount = serializers.SerializerMethodField(method_name='get_coupon_discount')
    overall_discount = serializers.SerializerMethodField(method_name='get_overall_discount')

   
    class Meta:
        model = Order
        #fields ='__all__'
        fields = ('id','date_created','order_status','delivery_status','admin_status','user_id','non_verified_user_id','ip_address','checkout_status','price_total','coupon_code','coupon_percentage','point_total','ordered_date','invoice_id','orders','all_orders','reference_id','is_seller','phone_number','discount','sub_price','coupon_discount','overall_discount')

    
    def get_phone_number(self,instance):

        phone_number = ""

        try:
            order_info = OrderInfo.objects.get(order_id=instance.id)

        except:
            order_info = None 

        print("order_info")
        print(order_info)

        if order_info:

            if order_info.billing_address_id:
                billing_address_id = order_info.billing_address_id

            else:
                billing_address_id = 0




            try:
                billing_address = BillingAddress.objects.get(id=billing_address_id)
            except:
                billing_address = None 


            print("billingaddress")
            print(billing_address)

            if billing_address:
                if billing_address.phone_number:
                    phone_number = billing_address.phone_number

                else:
                    phone_number = ""

            else:
                phone_number = ""

        else:
            phone_number = ""

        return phone_number
            


    #This method is to calculate the total price
    def get_price(self,instance):
        sum_total = 0
        admin = ["Pending","Approved"]
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,delivery_removed=False,product_status="None",admin_status__in=admin)
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
            print("totalprice")
            print(len(order_quantity))
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        print()

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price


                    elif product_discount.discount_type == "percentage":

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                    else:

                        total_price = (p_price * order_quantity[i])
                        sum_total += total_price


                else:

                   
                    total_price = (p_price * order_quantity[i])
                    sum_total += total_price


                print("sum total")


                print(sum_total)

        else:
            sum_total = 0

        current_date = timezone.now().date()
        coupon_percent = 0


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break


            coupon_amount = (sum_total * coupon_percent)/100
            sum_total = sum_total - coupon_amount

        else:

            sum_total = sum_total

        float_total = format(sum_total, '0.2f')
        return float_total


    def get_coupon(self,instance):

        current_date = timezone.now().date()
        coupon_percent = 0


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break

        else:
            coupon_percent = 0


        coupon_percentage = str(coupon_percent)+" %"

        return coupon_percentage


    def get_point(self,instance):
        sum_total = 0
        admin = ["Pending","Approved"]
        try:
            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,delivery_removed=False,product_status="None",admin_status__in=admin)

        except:
            order_details = None
        if order_details is not None:

            order_prices = order_details.values_list('product_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            print("point_total")
            print(len(order_quantity))
           
            for i in range(len(order_quantity)):
                try:
                    product_point = ProductPoint.objects.filter(product_id=order_prices[i]).last()
                except:
                    product_point = None

                if product_point is not None:
                    p_point = product_point.point
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
                        total_point = p_point * order_quantity[i]
                        sum_total += total_point

                else:
                    sum_total = sum_total


        else:
            sum_total = 0
               

        float_total = format(sum_total, '0.2f')
        return float_total


    def order_details(self,instance):
        details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,delivery_removed=False,product_status="None").order_by('date_added').values()
        list_result = [entry for entry in details]
        for i in range(len(list_result)):
            product_id = list_result[i]['product_id']
            try:
                product_images = ProductImage.objects.filter(product_id = product_id)
            except:
                product_images = None

            images= []

            if product_images:
                images= list(product_images.values_list('image_url',flat=True).distinct())

            list_result[i]['product_images'] = images

       

        return list_result


    def get_invoice_id(self,instance):

        try:

            invoice = Invoice.objects.filter(order_id=instance.id).last()

        except:

            invoice = None 

        if invoice:

            if invoice.id:

                invoice_id = invoice.id

            else:

                invoice_id = 0 

        else:

            invoice_id = 0 


        return invoice_id


    def get_reference(self,instance):

        try:

            invoice = Invoice.objects.filter(order_id=instance.id).last()

        except:

            invoice = None 

        if invoice:

            if invoice.ref_invoice:

                invoice_id = invoice.ref_invoice

            else:

                invoice_id = 0 

        else:

            invoice_id = 0 


        return invoice_id


    def order_detailz(self,instance):
        details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,delivery_removed=False).order_by('date_added').values()
        list_result = [entry for entry in details]
        for i in range(len(list_result)):
            product_id = list_result[i]['product_id']
            try:
                product_images = ProductImage.objects.filter(product_id = product_id)
            except:
                product_images = None

            images= []

            if product_images:
                images= list(product_images.values_list('image_url',flat=True).distinct())

            list_result[i]['product_images'] = images

       

        return list_result


        #This method is to calculate the total price
    def get_sub_price(self,instance):
        sum_total = 0
        admin = ["Pending","Approved"]
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in = admin,product_status="None",delivery_removed=False)
        except:
            order_details = None

        # print("sub price")
        # print(len(order_quantity))

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
            print("sub price")
            print(len(order_quantity))
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                # try:

                #     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                # except:
                #     product_discount = None
               

                if product_price:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                # if product_discount is not None:

                #     if product_discount.discount_type == "amount":

                #         print()

                #         if product_discount.amount:
                #             p_discount = product_discount.amount
                #         else:
                #             p_discount = 0

                   
                #         current_date = timezone.now().date()
                #         start_date = current_date
                #         end_date = current_date
                       

                #         if product_discount.start_date:
                #             start_date = product_discount.start_date
                #         else:
                #             start_date = current_date

                #         if product_discount.end_date:
                #             end_date = product_discount.end_date

                #         else:

                #             end_date = current_date


                #         if (current_date >= start_date) and (current_date <= end_date):
                #             total_discount = p_discount * order_quantity[i]
                #             total_price = (p_price * order_quantity[i]) - total_discount
                #             sum_total += total_price

                #         else:

                #             total_discount = 0
                #             total_price = (p_price * order_quantity[i]) - total_discount
                #             sum_total += total_price


                #     elif product_discount.discount_type == "percentage":

                #         if product_discount.amount:
                #             p_discount = product_discount.amount
                #             p_discount = (p_discount * p_price)/100
                #         else:
                #             p_discount = 0

                   
                #         current_date = timezone.now().date()
                #         start_date = current_date
                #         end_date = current_date
                       

                #         if product_discount.start_date:
                #             start_date = product_discount.start_date
                #         else:
                #             start_date = current_date

                #         if product_discount.end_date:
                #             end_date = product_discount.end_date

                #         else:

                #             end_date = current_date


                #         if (current_date >= start_date) and (current_date <= end_date):
                #             total_discount = p_discount * order_quantity[i]
                #             total_price = (p_price * order_quantity[i]) - total_discount
                #             sum_total += total_price

                #         else:

                #             total_discount = 0
                #             total_price = (p_price * order_quantity[i]) - total_discount
                #             sum_total += total_price

                #     else:

                #         total_price = (p_price * order_quantity[i])
                #         sum_total += total_price


                # else:

                   
                total_price = (p_price * order_quantity[i])
                sum_total += total_price


                print("sum total")


                print(sum_total)

        else:
            sum_total = 0

        # current_date = timezone.now().date()
        # coupon_percent = 0


        float_total = format(sum_total, '0.2f')
        return float_total




        # try:
        #     order = Order.objects.get(pk=instance.id)

        # except:
        #     order = None

        # if order:

        #     coupon_code = order.coupon_code

        #     coupons = Cupons.objects.all()
        #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
        #     coupon_amounts = list(coupons.values_list('amount',flat=True))
        #     coupon_start = list(coupons.values_list('start_from',flat=True))
        #     coupon_end = list(coupons.values_list('valid_to',flat=True))
        #     coupon_validity = list(coupons.values_list('is_active',flat=True))

        #     for i in range(len(coupon_codes)):
        #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
        #             coupon_percent = coupon_amounts[i]
        #             break


        #     coupon_amount = (sum_total * coupon_percent)/100
        #     sum_total = sum_total - coupon_amount

        # else:

        #     sum_total = sum_total



        #This method is to calculate the total price
    def get_discount(self,instance):
        sum_total = 0
        discount_total = 0 
        admin = ["Pending","Approved"]
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in=admin,product_status="None",delivery_removed=False)
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
            print("discount")
            print(len(order_quantity))
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount


                    elif product_discount.discount_type == "percentage":

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            #total_price = (p_price * order_quantity[i]) - total_discount
                            discount_total += total_discount

                    else:

                        total_price = (p_price * order_quantity[i])
                        # sum_total += total_price
                        discount_total += 0 


                else:

                   
                    # total_price = (p_price * order_quantity[i])
                    #sum_total += total_discount
                    discount_total += 0 


                print("sum total")


                # print(sum_total)

        else:
            discount_total = 0

        # current_date = timezone.now().date()
        # coupon_percent = 0


        # try:
        #     order = Order.objects.get(pk=instance.id)

        # except:
        #     order = None

        # if order:

        #     coupon_code = order.coupon_code

        #     coupons = Cupons.objects.all()
        #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
        #     coupon_amounts = list(coupons.values_list('amount',flat=True))
        #     coupon_start = list(coupons.values_list('start_from',flat=True))
        #     coupon_end = list(coupons.values_list('valid_to',flat=True))
        #     coupon_validity = list(coupons.values_list('is_active',flat=True))

        #     for i in range(len(coupon_codes)):
        #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
        #             coupon_percent = coupon_amounts[i]
        #             break


        #     coupon_amount = (sum_total * coupon_percent)/100
        #     sum_total = sum_total - coupon_amount

        # else:

        #     sum_total = sum_total

        float_total = format(discount_total, '0.2f')
        return float_total



        #This method is to calculate the total price
    def get_coupon_discount(self,instance):
        sum_total = 0
        admin = ["Pending","Approved"]
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in =admin,product_status="None",delivery_removed=False)
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        print()

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price


                    elif product_discount.discount_type == "percentage":

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price

                    else:

                        total_price = (p_price * order_quantity[i])
                        sum_total += total_price


                else:

                   
                    total_price = (p_price * order_quantity[i])
                    sum_total += total_price


                print("sum total")


                print(sum_total)

        else:
            sum_total = 0

        current_date = timezone.now().date()
        coupon_percent = 0
        coupon_amount = 0 


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break


            coupon_amount = (sum_total * coupon_percent)/100
            #sum_total = sum_total - coupon_amount
            # sum_total = coupon_amount

        else:

            sum_total = sum_total
            coupon_amount = 0 

        float_total = format(coupon_amount, '0.2f')
        return float_total



    def get_overall_discount(self,instance):
        sum_total = 0
        discount_total = 0
        admin = ["Pending","Approved"]
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in = admin,product_status="None",delivery_removed=False)
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            discount_total = 0 
            p_price = 0
            print("overalldiscount")
            print(len(order_quantity))
       
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_price = None

                print(product_price)
                try:

                    product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

                except:
                    product_discount = None

                print("product_discount")

                # print(product_discount.specification_id)
                # print(product_discount.amount)
               

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

         
                if product_discount is not None:

                    if product_discount.discount_type == "amount":

                        print("amount ey dhuktese")

                        

                        if product_discount.amount:
                            p_discount = product_discount.amount
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount


                    elif product_discount.discount_type == "percentage":


                        print("percentage ey dhuktese")

                        if product_discount.amount:
                            p_discount = product_discount.amount
                            p_discount = (p_discount * p_price)/100
                        else:
                            p_discount = 0

                   
                        current_date = timezone.now().date()
                        start_date = current_date
                        end_date = current_date
                       

                        if product_discount.start_date:
                            start_date = product_discount.start_date
                        else:
                            start_date = current_date

                        if product_discount.end_date:
                            end_date = product_discount.end_date

                        else:

                            end_date = current_date


                        if (current_date >= start_date) and (current_date <= end_date):
                            total_discount = p_discount * order_quantity[i]
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount

                        else:

                            total_discount = 0
                            total_price = (p_price * order_quantity[i]) - total_discount
                            sum_total += total_price
                            discount_total += total_discount

                    else:

                        total_discount = 0 

                        total_price = (p_price * order_quantity[i])
                        sum_total += total_price
                        discount_total += total_discount


                else:

                   
                    total_price = (p_price * order_quantity[i])
                    sum_total += total_price
                    total_discount = 0 
                    discount_total += total_discount


                print("sum total")


                print(discount_total)

        else:
            discount_total = 0
            sum_total = 0

        current_date = timezone.now().date()
        coupon_percent = 0
        coupon_amount = 0
        coupon_total = 0 


        try:
            order = Order.objects.get(pk=instance.id)

        except:
            order = None

        if order:

            coupon_code = order.coupon_code

            coupons = Cupons.objects.all()
            coupon_codes = list(coupons.values_list('cupon_code',flat=True))
            coupon_amounts = list(coupons.values_list('amount',flat=True))
            coupon_start = list(coupons.values_list('start_from',flat=True))
            coupon_end = list(coupons.values_list('valid_to',flat=True))
            coupon_validity = list(coupons.values_list('is_active',flat=True))

            for i in range(len(coupon_codes)):
                if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
                    coupon_percent = coupon_amounts[i]
                    break


            coupon_amount = (sum_total * coupon_percent)/100
            #sum_total = sum_total - coupon_amount
            # sum_total = coupon_amount

        else:

            sum_total = sum_total
            coupon_amount = 0 

        total = coupon_amount + discount_total

        float_total = format(total, '0.2f')
        return float_total





class PoSOrderSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField(method_name='order_details')
    #point_total = serializers.SerializerMethodField(method_name='get_point')


   
    class Meta:
        model = Order
        #fields ='__all__'
        fields = ('id','date_created','order_status','delivery_status','admin_status','user_id','non_verified_user_id','ip_address','checkout_status','coupon_code','coupon','ordered_date','is_seller','is_pos','admin_id','pos_additional_discount','pos_additional_discount_type','sub_total','grand_total','payment','changes','due','vat','num_items','items')


    def order_details(self,instance):
        print("posOrder serializer er moddhe")
        print(instance.id)
        details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,delivery_removed=False,product_status="None").order_by('date_added').values()
        list_result = [entry for entry in details]
        for i in range(len(list_result)):
            product_id = list_result[i]['product_id']
            specification_id = list_result[i]['specification_id']
            quantity = list_result[i]['total_quantity']
            try:
                product_images = ProductImage.objects.filter(product_id = product_id)
            except:
                product_images = None

            images= []

            if product_images:
                images= list(product_images.values_list('image_url',flat=True).distinct())

            list_result[i]['product_images'] = images

            try:
                product_price = ProductPrice.objects.filter(specification_id=specification_id).last()
            except:
                product_price = None

            
            try:

                product_discount = discount_product.objects.filter(specification_id=specification_id).last()

            except:
                product_discount = None
            

            if product_price is not None:
                p_price = product_price.price

            else:
                p_price = 0

            

        
            if product_discount is not None:

                if product_discount.discount_type == "amount":

                    

                    if product_discount.amount:
                        p_discount = product_discount.amount
                    else:
                        p_discount = 0

                
                    current_date = timezone.now().date()
                    start_date = current_date
                    end_date = current_date
                    

                    if product_discount.start_date:
                        start_date = product_discount.start_date
                    else:
                        start_date = current_date

                    if product_discount.end_date:
                        end_date = product_discount.end_date

                    else:

                        end_date = current_date


                    if (current_date >= start_date) and (current_date <= end_date):
                        unit_discount = p_discount
                        total_discount = p_discount * quantity
                        #total_price = (p_price * order_quantity[i]) - total_discount
                        

                    else:

                        total_discount = 0
                        unit_discount = 0
                        #total_price = (p_price * order_quantity[i]) - total_discount
                       


                elif product_discount.discount_type == "percentage":

                    if product_discount.amount:
                        p_discount = product_discount.amount
                        p_discount = (p_discount * p_price)/100
                    else:
                        p_discount = 0

                
                    current_date = timezone.now().date()
                    start_date = current_date
                    end_date = current_date
                    

                    if product_discount.start_date:
                        start_date = product_discount.start_date
                    else:
                        start_date = current_date

                    if product_discount.end_date:
                        end_date = product_discount.end_date

                    else:

                        end_date = current_date


                    if (current_date >= start_date) and (current_date <= end_date):
                        unit_discount = p_discount
                        total_discount = p_discount * quantity
                        #total_price = (p_price * order_quantity[i]) - total_discount
                        

                    else:

                        total_discount = 0
                        unit_discount = 0 
                        #total_price = (p_price * order_quantity[i]) - total_discount
                        

                else:

                    # total_price = (p_price * order_quantity[i])
                    # sum_total += total_price
                    # discount_total += 0 
                    unit_discount = 0 
                    total_discount = 0 


            else:

                
                # total_price = (p_price * order_quantity[i])
                #sum_total += total_discount
                unit_discount = 0 
                total_discount = 0
                

            list_result[i]['unit_discount'] = unit_discount
            list_result[i]['total_discount'] = total_discount    
   

        return list_result


    def get_point(self,instance):
        sum_total = 0
        admin = ["Pending","Approved"]
        try:
            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,delivery_removed=False,product_status="None",admin_status__in=admin)

        except:
            order_details = None
        if order_details is not None:

            order_prices = order_details.values_list('specification_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            print("point_total")
            print(len(order_quantity))
           
            for i in range(len(order_quantity)):
                try:
                    product_point = ProductPoint.objects.filter(specification_id=order_prices[i]).last()
                except:
                    product_point = None

                if product_point is not None:
                    p_point = product_point.point
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
                        total_point = p_point * order_quantity[i]
                        sum_total += total_point

                else:
                    sum_total = sum_total


        else:
            sum_total = 0
               

        float_total = format(sum_total, '0.2f')
        return float_total




# class OrderSerializer(serializers.ModelSerializer):
#     price_total = serializers.SerializerMethodField(method_name='get_price')
#     point_total = serializers.SerializerMethodField(method_name='get_point')
#     orders = serializers.SerializerMethodField(method_name='order_details')
#     all_orders = serializers.SerializerMethodField(method_name='order_detailz')
#     #orders = serializers.SerializerMethodField(method_name='order_details')
#     coupon_percentage = serializers.SerializerMethodField(method_name='get_coupon')
#     #product = serializers.SerializerMethodField(method_name='get_coupon')
#     invoice_id = serializers.SerializerMethodField(method_name='get_invoice_id')
#     reference_id = serializers.SerializerMethodField(method_name='get_reference')
#     phone_number = serializers.SerializerMethodField(method_name='get_phone_number')
#     discount = serializers.SerializerMethodField(method_name='get_discount')
#     sub_price = serializers.SerializerMethodField(method_name='get_sub_price')
#     coupon_discount = serializers.SerializerMethodField(method_name='get_coupon_discount')
#     overall_discount = serializers.SerializerMethodField(method_name='get_overall_discount')

   
#     class Meta:
#         model = Order
#         #fields ='__all__'
#         fields = ('id','date_created','order_status','delivery_status','admin_status','user_id','non_verified_user_id','ip_address','checkout_status','price_total','coupon_code','coupon_percentage','point_total','ordered_date','invoice_id','orders','all_orders','reference_id','is_seller','phone_number','discount','sub_price','coupon_discount','overall_discount','transaction_id','payment_method')

    
#     def get_phone_number(self,instance):

#         phone_number = ""

#         try:
#             order_info = OrderInfo.objects.get(order_id=instance.id)

#         except:
#             order_info = None 

#         print("order_info")
#         print(order_info)

#         if order_info:

#             if order_info.billing_address_id:
#                 billing_address_id = order_info.billing_address_id

#             else:
#                 billing_address_id = 0




#             try:
#                 billing_address = BillingAddress.objects.get(id=billing_address_id)
#             except:
#                 billing_address = None 


#             print("billingaddress")
#             print(billing_address)

#             if billing_address:
#                 if billing_address.phone_number:
#                     phone_number = billing_address.phone_number

#                 else:
#                     phone_number = ""

#             else:
#                 phone_number = ""

#         else:
#             phone_number = ""

#         return phone_number
            


#     #This method is to calculate the total price
#     def get_price(self,instance):
#         sum_total = 0
#         admin = ["Pending","Approved"]
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,delivery_removed=False,product_status="None",admin_status__in=admin)
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
#             print("totalprice")
#             print(len(order_quantity))
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

#                         print()

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price


#                     elif product_discount.discount_type == "percentage":

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                     else:

#                         total_price = (p_price * order_quantity[i])
#                         sum_total += total_price


#                 else:

                   
#                     total_price = (p_price * order_quantity[i])
#                     sum_total += total_price


#                 print("sum total")


#                 print(sum_total)

#         else:
#             sum_total = 0

#         current_date = timezone.now().date()
#         coupon_percent = 0


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break


#             coupon_amount = (sum_total * coupon_percent)/100
#             sum_total = sum_total - coupon_amount

#         else:

#             sum_total = sum_total

#         float_total = format(sum_total, '0.2f')
#         return float_total


#     def get_coupon(self,instance):

#         current_date = timezone.now().date()
#         coupon_percent = 0


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break

#         else:
#             coupon_percent = 0


#         coupon_percentage = str(coupon_percent)+" %"

#         return coupon_percentage


#     def get_point(self,instance):
#         sum_total = 0
#         admin = ["Pending","Approved"]
#         try:
#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,delivery_removed=False,product_status="None",admin_status__in=admin)

#         except:
#             order_details = None
#         if order_details is not None:

#             order_prices = order_details.values_list('product_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             print("point_total")
#             print(len(order_quantity))
           
#             for i in range(len(order_quantity)):
#                 try:
#                     product_point = ProductPoint.objects.filter(product_id=order_prices[i]).last()
#                 except:
#                     product_point = None

#                 if product_point is not None:
#                     p_point = product_point.point
#                     current_date = timezone.now().date()

#                     start_date = current_date
#                     end_date = current_date

#                     if product_point.start_date:
#                         start_date = product_point.start_date
#                     else:
#                         start_date = current_date

#                     if product_point.end_date:
#                         end_date = product_point.end_date

#                     else:

#                         end_date = current_date
                   
#                     if (current_date >= start_date) and (current_date <= end_date):
#                         total_point = p_point * order_quantity[i]
#                         sum_total += total_point

#                 else:
#                     sum_total = sum_total


#         else:
#             sum_total = 0
               

#         float_total = format(sum_total, '0.2f')
#         return float_total


#     def order_details(self,instance):
#         details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,delivery_removed=False,product_status="None").order_by('date_added').values()
#         list_result = [entry for entry in details]
#         for i in range(len(list_result)):
#             product_id = list_result[i]['product_id']
#             specification_id = list_result[i]['specification_id']
#             try:
#                 product_images = ProductImage.objects.filter(product_id = product_id)
#             except:
#                 product_images = None

#             images= []

#             if product_images:
#                 images= list(product_images.values_list('image_url',flat=True).distinct())

#             list_result[i]['product_images'] = images

#             try:
#                 barcode = ProductCode.objects.filter(specification_id=specification_id).last()

#             except:
#                 barcode = None 

#             product_barcode = ""

#             if barcode:
#                 product_barcode = barcode.Barcode

#             list_result[i]['product_barcode'] = product_barcode

       

#         return list_result


#     def get_invoice_id(self,instance):

#         try:

#             invoice = Invoice.objects.filter(order_id=instance.id).last()

#         except:

#             invoice = None 

#         if invoice:

#             if invoice.id:

#                 invoice_id = invoice.id

#             else:

#                 invoice_id = 0 

#         else:

#             invoice_id = 0 


#         return invoice_id


#     def get_reference(self,instance):

#         try:

#             invoice = Invoice.objects.filter(order_id=instance.id).last()

#         except:

#             invoice = None 

#         if invoice:

#             if invoice.ref_invoice:

#                 invoice_id = invoice.ref_invoice

#             else:

#                 invoice_id = 0 

#         else:

#             invoice_id = 0 


#         return invoice_id


#     def order_detailz(self,instance):
#         details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False,delivery_removed=False).order_by('date_added').values()
#         list_result = [entry for entry in details]
#         for i in range(len(list_result)):
#             product_id = list_result[i]['product_id']
#             specification_id = list_result[i]['specification_id']
#             try:
#                 product_images = ProductImage.objects.filter(product_id = product_id)
#             except:
#                 product_images = None

#             images= []

#             if product_images:
#                 images= list(product_images.values_list('image_url',flat=True).distinct())

#             list_result[i]['product_images'] = images

            
#             try:
#                 barcode = ProductCode.objects.filter(specification_id=specification_id).last()

#             except:
#                 barcode = None 

#             product_barcode = ""

#             if barcode:
#                 product_barcode = barcode.Barcode

#             list_result[i]['product_barcode'] = product_barcode

           

       

#         return list_result


#         #This method is to calculate the total price
#     def get_sub_price(self,instance):
#         sum_total = 0
#         admin = ["Pending","Approved"]
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in = admin,product_status="None",delivery_removed=False)
#         except:
#             order_details = None

#         # print("sub price")
#         # print(len(order_quantity))

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
#             print("sub price")
#             print(len(order_quantity))
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 # try:

#                 #     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 # except:
#                 #     product_discount = None
               

#                 if product_price:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 # if product_discount is not None:

#                 #     if product_discount.discount_type == "amount":

#                 #         print()

#                 #         if product_discount.amount:
#                 #             p_discount = product_discount.amount
#                 #         else:
#                 #             p_discount = 0

                   
#                 #         current_date = timezone.now().date()
#                 #         start_date = current_date
#                 #         end_date = current_date
                       

#                 #         if product_discount.start_date:
#                 #             start_date = product_discount.start_date
#                 #         else:
#                 #             start_date = current_date

#                 #         if product_discount.end_date:
#                 #             end_date = product_discount.end_date

#                 #         else:

#                 #             end_date = current_date


#                 #         if (current_date >= start_date) and (current_date <= end_date):
#                 #             total_discount = p_discount * order_quantity[i]
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price

#                 #         else:

#                 #             total_discount = 0
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price


#                 #     elif product_discount.discount_type == "percentage":

#                 #         if product_discount.amount:
#                 #             p_discount = product_discount.amount
#                 #             p_discount = (p_discount * p_price)/100
#                 #         else:
#                 #             p_discount = 0

                   
#                 #         current_date = timezone.now().date()
#                 #         start_date = current_date
#                 #         end_date = current_date
                       

#                 #         if product_discount.start_date:
#                 #             start_date = product_discount.start_date
#                 #         else:
#                 #             start_date = current_date

#                 #         if product_discount.end_date:
#                 #             end_date = product_discount.end_date

#                 #         else:

#                 #             end_date = current_date


#                 #         if (current_date >= start_date) and (current_date <= end_date):
#                 #             total_discount = p_discount * order_quantity[i]
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price

#                 #         else:

#                 #             total_discount = 0
#                 #             total_price = (p_price * order_quantity[i]) - total_discount
#                 #             sum_total += total_price

#                 #     else:

#                 #         total_price = (p_price * order_quantity[i])
#                 #         sum_total += total_price


#                 # else:

                   
#                 total_price = (p_price * order_quantity[i])
#                 sum_total += total_price


#                 print("sum total")


#                 print(sum_total)

#         else:
#             sum_total = 0

#         # current_date = timezone.now().date()
#         # coupon_percent = 0


#         float_total = format(sum_total, '0.2f')
#         return float_total




#         # try:
#         #     order = Order.objects.get(pk=instance.id)

#         # except:
#         #     order = None

#         # if order:

#         #     coupon_code = order.coupon_code

#         #     coupons = Cupons.objects.all()
#         #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#         #     coupon_amounts = list(coupons.values_list('amount',flat=True))
#         #     coupon_start = list(coupons.values_list('start_from',flat=True))
#         #     coupon_end = list(coupons.values_list('valid_to',flat=True))
#         #     coupon_validity = list(coupons.values_list('is_active',flat=True))

#         #     for i in range(len(coupon_codes)):
#         #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#         #             coupon_percent = coupon_amounts[i]
#         #             break


#         #     coupon_amount = (sum_total * coupon_percent)/100
#         #     sum_total = sum_total - coupon_amount

#         # else:

#         #     sum_total = sum_total



#         #This method is to calculate the total price
#     def get_discount(self,instance):
#         sum_total = 0
#         discount_total = 0 
#         admin = ["Pending","Approved"]
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in=admin,product_status="None",delivery_removed=False)
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
#             print("discount")
#             print(len(order_quantity))
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

                        

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount


#                     elif product_discount.discount_type == "percentage":

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             #total_price = (p_price * order_quantity[i]) - total_discount
#                             discount_total += total_discount

#                     else:

#                         total_price = (p_price * order_quantity[i])
#                         # sum_total += total_price
#                         discount_total += 0 


#                 else:

                   
#                     # total_price = (p_price * order_quantity[i])
#                     #sum_total += total_discount
#                     discount_total += 0 


#                 print("sum total")


#                 # print(sum_total)

#         else:
#             discount_total = 0

#         # current_date = timezone.now().date()
#         # coupon_percent = 0


#         # try:
#         #     order = Order.objects.get(pk=instance.id)

#         # except:
#         #     order = None

#         # if order:

#         #     coupon_code = order.coupon_code

#         #     coupons = Cupons.objects.all()
#         #     coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#         #     coupon_amounts = list(coupons.values_list('amount',flat=True))
#         #     coupon_start = list(coupons.values_list('start_from',flat=True))
#         #     coupon_end = list(coupons.values_list('valid_to',flat=True))
#         #     coupon_validity = list(coupons.values_list('is_active',flat=True))

#         #     for i in range(len(coupon_codes)):
#         #         if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#         #             coupon_percent = coupon_amounts[i]
#         #             break


#         #     coupon_amount = (sum_total * coupon_percent)/100
#         #     sum_total = sum_total - coupon_amount

#         # else:

#         #     sum_total = sum_total

#         float_total = format(discount_total, '0.2f')
#         return float_total



#         #This method is to calculate the total price
#     def get_coupon_discount(self,instance):
#         sum_total = 0
#         admin = ["Pending","Approved"]
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in =admin,product_status="None",delivery_removed=False)
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             p_price = 0
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

#                         print()

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price


#                     elif product_discount.discount_type == "percentage":

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price

#                     else:

#                         total_price = (p_price * order_quantity[i])
#                         sum_total += total_price


#                 else:

                   
#                     total_price = (p_price * order_quantity[i])
#                     sum_total += total_price


#                 print("sum total")


#                 print(sum_total)

#         else:
#             sum_total = 0

#         current_date = timezone.now().date()
#         coupon_percent = 0
#         coupon_amount = 0 


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break


#             coupon_amount = (sum_total * coupon_percent)/100
#             #sum_total = sum_total - coupon_amount
#             # sum_total = coupon_amount

#         else:

#             sum_total = sum_total
#             coupon_amount = 0 

#         float_total = format(coupon_amount, '0.2f')
#         return float_total



#     def get_overall_discount(self,instance):
#         sum_total = 0
#         discount_total = 0
#         admin = ["Pending","Approved"]
#         try:

#             order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False,admin_status__in = admin,product_status="None",delivery_removed=False)
#         except:
#             order_details = None

#         if order_details is not None:

#             order_prices = order_details.values_list('specification_id',flat = True)
#             order_quantity = order_details.values_list('total_quantity',flat = True)
#             sum_total= 0
#             discount_total = 0 
#             p_price = 0
#             print("overalldiscount")
#             print(len(order_quantity))
       
#             for i in range(len(order_quantity)):
#                 try:
#                     product_price = ProductPrice.objects.filter(specification_id=order_prices[i]).last()
#                 except:
#                     product_price = None

#                 print(product_price)
#                 try:

#                     product_discount = discount_product.objects.filter(specification_id=order_prices[i]).last()

#                 except:
#                     product_discount = None

#                 print("product_discount")

#                 # print(product_discount.specification_id)
#                 # print(product_discount.amount)
               

#                 if product_price is not None:
#                     p_price = product_price.price

#                 else:
#                     p_price = 0

               

         
#                 if product_discount is not None:

#                     if product_discount.discount_type == "amount":

#                         print("amount ey dhuktese")

                        

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount


#                     elif product_discount.discount_type == "percentage":


#                         print("percentage ey dhuktese")

#                         if product_discount.amount:
#                             p_discount = product_discount.amount
#                             p_discount = (p_discount * p_price)/100
#                         else:
#                             p_discount = 0

                   
#                         current_date = timezone.now().date()
#                         start_date = current_date
#                         end_date = current_date
                       

#                         if product_discount.start_date:
#                             start_date = product_discount.start_date
#                         else:
#                             start_date = current_date

#                         if product_discount.end_date:
#                             end_date = product_discount.end_date

#                         else:

#                             end_date = current_date


#                         if (current_date >= start_date) and (current_date <= end_date):
#                             total_discount = p_discount * order_quantity[i]
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount

#                         else:

#                             total_discount = 0
#                             total_price = (p_price * order_quantity[i]) - total_discount
#                             sum_total += total_price
#                             discount_total += total_discount

#                     else:

#                         total_discount = 0 

#                         total_price = (p_price * order_quantity[i])
#                         sum_total += total_price
#                         discount_total += total_discount


#                 else:

                   
#                     total_price = (p_price * order_quantity[i])
#                     sum_total += total_price
#                     total_discount = 0 
#                     discount_total += total_discount


#                 print("sum total")


#                 print(discount_total)

#         else:
#             discount_total = 0
#             sum_total = 0

#         current_date = timezone.now().date()
#         coupon_percent = 0
#         coupon_amount = 0
#         coupon_total = 0 


#         try:
#             order = Order.objects.get(pk=instance.id)

#         except:
#             order = None

#         if order:

#             coupon_code = order.coupon_code

#             coupons = Cupons.objects.all()
#             coupon_codes = list(coupons.values_list('cupon_code',flat=True))
#             coupon_amounts = list(coupons.values_list('amount',flat=True))
#             coupon_start = list(coupons.values_list('start_from',flat=True))
#             coupon_end = list(coupons.values_list('valid_to',flat=True))
#             coupon_validity = list(coupons.values_list('is_active',flat=True))

#             for i in range(len(coupon_codes)):
#                 if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):
#                     coupon_percent = coupon_amounts[i]
#                     break


#             coupon_amount = (sum_total * coupon_percent)/100
#             #sum_total = sum_total - coupon_amount
#             # sum_total = coupon_amount

#         else:

#             sum_total = sum_total
#             coupon_amount = 0 

#         total = coupon_amount + discount_total

#         float_total = format(total, '0.2f')
#         return float_total
