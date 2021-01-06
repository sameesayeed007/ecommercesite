# from tango_ecomerce_child_backend.Intense.models import CompanyInfo
from rest_framework import serializers
from django.contrib.auth.models import User
from Intense.models import (ProductPoint,Terminal,ProductPrice,ProductSpecification ,CompanyInfo,Category,Sub_Category,Sub_Sub_Category,Product,Comment,CommentReply,
Reviews,discount_product,ProductImage,Cupons,TerminalUsers,User,product_delivery_area,
ProductImpression,DeliveryArea,DeliveryLocation,Warehouse,Shop,WarehouseInfo,ShopInfo,inventory_report,Category,Sub_Category,Sub_Sub_Category,
ProductBrand,DeliveryInfo,SpecificationImage, SpecificationPrice,MotherSpecificationPrice, ProductCode)
#from django.contrib.auth.models import User
#from Cart.models import ProductPoint
from django.utils import timezone
from colour import Color
from User_details.serializers import UserSerializerz
import requests
from django.urls import reverse,reverse_lazy
#from Intense.Integral_apis import ratings
import json



#site_path = "http://127.0.0.1:8000/"
#site_path = "https://tango99.herokuapp.com/"
#site_path = "http://128.199.114.154:8080/"
#site_path = "http://128.199.66.61:8080/"

# site_path = "http://128.199.66.61:8080/"
site_path = "https://tes.com.bd/"


# Serializers define the API representation.

global_warehouse_id = 0 
global_shop_id = 0
def get_id(warehouse_id,shop_id):
    # print("method er moddhe dhuktese")
    globals()['global_warehouse_id'] = warehouse_id
    globals()['global_shop_id'] = shop_id
    

    


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = "__all__"


class ProductPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPoint
        fields = "__all__"

class DeliveryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInfo
        fields = "__all__"

class SpecificationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationImage
        fields = "__all__"

class ProductSpecificationSerializer(serializers.ModelSerializer):
    #hexcolor = serializers.SerializerMethodField(method_name='get_color')
    class Meta:
        model = ProductSpecification
        fields = "__all__"

class ProductDeliveryAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_delivery_area
        fields = "__all__"

class ProductSpecificationSerializerz(serializers.ModelSerializer):
    #hexcolor = serializers.SerializerMethodField(method_name='get_color')
    delivery_info = serializers.SerializerMethodField(method_name='get_info')
    price = serializers.SerializerMethodField(method_name='get_price')
    discount = serializers.SerializerMethodField(method_name='get_discount')
    point = serializers.SerializerMethodField(method_name='get_point')

    product_title = serializers.SerializerMethodField(method_name='get_title')
    class Meta:
        model = ProductSpecification
        fields = "__all__"

    def get_info(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = DeliveryInfo.objects.get(specification_id=instance.id)

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = DeliveryInfoSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data


    def get_price(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = ProductPrice.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductPriceSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data



    def get_point(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = ProductPoint.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductPointSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data


    def get_discount(self,instance):


        try:
            delivery_info = discount_product.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductDiscountSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data

        






    def get_title(self,instance):

        title = ""

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None

        if product:

            title = product.title

        return title
    
    
    



class ProductSpecificationSerializer1(serializers.ModelSerializer):


    new_price = serializers.SerializerMethodField(method_name='get_new_price')
    old_price = serializers.SerializerMethodField(method_name='get_old_price')
    discount = serializers.SerializerMethodField(method_name='get_discount')
    point = serializers.SerializerMethodField(method_name='get_point')
    delivery_info = serializers.SerializerMethodField(method_name='get_info')
    price = serializers.SerializerMethodField(method_name='get_price')
    purchase_price = serializers.SerializerMethodField(method_name='get_purchase_price')
    SKU = serializers.SerializerMethodField(method_name='get_SKU')
    barcode = serializers.SerializerMethodField(method_name='get_barcode')
    delivery_location = serializers.SerializerMethodField(method_name='get_delivery_info')
    # delivery_loc = serializers.SerializerMethodField(method_name='get_delivery_info')
    max_min = serializers.SerializerMethodField(method_name='get_max_min')
    
    

    # discount = serializers.SerializerMethodField(method_name='get_discount')
    # point = serializers.SerializerMethodField(method_name='get_point')


    class Meta:
        model = ProductSpecification
        fields = ('id','product_id','color','size','weight','unit','weight_unit','warranty','warranty_unit','vat','quantity','seller_quantity','remaining','SKU','barcode','new_price','old_price','purchase_price','price','discount','point','delivery_info','delivery_location','manufacture_date','expire','admin_status','max_min','shared','is_own','specification_status','on_hold') 

    def get_max_min(self,instance):
        max_min = []
        try:
            product_spec = SpecificationPrice.objects.filter(specification_id = instance.id)
        except:
            product_spec = None 

        if product_spec:
            product_spec_serializer = MaxMinSerializer1(product_spec,many=True)
            max_min = product_spec_serializer.data
        else:
            max_min = []

        return max_min
        
    def get_SKU(self,instance):



        try:
            delivery_info = ProductCode.objects.get(specification_id=instance.id)

        except:

            delivery_info = None 

        if delivery_info:


            # if delivery_info.manual_SKU:


            #     SKU = delivery_info.manual_SKU


            if delivery_info.SKU:

                SKU = delivery_info.SKU

            else:

                SKU = "N/A"



        else:

            SKU = "N/A"


        
        return SKU
    
    def get_delivery_info(self,instance):
        
        main_data = []
        
        try:
            delivery_places = product_delivery_area.objects.filter(specification_id = instance.id)
            
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
                        product_areas = product_delivery_area.objects.get(specification_id = instance.id,delivery_area_id=area_ids[i])
                        
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
            
            
        return main_data



    def get_barcode(self,instance):



        try:
            delivery_info = ProductCode.objects.get(specification_id=instance.id)

        except:

            delivery_info = None 

        if delivery_info:


            if delivery_info.manual_Barcode:


                barcode = delivery_info.manual_Barcode


            elif delivery_info.Barcode:

                barcode = delivery_info.Barcode

            else:

                barcode = "N/A"



        else:

            barcode = "N/A"


        
        return barcode




    def get_purchase_price(self,instance):



        try:
            delivery_info = ProductPrice.objects.filter(specification_id=instance.id).last()


        except:

            delivery_info = None 

        if delivery_info:


            if delivery_info.purchase_price:


                purchase_price = delivery_info.purchase_price


            else:

                purchase_price = 0



        else:


            purchase_price = 0
    

        # return purchase_price

        float_total = format(purchase_price, '0.2f')
        return float_total

      




  



    def get_info(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = DeliveryInfo.objects.get(specification_id=instance.id)

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = DeliveryInfoSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data


    def get_price(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = ProductPrice.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductPriceSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data



    def get_point(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = ProductPoint.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductPointSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data


    def get_new_price(self,instance):

        new_price = 0
        discount = 0  


        try:


            p_price = ProductPrice.objects.filter(specification_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            new_price =p_price.price

            try:

                p_discount = discount_product.objects.filter(specification_id = instance.id).last()

            except:

                p_discount = None


            if p_discount is not None:



                if p_discount.discount_type == "amount":


                    #Discount


                    if p_discount.amount:
                        discount = p_discount.amount
                    else:
                        discount = 0

                
                    current_date = timezone.now().date()
                    # discount_start_date = p_discount.start_date

                    if p_discount.end_date:

                        discount_end_date = p_discount.end_date

                    else:
                        discount_end_date = timezone.now().date()

                    if p_discount.start_date:
                        discount_start_date = p_discount.start_date

                    else:
                        discount_start_date = timezone.now().date()

                            

                    if (current_date >= discount_start_date) and (current_date <= discount_end_date):

                        new_price = new_price - discount

                    else:
                        discount =0 
                        new_price = new_price - discount


                elif p_discount.discount_type == "percentage":


                                        #Discount


                    if p_discount.amount:
                        discount = p_discount.amount
                        # print(type(discount))
                        # print(type(p_price))
                        discount =(discount * new_price)/100
                    else:
                        discount = 0

                
                    current_date = timezone.now().date()
                    # discount_start_date = p_discount.start_date

                    if p_discount.end_date:

                        discount_end_date = p_discount.end_date

                    else:
                        discount_end_date = timezone.now().date()

                    if p_discount.start_date:
                        discount_start_date = p_discount.start_date

                    else:
                        discount_start_date = timezone.now().date()

                            

                    if (current_date >= discount_start_date) and (current_date <= discount_end_date):

                        new_price = new_price - discount

                    else:
                        discount =0 
                        new_price = new_price - discount


                else:
                    discount = 0 
                    new_price = new_price - discount 

            else:
                discount = 0
                new_price = new_price - discount

        else:

            new_price = 0
            
        float_total = format(new_price, '0.2f')
        return float_total


   



    def get_old_price(self,instance):



        old_price = 0 


        try:


            p_price = ProductPrice.objects.filter(specification_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            old_price =p_price.price

        else:
            old_price = 0


        float_total = format(old_price, '0.2f')
        return float_total


    def get_discount(self,instance):


        try:
            delivery_info = discount_product.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductDiscountSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data






class ProductSpecificationSerializer5(serializers.ModelSerializer):


    new_price = serializers.SerializerMethodField(method_name='get_new_price')
    old_price = serializers.SerializerMethodField(method_name='get_old_price')
    discount = serializers.SerializerMethodField(method_name='get_discount')
    point = serializers.SerializerMethodField(method_name='get_point')
    delivery_info = serializers.SerializerMethodField(method_name='get_info')
    price = serializers.SerializerMethodField(method_name='get_price')
    purchase_price = serializers.SerializerMethodField(method_name='get_purchase_price')
    SKU = serializers.SerializerMethodField(method_name='get_SKU')
    barcode = serializers.SerializerMethodField(method_name='get_barcode')
    warehouse = serializers.SerializerMethodField(method_name='get_warehouse_info')
    shop = serializers.SerializerMethodField(method_name='get_shop_info')
    

    # discount = serializers.SerializerMethodField(method_name='get_discount')
    # point = serializers.SerializerMethodField(method_name='get_point')


    class Meta:
        model = ProductSpecification
        fields = ('id','product_id','color','size','weight','unit','weight_unit','warranty','warranty_unit','vat','quantity','seller_quantity','remaining','SKU','barcode','new_price','old_price','purchase_price','price','discount','point','delivery_info','manufacture_date','expire','warehouse','shop','shared','is_own','specification_status','on_hold')

    def get_warehouse_info(self,instance):
        print("global_warehouse_id")
        print(global_warehouse_id)

        try:

            warehouse_info = WarehouseInfo.objects.filter(specification_id=instance.id,warehouse_id=global_warehouse_id)

        except:

            warehouse_info = None 


        print("warehouse")

        print(warehouse_info)


        if warehouse_info:

            warehouse_serializer = WarehousePOSSerializer(warehouse_info,many=True)


            warehouse_data = warehouse_serializer.data 


        else:

            warehouse_data = [] 


        return warehouse_data 



    def get_shop_info(self,instance):
        print("global_shop_id")
        print(global_shop_id)

        try:

            shop_info = ShopInfo.objects.filter(specification_id=instance.id,shop_id=global_shop_id)

        except:

            shop_info = None 

        print("shop")
        print(shop_info)


        if shop_info:

            shop_serializer = ShopPOSSerializer(shop_info,many=True)


            shop_data = shop_serializer.data 


        else:

            shop_data = [] 


        return shop_data 




    def get_SKU(self,instance):



        try:
            delivery_info = ProductCode.objects.get(specification_id=instance.id)

        except:

            delivery_info = None 

        if delivery_info:


            if delivery_info.manual_SKU:


                SKU = delivery_info.manual_SKU


            elif delivery_info.SKU:

                SKU = delivery_info.SKU

            else:

                SKU = "N/A"



        else:

            SKU = "N/A"


        
        return SKU



    def get_barcode(self,instance):



        try:
            delivery_info = ProductCode.objects.get(specification_id=instance.id)

        except:

            delivery_info = None 

        if delivery_info:


            if delivery_info.manual_Barcode:


                barcode = delivery_info.manual_Barcode


            elif delivery_info.Barcode:

                barcode = delivery_info.Barcode

            else:

                barcode = "N/A"



        else:

            barcode = "N/A"


        
        return barcode




    def get_purchase_price(self,instance):



        try:
            delivery_info = ProductPrice.objects.filter(specification_id=instance.id).last()


        except:

            delivery_info = None 

        if delivery_info:


            if delivery_info.purchase_price:


                purchase_price = delivery_info.purchase_price


            else:

                purchase_price = 0



        else:


            purchase_price = 0
    

        # return purchase_price

        float_total = format(purchase_price, '0.2f')
        return float_total

      




  



    def get_info(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = DeliveryInfo.objects.get(specification_id=instance.id)

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = DeliveryInfoSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data


    def get_price(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = ProductPrice.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductPriceSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data



    def get_point(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = ProductPoint.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductPointSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data


    def get_new_price(self,instance):

        new_price = 0
        discount = 0  


        try:


            p_price = ProductPrice.objects.filter(specification_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            new_price =p_price.price

            try:

                p_discount = discount_product.objects.filter(specification_id = instance.id).last()

            except:

                p_discount = None


            if p_discount is not None:



                if p_discount.discount_type == "amount":


                    #Discount


                    if p_discount.amount:
                        discount = p_discount.amount
                    else:
                        discount = 0

                
                    current_date = timezone.now().date()
                    # discount_start_date = p_discount.start_date

                    if p_discount.end_date:

                        discount_end_date = p_discount.end_date

                    else:
                        discount_end_date = timezone.now().date()

                    if p_discount.start_date:
                        discount_start_date = p_discount.start_date

                    else:
                        discount_start_date = timezone.now().date()

                            

                    if (current_date >= discount_start_date) and (current_date <= discount_end_date):

                        new_price = new_price - discount

                    else:
                        discount =0 
                        new_price = new_price - discount


                elif p_discount.discount_type == "percentage":


                                        #Discount


                    if p_discount.amount:
                        discount = p_discount.amount
                        # print(type(discount))
                        # print(type(p_price))
                        discount =(discount * new_price)/100
                    else:
                        discount = 0

                
                    current_date = timezone.now().date()
                    # discount_start_date = p_discount.start_date

                    if p_discount.end_date:

                        discount_end_date = p_discount.end_date

                    else:
                        discount_end_date = timezone.now().date()

                    if p_discount.start_date:
                        discount_start_date = p_discount.start_date

                    else:
                        discount_start_date = timezone.now().date()

                            

                    if (current_date >= discount_start_date) and (current_date <= discount_end_date):

                        new_price = new_price - discount

                    else:
                        discount =0 
                        new_price = new_price - discount


                else:
                    discount = 0 
                    new_price = new_price - discount 

            else:
                discount = 0
                new_price = new_price - discount

        else:

            new_price = 0
            
        float_total = format(new_price, '0.2f')
        return float_total


   



    def get_old_price(self,instance):



        old_price = 0 


        try:


            p_price = ProductPrice.objects.filter(specification_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            old_price =p_price.price

        else:
            old_price = 0


        float_total = format(old_price, '0.2f')
        return float_total


    def get_discount(self,instance):


        try:
            delivery_info = discount_product.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductDiscountSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data

class ProductDetailSerializer2(serializers.ModelSerializer):
    old_price = serializers.SerializerMethodField(method_name='get_price')
    new_price = serializers.SerializerMethodField(method_name='get_discounted_price')
    specification = serializers.SerializerMethodField(method_name='get_specification')
    quantity = serializers.SerializerMethodField(method_name='get_quantity')
    variations = serializers.SerializerMethodField(method_name='get_variations')

    #availability = serializers.SerializerMethodField(method_name='available')
    ratings = serializers.SerializerMethodField(method_name='get_ratings')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    images = serializers.SerializerMethodField(method_name='get_images')
    imagez = serializers.SerializerMethodField(method_name='get_imagez')
    question_answers = serializers.SerializerMethodField(method_name='get_comments')
    specifications = serializers.SerializerMethodField(method_name='get_specifications')
    class Meta:
        model = Product
        fields = ('id','title','description','brand','quantity','key_features','old_price','new_price','specification','ratings','reviews','question_answers','images','imagez','specifications','variations','origin','shipping_country')

    def get_specifications(self,instance):

        specs = []

        try:

            prod_specs = ProductSpecification.objects.filter(product_id=instance.id)

        except:

            prod_specs = None 


        if prod_specs:

            product_serializer = ProductSpecificationSerializer1(prod_specs,many=True)
            product_data = product_serializer.data

        else:
            product_data = []


        return product_data

    def get_price(self,instance):
        p_price = 0

        try:
            product_price = ProductPrice.objects.filter(product_id = instance.id).last()
        except:
            product_price = None

        if product_price is not None:
            p_price = product_price.price

        else:
            p_price = 0

        float_total = format(p_price, '0.2f')
        return float_total


    def get_discounted_price(self,instance):
        p_price = 0
        p_discount = 0
        discounted_price =0


        try:
            product_price = ProductPrice.objects.filter(product_id=instance.id).last()
        except:
            product_price = None
        try:

            product_discount = discount_product.objects.filter(product_id=instance.id).last()

        except:
            product_discount = None
        

        if product_price is not None:
            p_price = product_price.price

        else:
            p_price = 0


        if product_discount is not None:


            if product_discount.amount:
                p_discount = product_discount.amount
            else:
                p_discount = 0



            #p_discount = product_discount.amount
            current_date = timezone.now().date()
            if product_discount.start_date:
                start_date = product_discount.start_date
            else:
                start_date = current_date

            if product_discount.end_date:
                end_date = product_discount.end_date

            else:
                end_date = current_date
            

            if(current_date >= start_date) and (current_date <= end_date):
                discounted_price = p_price - p_discount

            else:
                discounted_price = p_price

        else:
            discounted_price = p_price


        float_total = format(discounted_price, '0.2f')
        return float_total


    def get_ratings(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/ratings/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values


    def get_reviews(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/reviews_product/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values

    def get_comments(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/comments_product/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values


    # def get_specifications(self,instance):


    #     product_id = instance.id
    #     #site_path = "https://tango99.herokuapp.com/"

    #     url = site_path+ "productdetails/showspec/"+str(product_id)+"/"
    #     values = requests.get(url).json()
    #     return values

    def get_variations(self,instance):

        variations = []

        try:
            p_spec = ProductSpecification.objects.filter(product_id = instance.id,specification_status="Published")

        except:

            p_spec = None 


        if p_spec:

            varz = list(p_spec.values_list('weight_unit',flat=True).distinct())
            

            variations = varz 
            

        else:

            variations = [] 


        return variations



    def get_specification(self,instance):

        arr =  {'colors':[],'sizes':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            

            colors = list(p_spec.values_list('color',flat=True).distinct())
            print(colors)
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            print(sizes)
            # units = list(p_spec.values_list('unit',flat=True).distinct())
            # colors.remove(None)
            # sizes.remove(None)
            # if sizes == [None]:
            #     sizes= []


            # if colors == [None]:
            #     colors = []

            arr =  {'colors':colors,'sizes':sizes}

            return arr

        else:

            return arr


    def get_quantity(self,instance):

        #arr =  {'colors':[],'sizes':[],'units':[]}

        total_sum = 0


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            quantities = list(p_spec.values_list('quantity',flat=True))

            #total_sum = 0
            for i in range(len(quantities)):

                total_sum = total_sum + quantities[i]



            

            return total_sum

        else:

            return total_sum




    def get_images(self,instance):

        images=[]


        try:

            product_images = ProductImage.objects.filter(product_id = instance.id)

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


    def get_imagez(self,instance):
        replys = ProductImage.objects.filter(product_id=instance.id).values()
        list_result = [entry for entry in replys] 
    
        return list_result

class ProductDetailSerializer(serializers.ModelSerializer):
    old_price = serializers.SerializerMethodField(method_name='get_price')
    new_price = serializers.SerializerMethodField(method_name='get_discounted_price')
    specification = serializers.SerializerMethodField(method_name='get_specification')
    quantity = serializers.SerializerMethodField(method_name='get_quantity')

    #availability = serializers.SerializerMethodField(method_name='available')
    ratings = serializers.SerializerMethodField(method_name='get_ratings')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    images = serializers.SerializerMethodField(method_name='get_images')
    imagez = serializers.SerializerMethodField(method_name='get_imagez')
    question_answers = serializers.SerializerMethodField(method_name='get_comments')
    specifications = serializers.SerializerMethodField(method_name='get_specifications')
    class Meta:
        model = Product
        fields = ('id','title','description','brand','quantity','key_features','old_price','new_price','unit','specification','ratings','reviews','question_answers','images','imagez','specifications')

    def get_price(self,instance):
        p_price = 0

        try:
            product_price = ProductPrice.objects.filter(product_id = instance.id).last()
        except:
            product_price = None

        if product_price is not None:
            p_price = product_price.price

        else:
            p_price = 0

        float_total = format(p_price, '0.2f')
        return float_total


    def get_discounted_price(self,instance):
        p_price = 0
        p_discount = 0
        discounted_price =0


        try:
            product_price = ProductPrice.objects.filter(product_id=instance.id).last()
        except:
            product_price = None
        try:

            product_discount = discount_product.objects.filter(product_id=instance.id).last()

        except:
            product_discount = None
        

        if product_price is not None:
            p_price = product_price.price

        else:
            p_price = 0


        if product_discount is not None:


            if product_discount.amount:
                p_discount = product_discount.amount
            else:
                p_discount = 0



            #p_discount = product_discount.amount
            current_date = timezone.now().date()
            if product_discount.start_date:
                start_date = product_discount.start_date
            else:
                start_date = current_date

            if product_discount.end_date:
                end_date = product_discount.end_date

            else:
                end_date = current_date
            

            if(current_date >= start_date) and (current_date <= end_date):
                discounted_price = p_price - p_discount

            else:
                discounted_price = p_price

        else:
            discounted_price = p_price


        float_total = format(discounted_price, '0.2f')
        return float_total


    def get_ratings(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/ratings/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values


    def get_reviews(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/reviews_product/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values

    def get_comments(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/comments_product/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values


    # def get_specifications(self,instance):


    #     product_id = instance.id
    #     #site_path = "https://tango99.herokuapp.com/"

    #     url = site_path+ "productdetails/showspec/"+str(product_id)+"/"
    #     values = requests.get(url).json()
    #     return values

    def get_specification(self,instance):

        arr =  {'colors':[],'sizes':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            

            colors = list(p_spec.values_list('color',flat=True).distinct())
            print(colors)
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            print(sizes)
            # units = list(p_spec.values_list('unit',flat=True).distinct())
            colors.remove(None)
            sizes.remove(None)
            # if sizes == [None]:
            #     sizes= []


            # if colors == [None]:
            #     colors = []

            arr =  {'colors':colors,'sizes':sizes}

            return arr

        else:

            return arr


    def get_quantity(self,instance):

        #arr =  {'colors':[],'sizes':[],'units':[]}

        total_sum = 0


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            quantities = list(p_spec.values_list('quantity',flat=True))

            #total_sum = 0
            for i in range(len(quantities)):

                total_sum = total_sum + quantities[i]



            

            return total_sum

        else:

            return total_sum




    def get_images(self,instance):

        images=[]


        try:

            product_images = ProductImage.objects.filter(product_id = instance.id)

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


    def get_imagez(self,instance):
        replys = ProductImage.objects.filter(product_id=instance.id).values()
        list_result = [entry for entry in replys] 
    
        return list_result


    # def get_specifications(self,instance):





class ProductDetailSerializer1(serializers.ModelSerializer):
    old_price = serializers.SerializerMethodField(method_name='get_price')
    new_price = serializers.SerializerMethodField(method_name='get_discounted_price')
    specification = serializers.SerializerMethodField(method_name='get_specification')
    quantity = serializers.SerializerMethodField(method_name='get_quantity')

    #availability = serializers.SerializerMethodField(method_name='available')
    ratings = serializers.SerializerMethodField(method_name='get_ratings')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    images = serializers.SerializerMethodField(method_name='get_images')
    imagez = serializers.SerializerMethodField(method_name='get_imagez')
    question_answers = serializers.SerializerMethodField(method_name='get_comments')
    class Meta:
        model = Product
        fields = ('id','title','description','brand','quantity','key_features','old_price','new_price','specification','ratings','reviews','question_answers','images','imagez')

    def get_price(self,instance):
        p_price = 0

        try:
            product_price = ProductPrice.objects.filter(product_id = instance.id).last()
        except:
            product_price = None

        if product_price is not None:
            p_price = product_price.price

        else:
            p_price = 0

        float_total = format(p_price, '0.2f')
        return float_total


    def get_discounted_price(self,instance):
        p_price = 0
        p_discount = 0
        discounted_price =0


        try:
            product_price = ProductPrice.objects.filter(product_id=instance.id).last()
        except:
            product_price = None
        try:

            product_discount = discount_product.objects.filter(product_id=instance.id).last()

        except:
            product_discount = None
        

        if product_price is not None:
            p_price = product_price.price

        else:
            p_price = 0


        if product_discount is not None:


            if product_discount.amount:
                p_discount = product_discount.amount
            else:
                p_discount = 0



            #p_discount = product_discount.amount
            current_date = timezone.now().date()
            if product_discount.start_date:
                start_date = product_discount.start_date
            else:
                start_date = current_date

            if product_discount.end_date:
                end_date = product_discount.end_date

            else:
                end_date = current_date
            

            if(current_date >= start_date) and (current_date <= end_date):
                discounted_price = p_price - p_discount

            else:
                discounted_price = p_price

        else:
            discounted_price = p_price


        float_total = format(discounted_price, '0.2f')
        return float_total


    def get_ratings(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/ratings/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values


    def get_reviews(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/reviews_product/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values

    def get_comments(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/comments_product/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values


    # def get_specifications(self,instance):


    #     product_id = instance.id
    #     #site_path = "https://tango99.herokuapp.com/"

    #     url = site_path+ "productdetails/showspec/"+str(product_id)+"/"
    #     values = requests.get(url).json()
    #     return values

    def get_specification(self,instance):

        arr =  {'colors':[],'sizes':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            

            colors = list(p_spec.values_list('color',flat=True).distinct())
            print(colors)
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            print(sizes)
            # units = list(p_spec.values_list('unit',flat=True).distinct())

            # if sizes == [None]:
            #     sizes= []


            # if colors == [None]:
            #     colors = []

            arr =  {'colors':colors,'sizes':sizes}

            return arr

        else:

            return arr


    def get_quantity(self,instance):

        #arr =  {'colors':[],'sizes':[],'units':[]}

        total_sum = 0


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            quantities = list(p_spec.values_list('quantity',flat=True))

            #total_sum = 0
            for i in range(len(quantities)):

                total_sum = total_sum + quantities[i]



            

            return total_sum

        else:

            return total_sum




    def get_images(self,instance):

        images=[]


        try:

            product_images = ProductImage.objects.filter(product_id = instance.id)

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


    def get_imagez(self,instance):
        replys = ProductImage.objects.filter(product_id=instance.id).values()
        list_result = [entry for entry in replys] 
    
        return list_result
# ------------------------- Product Cupon ---------------------------------

class CupponSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Cupons
        fields = "__all__"


# --------------------- Product Discount ---------------------

class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = discount_product
        fields = "__all__"
        #fields=("name", "email")



class ProductImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImpression
        fields = "__all__"
        #fields=("name", "email")


# class WareHouseSerializer(serializers.ModelSerializer):

#     item_quantity = serializers.SerializerMethodField(method_name='get_quantity')
#     class Meta:
#         model = Warehouse
#         fields = ('id','warehouse_name','warehouse_location','item_quantity')


#     def get_




class WarehouseSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name='get_products')
    class Meta:
        model = Warehouse
        fields = ('id','warehouse_name','warehouse_location','products')


    def get_products(self,instance):

        product_data = []

        print("dhuklam")

        try:

            products = WarehouseInfo.objects.filter(warehouse_id=instance.id)

        except:

            products = None

        print("warehouse info")
        print(products)  


        if products:

            product_ids = list(products.values_list('product_id',flat=True).distinct())


            print("product ids")

            print(product_ids)

            if len(product_ids) > 0:

                print("dhuklam loop er bhitore")


                for i in range(len(product_ids)):

                    print("yeeeesssss")


                    try:

                        specific_product = Product.objects.get(id = product_ids[i])

                    except:

                        specific_product = None 

                    print(specific_product)


                    if specific_product:

                        product_id = specific_product.id
                        print("productid")
                        print(product_id)

                        product_title = specific_product.title
                        print(product_title)

                        #Finding out the product price 

                        try:

                            product_price = ProductPrice.objects.filter(product_id=product_id).last()
                        except:
                            product_price = None

                        if product_price is not None:
                            old_price = product_price.price
                            p_price = product_price.price
                            #unit_price = p_price
                        else:
                            old_price = 0
                            p_price = 0
                            #unit_price = p_price

                        #Fetching the product discount
                        try:
                            product_discount = discount_product.objects.filter(product_id=product_id).last()
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
                              
                                p_price = p_price - p_discount

                            else:
                                #total_discount=0
                                #total_price = (p_price * quantity) - total_discount
                                p_price = p_price
                        else:

                            p_price

                        print("price")
                        print(p_price)
                        print(old_price)

                        specifications = [] 


                        try:


                            spec_prods = WarehouseInfo.objects.filter(warehouse_id=instance.id,product_id=product_id)


                        except:

                            spec_prods = None

                        print(spec_prods)

                        if spec_prods:

                            #Fetch the specification ids

                            specs_ids = list(spec_prods.values_list('specification_id',flat=True))


                            spec_quantities = list(spec_prods.values_list('quantity',flat=True))

                            total_quantity = sum(spec_quantities)

                            print("-----")
                            print(specs_ids)
                            print("-----")
                            print(spec_quantities)
                            print(total_quantity)

                            


                            for j in range (len(specs_ids)):

                                print("second loop ey dhuklam")

                                try:

                                    specific_spec = ProductSpecification.objects.get(id=specs_ids[j])

                                except:

                                    specific_spec = None 




                                if specific_spec:

                                    color = specific_spec.color
                                    weight = specific_spec.weight
                                    size = specific_spec.size

                                    print("specssss")
                                    print(color)
                                    print(weight)
                                    print(size)


                                else:

                                    color = ""
                                    weight = ""
                                    size = ""


                                spec_data = {"color":color,"size":size,"weight":weight,"quantity":spec_quantities[j]}

                                specifications.append(spec_data)
                            print(specifications)


                        else:

                            total_quantity = 0

                            specifications = []



                        product_datas = {"product_id":product_id,"product_title":product_title,"product_price":p_price,"total_quantity":total_quantity,"specifications":specifications}
                        print(product_datas)

                    else:

                        product_datas = {}


                    product_data.append(product_datas)

                return product_data


            else:

                return product_data


        else:

            return product_data






      

class ShopSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name='get_products')
    class Meta:
        model = Shop
        fields = ('id','shop_name','shop_location','products')

    def get_products(self,instance):

        product_data = []

        print("dhuklam")

        try:

            products = ShopInfo.objects.filter(shop_id=instance.id)

        except:

            products = None

        print("warehouse info")
        print(products)  


        if products:

            product_ids = list(products.values_list('product_id',flat=True).distinct())


            print("product ids")

            print(product_ids)

            if len(product_ids) > 0:

                print("dhuklam loop er bhitore")


                for i in range(len(product_ids)):

                    print("yeeeesssss")


                    try:

                        specific_product = Product.objects.get(id = product_ids[i])

                    except:

                        specific_product = None 

                    print(specific_product)


                    if specific_product:

                        product_id = specific_product.id
                        print("productid")
                        print(product_id)

                        product_title = specific_product.title
                        print(product_title)

                        #Finding out the product price 

                        try:

                            product_price = ProductPrice.objects.filter(product_id=product_id).last()
                        except:
                            product_price = None

                        if product_price is not None:
                            old_price = product_price.price
                            p_price = product_price.price
                            #unit_price = p_price
                        else:
                            old_price = 0
                            p_price = 0
                            #unit_price = p_price

                        #Fetching the product discount
                        try:
                            product_discount = discount_product.objects.filter(product_id=product_id).last()
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
                              
                                p_price = p_price - p_discount

                            else:
                                #total_discount=0
                                #total_price = (p_price * quantity) - total_discount
                                p_price = p_price
                        else:

                            p_price

                        print("price")
                        print(p_price)
                        print(old_price)

                        specifications = [] 


                        try:


                            spec_prods = ShopInfo.objects.filter(shop_id=instance.id,product_id=product_id)


                        except:

                            spec_prods = None

                        

                        if spec_prods:

                            #Fetch the specification ids

                            specs_ids = list(spec_prods.values_list('specification_id',flat=True))


                            spec_quantities = list(spec_prods.values_list('quantity',flat=True))

                            total_quantity = sum(spec_quantities)

          

                            


                            for j in range (len(specs_ids)):

                                print("second loop ey dhuklam")

                                try:

                                    specific_spec = ProductSpecification.objects.get(id=specs_ids[j])

                                except:

                                    specific_spec = None 




                                if specific_spec:

                                    color = specific_spec.color
                                    weight = specific_spec.weight
                                    size = specific_spec.size

                                    print("specssss")
                                    print(color)
                                    print(weight)
                                    print(size)


                                else:

                                    color = ""
                                    weight = ""
                                    size = ""


                                spec_data = {"color":color,"size":size,"weight":weight,"quantity":spec_quantities[j]}

                                specifications.append(spec_data)
                            print(specifications)


                        else:

                            total_quantity = 0

                            specifications = []



                        product_datas = {"product_id":product_id,"product_title":product_title,"product_price":p_price,"total_quantity":total_quantity,"specifications":specifications}
                        print(product_datas)

                    else:

                        product_datas = {}


                    product_data.append(product_datas)

                return product_data


            else:

                return product_data


        else:

            return product_data


class WarehouseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseInfo
        fields = "__all__"
      

class ShopInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopInfo
        fields = "__all__"

class WSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class SSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"



class WarehousePOSSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.SerializerMethodField(method_name='get_warehouse_name')
    warehouse_location = serializers.SerializerMethodField(method_name='get_warehouse_location')

    class Meta:

        model = WarehouseInfo
        fields = ('id','warehouse_id','warehouse_name','warehouse_location','specification_id','quantity')



    def get_warehouse_name(self,instance):

        try:

            warehouse = Warehouse.objects.get(pk=instance.warehouse_id)

        except:

            warehouse = None 


        print("warehouse name")
        print(warehouse)


        if warehouse:

            if warehouse.warehouse_name:

                warehouse_name = warehouse.warehouse_name 

            else:

                warehouse_name = ""


        else:

            warehouse_name = ""


        return warehouse_name



    def get_warehouse_location(self,instance):

        try:

            warehouse = Warehouse.objects.get(id=instance.warehouse_id)

        except:

            warehouse = None 


        if warehouse:

            if warehouse.warehouse_location:

                warehouse_name = warehouse.warehouse_location 

            else:

                warehouse_name = ""


        else:

            warehouse_name = ""


        return warehouse_name




class ShopPOSSerializer(serializers.ModelSerializer):
    shop_name = serializers.SerializerMethodField(method_name='get_shop_name')
    shop_location = serializers.SerializerMethodField(method_name='get_shop_location')

    class Meta:

        model = ShopInfo
        fields = ('id','shop_id','shop_name','shop_location','specification_id','quantity')



    def get_shop_name(self,instance):

        try:

            warehouse = Shop.objects.get(id=instance.shop_id)

        except:

            warehouse = None 

        print("name")
        print(warehouse)


        if warehouse:

            if warehouse.shop_name:

                warehouse_name = warehouse.shop_name 

            else:

                warehouse_name = ""


        else:

            warehouse_name = ""

        
        return warehouse_name



    def get_shop_location(self,instance):

        try:

            warehouse = Shop.objects.get(id=instance.shop_id)

        except:

            warehouse = None 


        if warehouse:

            if warehouse.shop_location:

                warehouse_name = warehouse.shop_location 

            else:

                warehouse_name = ""


        else:

            warehouse_name = ""

        return warehouse_name

   
   
        


class NewWarehouseInfoSerializer(serializers.ModelSerializer):
    previous_quantity = serializers.SerializerMethodField(method_name='get_quantity')
    warehouse_name = serializers.SerializerMethodField(method_name='get_warehouse_name')
    class Meta:
        model = Warehouse
        fields = ('id','previous_quantity','warehouse_name')
    def get_quantity(self,instance):
        previous_quantity= instance.quantity
        return previous_quantity
    def get_warehouse_name (self, instance):
        wh_name = Warehouse.objects.filter(id=instance.warehouse_id)
        return wh_name[0].warehouse_name 
    



class AddBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = "__all__"


class InventoryReportSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(method_name='get_product_name')
    product_brand = serializers.SerializerMethodField(method_name='get_product_brand')
    product_color = serializers.SerializerMethodField(method_name='get_color')
    product_size = serializers.SerializerMethodField(method_name='get_size')
    variant = serializers.SerializerMethodField(method_name='get_variant')
    product_sku = serializers.SerializerMethodField(method_name='get_SKU')
    product_barcode = serializers.SerializerMethodField(method_name='get_barcode')
    warehouse_name = serializers.SerializerMethodField(method_name='get_warehouse_name')
    warehouse_location = serializers.SerializerMethodField(method_name='get_warehouse_location')
    shop_name = serializers.SerializerMethodField(method_name='get_shop_name')
    shop_location = serializers.SerializerMethodField(method_name='get_shop_location')
    quantity = serializers.SerializerMethodField(method_name='get_stock')
    discount = serializers.SerializerMethodField(method_name='get_discount')
    
    class Meta:
        model = inventory_report
        fields = ('product_name','product_brand','product_sku','product_barcode','product_color','product_size','variant','warehouse_name','warehouse_location','shop_name','shop_location','shop_name',"discount",'quantity','product_id','specification_id','debit','credit','requested','date','warehouse_id','shop_id')



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

        total_price = old_price
        float_total = format(total_price, '0.2f')
        float_value= float(float_total)
        return float_value




    def get_SKU(self,instance):



        try:
            delivery_info = ProductCode.objects.get(specification_id=instance.specification_id)

        except:

            delivery_info = None 

        if delivery_info:


            # if delivery_info.manual_SKU:


            #     SKU = delivery_info.manual_SKU


            if delivery_info.SKU:

                SKU = delivery_info.SKU
                SKU = SKU[7:]

            else:

                SKU = "N/A"



        else:

            SKU = "N/A"


        
        return SKU



    def get_barcode(self,instance):



        try:
            delivery_info = ProductCode.objects.get(specification_id=instance.specification_id)

        except:

            delivery_info = None 

        if delivery_info:


            if delivery_info.manual_Barcode:


                barcode = delivery_info.manual_Barcode


            elif delivery_info.Barcode:

                barcode = delivery_info.Barcode

            else:

                barcode = "N/A"



        else:

            barcode = "N/A"


        
        return barcode


    def get_product_name(self,instance):

        # print(instance.product_id)
        # print(instance.specification_id)

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None 

        print("prothom")

        print("dfvhdsuhf",instance.product_id)

        print(product)

        if product:

            if product.title:

                title = product.title

            else:

                title = "N/A"


        else:

            title = "N/A"


        return title





    def get_product_brand(self,instance):

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None 

        print(product)

        if product:

            if product.brand:

                title = product.brand

            else:

                title = "N/A"


        else:

            title = "N/A"


        return title




    def get_color(self,instance):



        try:

            product = ProductSpecification.objects.get(id=instance.specification_id)

        except:

            product = None 

        if product:

            if product.color:

                title = product.color

            else:

                title = "N/A"


        else:

            title = "N/A"


        return title



    def get_size(self,instance):



        try:

            product = ProductSpecification.objects.get(id=instance.specification_id)

        except:

            product = None 

        if product:

            if product.size:

                title = product.size

            else:

                title = "N/A"


        else:

            title = "N/A"


        return title



    def get_variant(self,instance):



        try:

            product = ProductSpecification.objects.get(id=instance.specification_id)

        except:

            product = None 

        if product:

            print(product)

            if product.weight_unit:

                title = product.weight_unit

            else:

                title = "N/A"


        else:

            title = "N/A"


        return title



    def get_warehouse_name(self,instance):



        try:

            product = Warehouse.objects.get(id=instance.warehouse_id)

        except:

            product = None 

        if product:

            if product.warehouse_name:

                title = product.warehouse_name

            else:

                title = "N/A"


        else:

            title = "N/A"


        return title



    def get_warehouse_location(self,instance):



        try:

            product = Warehouse.objects.get(id=instance.warehouse_id)

        except:

            product = None 

        if product:

            if product.warehouse_location:

                title = product.warehouse_location

            else:

                title = "N/A"


        else:

            title = "N/A"


        return title



    def get_shop_name(self,instance):



        try:

            product = Shop.objects.get(id=instance.shop_id)

        except:

            product = None 

        if product:

            if product.shop_name:

                title = product.shop_location

            else:

                title = "N/A"


        else:

            title = "N/A"


        return title



    def get_shop_location(self,instance):



        try:

            product = Shop.objects.get(id=instance.shop_id)

        except:

            product = None 

        if product:

            if product.shop_name:

                title = product.shop_location

            else:

                title = "N/A"


        else:

            title = "N/A"


        return title



    def get_stock(self,instance):

        quantity = 0


        if instance.warehouse_id == -1:

            inventory_id = instance.shop_id

            try:

                shop = ShopInfo.objects.get(shop_id = inventory_id , specification_id=instance.specification_id,product_id=instance.product_id)

            except:

                shop = None 

            if shop:

                quantity = shop.quantity

            else:

                quantity = 0

        else:

            inventory_id = instance.warehouse_id 



            try:

                shop = WarehouseInfo.objects.get(warehouse_id = inventory_id , specification_id=instance.specification_id,product_id=instance.product_id)

            except:

                shop = None 

            if shop:

                quantity = shop.quantity

            else:

                quantity = 0



        return quantity





# class ProductSpecificationSerializer1(serializers.ModelSerializer):


#     new_price = serializers.SerializerMethodField(method_name='get_new_price')
#     old_price = serializers.SerializerMethodField(method_name='get_old_price')
#     discount = serializers.SerializerMethodField(method_name='get_discount')
#     point = serializers.SerializerMethodField(method_name='get_point')
#     delivery_info = serializers.SerializerMethodField(method_name='get_info')
#     price = serializers.SerializerMethodField(method_name='get_price')
#     purchase_price = serializers.SerializerMethodField(method_name='get_purchase_price')
#     SKU = serializers.SerializerMethodField(method_name='get_SKU')
#     barcode = serializers.SerializerMethodField(method_name='get_barcode')
    

#     # discount = serializers.SerializerMethodField(method_name='get_discount')
#     # point = serializers.SerializerMethodField(method_name='get_point')


#     class Meta:
#         model = ProductSpecification
#         fields = ('id','product_id','color','size','weight','unit','weight_unit','warranty','warranty_unit','vat','quantity','seller_quantity','remaining','SKU','barcode','new_price','old_price','purchase_price','price','discount','point','delivery_info','manufacture_date','expire') 


#     def get_SKU(self,instance):



#         try:
#             delivery_info = ProductCode.objects.get(specification_id=instance.id)

#         except:

#             delivery_info = None 

#         if delivery_info:


#             # if delivery_info.manual_SKU:


#             #     SKU = delivery_info.manual_SKU


#             if delivery_info.SKU:

#                 SKU = delivery_info.SKU

#             else:

#                 SKU = "N/A"



#         else:

#             SKU = "N/A"


        
#         return SKU



#     def get_barcode(self,instance):



#         try:
#             delivery_info = ProductCode.objects.get(specification_id=instance.id)

#         except:

#             delivery_info = None 

#         if delivery_info:


#             if delivery_info.manual_Barcode:


#                 barcode = delivery_info.manual_Barcode


#             elif delivery_info.Barcode:

#                 barcode = delivery_info.Barcode

#             else:

#                 barcode = "N/A"



#         else:

#             barcode = "N/A"


        
#         return barcode




#     def get_purchase_price(self,instance):



#         try:
#             delivery_info = ProductPrice.objects.filter(specification_id=instance.id).last()


#         except:

#             delivery_info = None 

#         if delivery_info:


#             if delivery_info.purchase_price:


#                 purchase_price = delivery_info.purchase_price


#             else:

#                 purchase_price = 0



#         else:


#             purchase_price = 0
    

#         # return purchase_price

#         float_total = format(purchase_price, '0.2f')
#         return float_total

      




  



#     def get_info(self,instance):

#         # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
#         # list_result = [entry for entry in details]

#         try:
#             delivery_info = DeliveryInfo.objects.get(specification_id=instance.id)

#         except:

#             delivery_info = None 

#         if delivery_info:

#             delivery_serializer = DeliveryInfoSerializer(delivery_info,many=False)
#             delivery_data = delivery_serializer.data

#         else:

#             delivery_data = {}
        

#         return delivery_data


#     def get_price(self,instance):

#         # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
#         # list_result = [entry for entry in details]

#         try:
#             delivery_info = ProductPrice.objects.filter(specification_id=instance.id).last()

#         except:

#             delivery_info = None 

#         if delivery_info:

#             delivery_serializer = ProductPriceSerializer(delivery_info,many=False)
#             delivery_data = delivery_serializer.data

#         else:

#             delivery_data = {}
        

#         return delivery_data



#     def get_point(self,instance):

#         # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
#         # list_result = [entry for entry in details]

#         try:
#             delivery_info = ProductPoint.objects.filter(specification_id=instance.id).last()

#         except:

#             delivery_info = None 

#         if delivery_info:

#             delivery_serializer = ProductPointSerializer(delivery_info,many=False)
#             delivery_data = delivery_serializer.data

#         else:

#             delivery_data = {}
        

#         return delivery_data


#     def get_new_price(self,instance):

#         new_price = 0
#         discount = 0  


#         try:


#             p_price = ProductPrice.objects.filter(specification_id = instance.id).last()

#         except:

#             p_price = None 


#         if p_price is not None:

#             new_price =p_price.price

#             try:

#                 p_discount = discount_product.objects.filter(specification_id = instance.id).last()

#             except:

#                 p_discount = None


#             if p_discount is not None:



#                 if p_discount.discount_type == "amount":


#                     #Discount


#                     if p_discount.amount:
#                         discount = p_discount.amount
#                     else:
#                         discount = 0

                
#                     current_date = timezone.now().date()
#                     # discount_start_date = p_discount.start_date

#                     if p_discount.end_date:

#                         discount_end_date = p_discount.end_date

#                     else:
#                         discount_end_date = timezone.now().date()

#                     if p_discount.start_date:
#                         discount_start_date = p_discount.start_date

#                     else:
#                         discount_start_date = timezone.now().date()

                            

#                     if (current_date >= discount_start_date) and (current_date <= discount_end_date):

#                         new_price = new_price - discount

#                     else:
#                         discount =0 
#                         new_price = new_price - discount


#                 elif p_discount.discount_type == "percentage":


#                                         #Discount


#                     if p_discount.amount:
#                         discount = p_discount.amount
#                         # print(type(discount))
#                         # print(type(p_price))
#                         discount =(discount * new_price)/100
#                     else:
#                         discount = 0

                
#                     current_date = timezone.now().date()
#                     # discount_start_date = p_discount.start_date

#                     if p_discount.end_date:

#                         discount_end_date = p_discount.end_date

#                     else:
#                         discount_end_date = timezone.now().date()

#                     if p_discount.start_date:
#                         discount_start_date = p_discount.start_date

#                     else:
#                         discount_start_date = timezone.now().date()

                            

#                     if (current_date >= discount_start_date) and (current_date <= discount_end_date):

#                         new_price = new_price - discount

#                     else:
#                         discount =0 
#                         new_price = new_price - discount


#                 else:
#                     discount = 0 
#                     new_price = new_price - discount 

#             else:
#                 discount = 0
#                 new_price = new_price - discount

#         else:

#             new_price = 0
            
#         float_total = format(new_price, '0.2f')
#         return float_total


   



#     def get_old_price(self,instance):



#         old_price = 0 


#         try:


#             p_price = ProductPrice.objects.filter(specification_id = instance.id).last()

#         except:

#             p_price = None 


#         if p_price is not None:

#             old_price =p_price.price

#         else:
#             old_price = 0


#         float_total = format(old_price, '0.2f')
#         return float_total


#     def get_discount(self,instance):


#         try:
#             delivery_info = discount_product.objects.filter(specification_id=instance.id).last()

#         except:

#             delivery_info = None 

#         if delivery_info:

#             delivery_serializer = ProductDiscountSerializer(delivery_info,many=False)
#             delivery_data = delivery_serializer.data

#         else:

#             delivery_data = {}
        

#         return delivery_data





class SellerSpecificationSerializer(serializers.ModelSerializer):


    new_price = serializers.SerializerMethodField(method_name='get_new_price')
    old_price = serializers.SerializerMethodField(method_name='get_old_price')
    discount = serializers.SerializerMethodField(method_name='get_discount')
    point = serializers.SerializerMethodField(method_name='get_point')
    delivery_info = serializers.SerializerMethodField(method_name='get_info')
    price = serializers.SerializerMethodField(method_name='get_price')
    purchase_price = serializers.SerializerMethodField(method_name='get_purchase_price')
    SKU = serializers.SerializerMethodField(method_name='get_SKU')
    barcode = serializers.SerializerMethodField(method_name='get_barcode')
    product_name = serializers.SerializerMethodField(method_name='get_product_name')
    product_brand = serializers.SerializerMethodField(method_name='get_product_brand')
    category = serializers.SerializerMethodField(method_name='get_category')
    sub_category = serializers.SerializerMethodField(method_name='get_sub_category')
    sub_sub_category = serializers.SerializerMethodField(method_name='get_sub_sub_category')
    description = serializers.SerializerMethodField(method_name='get_description')
    key_features = serializers.SerializerMethodField(method_name='get_key_features')
    origin = serializers.SerializerMethodField(method_name='get_origin')
    shipping_country = serializers.SerializerMethodField(method_name='get_shipping_country')
    images = serializers.SerializerMethodField(method_name='get_images')



    

    # discount = serializers.SerializerMethodField(method_name='get_discount')
    # point = serializers.SerializerMethodField(method_name='get_point')


    class Meta:
        model = ProductSpecification
        fields = ('id','product_id','category','sub_category','sub_sub_category','description','key_features','origin','shipping_country','color','size','weight','unit','weight_unit','warranty','warranty_unit','vat','quantity','seller_quantity','remaining','SKU','barcode','new_price','old_price','purchase_price','price','discount','point','delivery_info','manufacture_date','expire','product_name','product_brand','admin_status','images') 


    def get_category(self,instance):

        category = ""

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None 

        if product:

            if product.category_id:

                category_id = product.category_id

                try:
                    prod_cat = Category.objects.get(id=category_id)

                except:
                    prod_cat = None 

                if prod_cat:

                    category = prod_cat.title 

                else:
                    category = ""



            else:

                category = ""

        else:

            category = ""


        return category


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



    def get_sub_category(self,instance):

        category = ""

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None 

        if product:

            if product.sub_category_id:

                category_id = product.sub_category_id

                try:
                    prod_cat = Sub_Category.objects.get(id=category_id)

                except:
                    prod_cat = None 

                if prod_cat:

                    category = prod_cat.title 

                else:
                    category = ""



            else:

                category = ""

        else:

            category = ""


        return category



    def get_sub_sub_category(self,instance):

        category = ""

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None 

        if product:

            if product.sub_sub_category_id:

                category_id = product.sub_sub_category_id

                try:
                    prod_cat = Sub_Sub_Category.objects.get(id=category_id)

                except:
                    prod_cat = None 

                if prod_cat:

                    category = prod_cat.title 

                else:
                    category = ""



            else:

                category = ""

        else:

            category = ""


        return category


    def get_description(self,instance):

        product_name = ""

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None 

        if product:

            if product.description:

                product_name = product.description

            else:

                product_name = ""

        else:

            product_name = ""


        return product_name


    def get_key_features(self,instance):

        product_name = []

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None 

        if product:

            if product.key_features:

                product_name = product.key_features

            else:

                product_name = []

        else:

            product_name = []


        return product_name



    def get_origin(self,instance):

        product_name = ""

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None 

        if product:

            if product.origin:

                product_name = product.origin

            else:

                product_name = ""

        else:

            product_name = ""


        return product_name






    def get_shipping_country(self,instance):

        product_name = ""

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None 

        if product:

            if product.shipping_country:

                product_name = product.shipping_country

            else:

                product_name = ""

        else:

            product_name = ""


        return product_name



    def get_product_brand(self,instance):

        product_name = ""

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None 

        if product:

            if product.brand:

                product_name = product.brand

            else:

                product_name = ""

        else:

            product_name = ""


        return product_name




    def get_product_name(self,instance):

        product_name = ""

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None 

        if product:

            if product.title:

                product_name = product.title

            else:

                product_name = ""

        else:

            product_name = ""


        return product_name








    def get_SKU(self,instance):



        try:
            delivery_info = ProductCode.objects.get(specification_id=instance.id)

        except:

            delivery_info = None 

        if delivery_info:


            # if delivery_info.manual_SKU:


            #     SKU = delivery_info.manual_SKU


            if delivery_info.SKU:

                SKU = delivery_info.SKU

            else:

                SKU = "N/A"



        else:

            SKU = "N/A"


        
        return SKU



    def get_barcode(self,instance):



        try:
            delivery_info = ProductCode.objects.get(specification_id=instance.id)

        except:

            delivery_info = None 

        if delivery_info:


            if delivery_info.manual_Barcode:


                barcode = delivery_info.manual_Barcode


            elif delivery_info.Barcode:

                barcode = delivery_info.Barcode

            else:

                barcode = "N/A"



        else:

            barcode = "N/A"


        
        return barcode




    def get_purchase_price(self,instance):



        try:
            delivery_info = ProductPrice.objects.filter(specification_id=instance.id).last()


        except:

            delivery_info = None 

        if delivery_info:


            if delivery_info.purchase_price:


                purchase_price = delivery_info.purchase_price


            else:

                purchase_price = 0



        else:


            purchase_price = 0
    

        # return purchase_price

        float_total = format(purchase_price, '0.2f')
        return float_total

      




  



    def get_info(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = DeliveryInfo.objects.get(specification_id=instance.id)

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = DeliveryInfoSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data


    def get_price(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = ProductPrice.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductPriceSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data



    def get_point(self,instance):

        # details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        # list_result = [entry for entry in details]

        try:
            delivery_info = ProductPoint.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductPointSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data


    def get_new_price(self,instance):

        new_price = 0
        discount = 0  


        try:


            p_price = ProductPrice.objects.filter(specification_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            new_price =p_price.price

            try:

                p_discount = discount_product.objects.filter(specification_id = instance.id).last()

            except:

                p_discount = None


            if p_discount is not None:



                if p_discount.discount_type == "amount":


                    #Discount


                    if p_discount.amount:
                        discount = p_discount.amount
                    else:
                        discount = 0

                
                    current_date = timezone.now().date()
                    # discount_start_date = p_discount.start_date

                    if p_discount.end_date:

                        discount_end_date = p_discount.end_date

                    else:
                        discount_end_date = timezone.now().date()

                    if p_discount.start_date:
                        discount_start_date = p_discount.start_date

                    else:
                        discount_start_date = timezone.now().date()

                            

                    if (current_date >= discount_start_date) and (current_date <= discount_end_date):

                        new_price = new_price - discount

                    else:
                        discount =0 
                        new_price = new_price - discount


                elif p_discount.discount_type == "percentage":


                                        #Discount


                    if p_discount.amount:
                        discount = p_discount.amount
                        # print(type(discount))
                        # print(type(p_price))
                        discount =(discount * new_price)/100
                    else:
                        discount = 0

                
                    current_date = timezone.now().date()
                    # discount_start_date = p_discount.start_date

                    if p_discount.end_date:

                        discount_end_date = p_discount.end_date

                    else:
                        discount_end_date = timezone.now().date()

                    if p_discount.start_date:
                        discount_start_date = p_discount.start_date

                    else:
                        discount_start_date = timezone.now().date()

                            

                    if (current_date >= discount_start_date) and (current_date <= discount_end_date):

                        new_price = new_price - discount

                    else:
                        discount =0 
                        new_price = new_price - discount


                else:
                    discount = 0 
                    new_price = new_price - discount 

            else:
                discount = 0
                new_price = new_price - discount

        else:

            new_price = 0
            
        float_total = format(new_price, '0.2f')
        return float_total


   



    def get_old_price(self,instance):



        old_price = 0 


        try:


            p_price = ProductPrice.objects.filter(specification_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            old_price =p_price.price

        else:
            old_price = 0


        float_total = format(old_price, '0.2f')
        return float_total


    def get_discount(self,instance):


        try:
            delivery_info = discount_product.objects.filter(specification_id=instance.id).last()

        except:

            delivery_info = None 

        if delivery_info:

            delivery_serializer = ProductDiscountSerializer(delivery_info,many=False)
            delivery_data = delivery_serializer.data

        else:

            delivery_data = {}
        

        return delivery_data
    

class UserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User()
        fields = ('id','pwd','role')

        
class TerminalSerializer(serializers.ModelSerializer):

    users = serializers.SerializerMethodField(method_name='get_users')


    class Meta:

        model = Terminal
        fields = ('id','terminal_name','warehouse_id','shop_id','site_id','API_key','date_creation','admin_id','is_active','users')

    
    def get_users(self,instance):

        users = []

        try:
            terminal_users = TerminalUsers.objects.filter(terminal_id = instance.id)

        except:
            terminal_users = None 

        if terminal_users:

            user_ids = list(terminal_users.values_list('user_id',flat=True).distinct())
            statuses = list(terminal_users.values_list('is_active',flat=True))

           
            
            for j in range(len(user_ids)):

                status = statuses[j]

               

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
                    
                    

                    user_data = {"id":specific_user.id,"email":email,"password":pwd,"role":role,"phone_number":phone_number,"username":username,"is_active":status}
                    users.append(user_data)
                else:
                    pass

        
        else:
            pass

        return users

class MotherCodeCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCode
        fields = "__all__"


class MotherSpecificationCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = "__all__"


class MotherDeliveryInfoCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInfo
        fields = "__all__"

class MaxMinSerializer(serializers.ModelSerializer):


    class Meta:

        model = SpecificationPrice
        fields = ('id','status','quantity','selling_price','mrp','is_active','specification_id')


class MaxMinSerializer1(serializers.ModelSerializer):

    

    class Meta:

        model = SpecificationPrice
        fields = "__all__"

class ChildSpecificationPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherSpecificationPrice
        fields = "__all__"

class MotherProductSerailizer(serializers.ModelSerializer):


    class Meta:

        model = Product
        fields = "__all__"


class MotherCompanyInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyInfo
        fields = ('name','site_identification','domain','backend_domain')


class MotherProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id','category_id','sub_category_id','sub_sub_category_id','title','brand','description','key_features','is_group','origin','shipping_country','mother_status')

class MotherProductCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCode
        fields = "__all__"

class MotherProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = "__all__"



class MotherSpecificationSerializer(serializers.ModelSerializer):
    #hexcolor = serializers.SerializerMethodField(method_name='get_color')
    site_id = serializers.SerializerMethodField(method_name='get_site_id')
    product_data = serializers.SerializerMethodField(method_name='get_product_info')
    category_data = serializers.SerializerMethodField(method_name='get_category_info')
    product_code = serializers.SerializerMethodField(method_name='get_code_info')
    product_images = serializers.SerializerMethodField(method_name='get_images')
    delivery_info = serializers.SerializerMethodField(method_name='get_delivery_info')
    max_min = serializers.SerializerMethodField(method_name='get_max_min_info')
    class Meta:
        model = ProductSpecification
        fields = ('id','product_id','size','unit','weight','color','warranty','warranty_unit','vat','weight_unit','manufacture_date','expire','shared','mother_status','site_id','product_data','category_data','product_code','product_images','delivery_info','max_min')

    def get_site_id(self,instance):
        company_data = {}
        try:
            company= CompanyInfo.objects.all()
        except:
            company = None 

        if company:
            company = company[0]
            company_serializer = MotherCompanyInfoSerializer(company,many=False)
            company_data = company_serializer.data
        else:
            company_data = []

        return company_data


    def get_product_info(self,instance):
        product_data = {}
        try:
            product= Product.objects.get(id=instance.product_id)
        except:
            product = None 

        if product:
            
            product_serializer = MotherProductSerializer(product,many=False)
            product_data = product_serializer.data
        else:
            product_data = {}

        return product_data


    def get_category_info(self,instance):

        try:
            product = Product.objects.get(id=instance.product_id)
        except:
            product = None 

        if product:
            category_id = product.category_id
            sub_category_id = product.sub_category_id
            sub_sub_category_id = product.sub_sub_category_id
        else:
            category_id = -1 
            sub_category_id = -1 
            sub_sub_category_id= -1 

        try:
            cat = Category.objects.get(id=category_id)
        except:
            cat = None 

        if cat:
            category = cat.title

        else:
            category = ""

        try:
            subcat = Sub_Category.objects.get(id=sub_category_id)
        except:
            subcat = None 

        if subcat:
            sub_category = subcat.title

        else:
            sub_category = ""

        try:
            subsubcat = Sub_Sub_Category.objects.get(id = sub_sub_category_id)
        except:
            subsubcat = None 

        if subsubcat:
            sub_sub_category = subsubcat.title

        else:
            sub_sub_category = ""

        cat_data = {"category":category,"sub_category":sub_category,"sub_sub_category":sub_sub_category}

        return cat_data


    def get_code_info(self,instance):
        product_data = {}
        try:
            product= ProductCode.objects.filter(specification_id=instance.id).last()
        except:
            product = None 

        if product:
            
            product_serializer = MotherProductCodeSerializer(product,many=False)
            product_data = product_serializer.data
        else:
            product_data = {}

        return product_data


    def get_images(self,instance):

        images = []
        try:
            product= ProductImage.objects.filter(product_id=instance.product_id)
        except:
            product = None 

        if product:
            
            product_serializer = MotherProductImageSerializer(product,many=True)
            product_data = product_serializer.data
        else:
            product_data = []

        return product_data


    def get_delivery_info(self,instance):
        product_data = {}
        try:
            product= DeliveryInfo.objects.filter(specification_id=instance.id).last()
        except:
            product = None 

        if product:
            
            product_serializer = DeliveryInfoSerializer(product,many=False)
            product_data = product_serializer.data
        else:
            product_data = {}

        return product_data


    def get_max_min_info(self,instance):

        try:
            product_spec = SpecificationPrice.objects.filter(specification_id = instance.id)
        except:
            product_spec = None

        if product_spec:
            product_serializer  = MaxMinSerializer(product_spec,many=True)
            product_data = product_serializer.data

        else:
            product_data = []

        return product_data




class ChildProductCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class MotherProductImageCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"









class OwnSpecificationSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField(method_name='get_product_info')
    category_data = serializers.SerializerMethodField(method_name='get_category_info')
    product_code = serializers.SerializerMethodField(method_name='get_code_info')
    product_images = serializers.SerializerMethodField(method_name='get_images')
    delivery_info = serializers.SerializerMethodField(method_name='get_delivery_info')
    class Meta:
        model = ProductSpecification
        fields = ('id','product_id','size','unit','weight','color','warranty','warranty_unit','vat','weight_unit','manufacture_date','expire','shared','mother_status','product_data','category_data','product_code','product_images','delivery_info')


    def get_product_info(self,instance):
        product_data = {}
        try:
            product= Product.objects.get(id=instance.product_id)
        except:
            product = None 

        if product:
            
            product_serializer = MotherProductSerializer(product,many=False)
            product_data = product_serializer.data
        else:
            product_data = {}

        return product_data


    def get_category_info(self,instance):

        try:
            product = Product.objects.get(id=instance.product_id)
        except:
            product = None 

        if product:
            category_id = product.category_id
            sub_category_id = product.sub_category_id
            sub_sub_category_id = product.sub_sub_category_id
        else:
            category_id = -1 
            sub_category_id = -1 
            sub_sub_category_id= -1 

        try:
            cat = Category.objects.get(id=category_id)
        except:
            cat = None 

        if cat:
            category = cat.title

        else:
            category = ""

        try:
            subcat = Sub_Category.objects.get(id=sub_category_id)
        except:
            subcat = None 

        if subcat:
            sub_category = subcat.title

        else:
            sub_category = ""

        try:
            subsubcat = Sub_Sub_Category.objects.get(id = sub_sub_category_id)
        except:
            subsubcat = None 

        if subsubcat:
            sub_sub_category = subsubcat.title

        else:
            sub_sub_category = ""

        cat_data = {"category":category,"sub_category":sub_category,"sub_sub_category":sub_sub_category}

        return cat_data


    def get_code_info(self,instance):
        product_data = {}
        try:
            product= ProductCode.objects.filter(specification_id=instance.id).last()
        except:
            product = None 

        if product:
            
            product_serializer = MotherProductCodeSerializer(product,many=False)
            product_data = product_serializer.data
        else:
            product_data = {}

        return product_data


    def get_images(self,instance):

        images = []
        try:
            product= ProductImage.objects.filter(product_id=instance.product_id)
        except:
            product = None 

        if product:
            
            product_serializer = MotherProductImageSerializer(product,many=True)
            product_data = product_serializer.data
        else:
            product_data = []

        return product_data


    def get_delivery_info(self,instance):
        product_data = {}
        try:
            product= DeliveryInfo.objects.filter(specification_id=instance.id).last()
        except:
            product = None 

        if product:
            
            product_serializer = DeliveryInfoSerializer(product,many=False)
            product_data = product_serializer.data
        else:
            product_data = {}

        return product_data








        





