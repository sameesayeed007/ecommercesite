import json
import serpy
from rest_framework import serializers
#from user_profile.models import User
from Intense.models import (
    Category,Sub_Category,Sub_Sub_Category,Product , Variation ,GroupProduct,Comment,CommentReply,Reviews,User,
     Product, Variation , GroupProduct,ProductImage,User,
     ProductPrice,ProductCode,discount_product,ProductCode,ProductSpecification,ProductPoint,Inventory_Price
)
from drf_extra_fields.fields import Base64ImageField
from django.db.models import Avg
from Product_details.serializers import ProductSpecificationSerializer1,ProductSpecificationSerializer5
from Product_category.serializers import CatSerializer,SubCatSerializer,SubSubCatSerializer


from rest_framework import serializers
from rest_framework import fields
from django.utils import timezone
from django.conf import settings
from django.forms.models import model_to_dict
import requests



host_prefix = "https://"
host_name = host_prefix+settings.ALLOWED_HOSTS[0]

# host_prefix = "http://"
# host_name = host_prefix+settings.ALLOWED_HOSTS[0]+":8080"

# host_prefix = "https://"
# host_name = host_prefix+settings.ALLOWED_HOSTS[0]


#site_path = "http://128.199.114.154:8080/"
site_path = "https://tes.com.bd/"
#site_path = "https://tango99.herokuapp.com/"
#site_path = "http://127.0.0.1:8000/"

#site_path = "http://128.199.66.61:8080/"

# site_path = "http://128.199.66.61:8080/"
# site_path = "https://tes.com.bd/"


#------------------------ product---------------------------

class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = [
            "id",
            "title",
            "price",
        ]


# class ProductSerializer(serializers.ModelSerializer):
#     seller=serializers.SerializerMethodField(method_name='get_seller')



#     class Meta:
#         model = Product
#         fields=[
#             'id',
#             'seller',
#             'category_id',
#             'title',
#             'brand',
#             'image',
#             'description',
#             'quantity',
#             'properties',
#             'is_deleted',
#             "key_features" ,
            
#         ]
 
#     def get_seller(self, obj):
#         return obj.seller
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory_Price
        fields = "__all__"


class ProductCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCode
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    new_price = serializers.SerializerMethodField(method_name='get_new_price')
    old_price = serializers.SerializerMethodField(method_name='get_old_price')
    specification = serializers.SerializerMethodField(method_name='get_specification')
    quantity = serializers.SerializerMethodField(method_name='get_quantity')


    #comment_name = serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = Product
        fields = ('id','title','brand','old_price','new_price','images','specification','quantity')

    def get_images(self,instance):
        try:

            replys = ProductImage.objects.filter(product_id=instance.id).values()

        except:
            replys = None

        if replys:
            list_result = [entry for entry in replys] 
            print(list_result)

        else:
            list_result = []
    
        return list_result


    def get_old_price(self,instance):

        old_price = 0 


        try:


            p_price = ProductPrice.objects.filter(product_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            old_price =p_price.price

        else:
            old_price = 0


        float_total = format(old_price, '0.2f')
        return float_total



    def get_new_price(self,instance):

        new_price = 0
        discount = 0  


        try:


            p_price = ProductPrice.objects.filter(product_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            new_price =p_price.price

            try:

                p_discount = discount_product.objects.filter(product_id = instance.id).last()

            except:

                p_discount = None


            if p_discount is not None:


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

            else:
                discount = 0
                new_price = new_price - discount




        else:

            new_price = 0
            


        float_total = format(new_price, '0.2f')
        return float_total


    def get_specification(self,instance):

        arr =  {'colors':[],'sizes':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            colors = list(p_spec.values_list('color',flat=True).distinct())
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            #units = list(p_spec.values_list('unit',flat=True).distinct())
            # colors.remove(None)
            # sizes.remove(None)

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



class ProductSerializer1(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    new_price = serializers.SerializerMethodField(method_name='get_new_price')
    old_price = serializers.SerializerMethodField(method_name='get_old_price')
    #specification = serializers.SerializerMethodField(method_name='get_specification')
    #quantity = serializers.SerializerMethodField(method_name='get_quantity')


    #comment_name = serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = Product
        fields = ('id','title','brand','old_price','new_price','images')

    def get_images(self,instance):
        try:

            replys = ProductImage.objects.filter(product_id=instance.id).values()

        except:
            replys = None

        if replys:
            list_result = [entry for entry in replys] 
            print(list_result)

        else:
            list_result = []
    
        return list_result


    def get_old_price(self,instance):



        new_price = 0
    

        product_id = instance.id

        try:
            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            spec_ids = list(p_spec.values_list('id',flat=True).distinct())

            new_prices = []

            old_prices = []

            for i in range(len(spec_ids)):

                try:

                    specz = ProductSpecification.objects.get(id = spec_ids[i])

                except:

                    specz = None 

                if specz:

                    specz_serializer = ProductSpecificationSerializer1(specz,many=False)

                    specz_data = specz_serializer.data

                    price_value = specz_data["new_price"]

                    old_price_value = specz_data["old_price"]

                    new_prices.append(float(price_value))
                    old_prices.append(float(old_price_value))



            print(new_prices)
            print(old_prices)


            new_price = min(new_prices)
            min_index = new_prices.index(min(new_prices))
            old_price = old_prices[min_index]


        else:
            old_price = 0
        


        float_total = format(old_price, '0.2f')
        return float_total






    # def get_new_price(self,instance):

    #     new_price = 0
    #     discount = 0  


    #     try:


    #         p_price = ProductPrice.objects.filter(product_id = instance.id).last()

    #     except:

    #         p_price = None 


    #     if p_price is not None:

    #         new_price =p_price.price

    #         try:

    #             p_discount = discount_product.objects.filter(product_id = instance.id).last()

    #         except:

    #             p_discount = None


    #         if p_discount is not None:


    #             if p_discount.amount:
    #                 discount = p_discount.amount
    #             else:
    #                 discount = 0

                
    #             current_date = timezone.now().date()
    #             # discount_start_date = p_discount.start_date

    #             if p_discount.end_date:

    #                 discount_end_date = p_discount.end_date

    #             else:
    #                 discount_end_date = timezone.now().date()

    #             if p_discount.start_date:
    #                 discount_start_date = p_discount.start_date

    #             else:
    #                 discount_start_date = timezone.now().date()

                

                

    #             if (current_date >= discount_start_date) and (current_date <= discount_end_date):

    #                 new_price = new_price - discount

    #             else:
    #                 discount =0 
    #                 new_price = new_price - discount

    #         else:
    #             discount = 0
    #             new_price = new_price - discount




    #     else:

    #         new_price = 0
            


    #     float_total = format(new_price, '0.2f')
    #     return float_total


    def get_new_price(self,instance):

        new_price = 0
        discount = 0  

        product_id = instance.id

        try:
            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            spec_ids = list(p_spec.values_list('id',flat=True).distinct())

            new_prices = []

            for i in range(len(spec_ids)):

                try:

                    specz = ProductSpecification.objects.get(id = spec_ids[i])

                except:

                    specz = None 

                if specz:

                    specz_serializer = ProductSpecificationSerializer1(specz,many=False)

                    specz_data = specz_serializer.data

                    price_value = specz_data["new_price"]

                    new_prices.append(float(price_value))



            print(new_prices)


            new_price = min(new_prices)


        else:
            new_price = 0
        


        float_total = format(new_price, '0.2f')
        return float_total


    def get_specification(self,instance):

        arr =  {'colors':[],'sizes':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            colors = list(p_spec.values_list('color',flat=True).distinct())
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            #units = list(p_spec.values_list('unit',flat=True).distinct())
            # colors.remove(None)
            # sizes.remove(None)

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

class NewProductSerializer1(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    # new_price = serializers.SerializerMethodField(method_name='get_new_price')
    # old_price = serializers.SerializerMethodField(method_name='get_old_price')
    #specification = serializers.SerializerMethodField(method_name='get_specification')
    #quantity = serializers.SerializerMethodField(method_name='get_quantity')


    #comment_name = serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = Product
        #fields = ('id','title','brand','old_price','new_price','images')
        fields = ('id','title','brand','images','new_price','old_price')

    def get_images(self,instance):
        
        product_images = ProductImage.objects.filter(product_id=instance.id).values()

        if product_images.exists():
            return [product_images[0]]
        else:
           return  []



    # def get_old_price(self,instance):



    #     new_price = 0
    

    #     product_id = instance.id

    #     try:
    #         p_spec = ProductSpecification.objects.filter(product_id = instance.id)

    #     except:

    #         p_spec = None 


    #     if p_spec:

    #         spec_ids = list(p_spec.values_list('id',flat=True).distinct())

    #         new_prices = []

    #         old_prices = []

    #         for i in range(len(spec_ids)):

    #             try:

    #                 specz = ProductSpecification.objects.get(id = spec_ids[i])

    #             except:

    #                 specz = None 

    #             if specz:

    #                 specz_serializer = ProductSpecificationSerializer1(specz,many=False)

    #                 specz_data = specz_serializer.data

    #                 price_value = specz_data["new_price"]

    #                 old_price_value = specz_data["old_price"]

    #                 new_prices.append(float(price_value))
    #                 old_prices.append(float(old_price_value))



    #         print(new_prices)
    #         print(old_prices)


    #         new_price = min(new_prices)
    #         min_index = new_prices.index(min(new_prices))
    #         old_price = old_prices[min_index]


    #     else:
    #         old_price = 0
        


    #     float_total = format(old_price, '0.2f')
    #     return float_total



    # def get_new_price(self,instance):

    #     new_price = 0
    #     discount = 0  

    #     product_id = instance.id

    #     try:
    #         p_spec = ProductSpecification.objects.filter(product_id = instance.id)

    #     except:

    #         p_spec = None 


    #     if p_spec:

    #         spec_ids = list(p_spec.values_list('id',flat=True).distinct())

    #         new_prices = []

    #         for i in range(len(spec_ids)):

    #             try:

    #                 specz = ProductSpecification.objects.get(id = spec_ids[i])

    #             except:

    #                 specz = None 

    #             if specz:

    #                 specz_serializer = ProductSpecificationSerializer1(specz,many=False)

    #                 specz_data = specz_serializer.data

    #                 price_value = specz_data["new_price"]

    #                 new_prices.append(float(price_value))



    #         print(new_prices)


    #         new_price = min(new_prices)


    #     else:
    #         new_price = 0
        


    #     float_total = format(new_price, '0.2f')
        # return float_total


    # def get_specification(self,instance):

    #     arr =  {'colors':[],'sizes':[]}


        
    #     try:


    #         p_spec = ProductSpecification.objects.filter(product_id = instance.id)

    #     except:

    #         p_spec = None 


    #     if p_spec is not None:

    #         colors = list(p_spec.values_list('color',flat=True).distinct())
    #         sizes = list(p_spec.values_list('size',flat=True).distinct())
    #         #units = list(p_spec.values_list('unit',flat=True).distinct())
    #         # colors.remove(None)
    #         # sizes.remove(None)

    #         arr =  {'colors':colors,'sizes':sizes}

    #         return arr

    #     else:

    #         return arr


    # def get_quantity(self,instance):

    #     #arr =  {'colors':[],'sizes':[],'units':[]}

    #     total_sum = 0


        
    #     try:


    #         p_spec = ProductSpecification.objects.filter(product_id = instance.id)

    #     except:

    #         p_spec = None 


    #     if p_spec is not None:

    #         quantities = list(p_spec.values_list('quantity',flat=True))

    #         #total_sum = 0
    #         for i in range(len(quantities)):

    #             total_sum = total_sum + quantities[i]



            

    #         return total_sum

    #     else:

    #         return total_sum



class ProductAdminSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    purchase_price = serializers.SerializerMethodField(method_name='get_purchase_price')
    new_price = serializers.SerializerMethodField(method_name='get_new_price')
    old_price = serializers.SerializerMethodField(method_name='get_old_price')
    specification = serializers.SerializerMethodField(method_name='get_specification')
    quantity = serializers.SerializerMethodField(method_name='get_quantity')
    category = serializers.SerializerMethodField(method_name='get_cat')
    sub_category = serializers.SerializerMethodField(method_name='get_sub_cat')
    sub_sub_category = serializers.SerializerMethodField(method_name='get_sub_sub_cat')
    discount_type = serializers.SerializerMethodField(method_name='get_discount_type')
    discount_start_date = serializers.SerializerMethodField(method_name='get_discount_start_date')
    discount_end_date = serializers.SerializerMethodField(method_name='get_discount_end_date')
    discount_amount = serializers.SerializerMethodField(method_name='get_discount_amount')
    point = serializers.SerializerMethodField(method_name='get_point')
    point_start_date = serializers.SerializerMethodField(method_name='get_point_start_date')
    point_end_date = serializers.SerializerMethodField(method_name='get_point_end_date')
    seller_name = serializers.SerializerMethodField(method_name='get_seller_name')




    #comment_name = serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = Product
        fields = ('id','seller_name','product_admin_status','title','brand','date','description','key_features','properties','unit','warranty','origin','shipping_country','purchase_price','old_price','new_price','discount_type','discount_amount','discount_start_date','discount_end_date','point','point_start_date','point_end_date','images','specification','quantity','category','sub_category','sub_sub_category')

    def get_images(self,instance):
        try:

            replys = ProductImage.objects.filter(product_id=instance.id).values()

        except:
            replys = None

        if replys:
            list_result = [entry for entry in replys] 

        else:
            list_result = []
    
        return list_result


    def get_old_price(self,instance):

        old_price = 0 


        try:


            p_price = ProductPrice.objects.filter(product_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            old_price =p_price.price

        else:
            old_price = 0


        float_total = format(old_price, '0.2f')
        return float_total


    def get_purchase_price(self,instance):

        old_price = 0 


        try:


            p_price = ProductPrice.objects.filter(product_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            old_price =p_price.purchase_price

        else:
            old_price = 0


        float_total = format(old_price, '0.2f')
        return float_total



    def get_new_price(self,instance):

        new_price = 0
        discount = 0  


        try:


            p_price = ProductPrice.objects.filter(product_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            new_price =p_price.price

            try:

                p_discount = discount_product.objects.filter(product_id = instance.id).last()

            except:

                p_discount = None


            if p_discount is not None:


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

            else:
                discount = 0
                new_price = new_price - discount




        else:

            new_price = 0
            


        float_total = format(new_price, '0.2f')
        return float_total


    def get_specification(self,instance):

        arr =  {'colors':[],'sizes':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            colors = list(p_spec.values_list('color',flat=True).distinct())
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            #units = list(p_spec.values_list('unit',flat=True).distinct())

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



    def get_cat(self,instance):

        title = ""

        try:

            category = Category.objects.get(id=instance.category_id)

        except:

            category = None


        if category:

            title = category.title


        return title


    def get_sub_cat(self,instance):

        title = ""

        try:

            category = Sub_Category.objects.get(id=instance.sub_category_id)

        except:

            category = None


        if category:

            title = category.title


        return title



    def get_sub_sub_cat(self,instance):

        title = ""

        try:

            category = Sub_Sub_Category.objects.get(id=instance.sub_sub_category_id)

        except:

            category = None


        if category:

            title = category.title


        return title


    def get_discount_type(self,instance):

        discount_type = ""

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_type = discount.discount_type


        return discount_type



    def get_discount_amount(self,instance):

        discount_amount = 0

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_amount = discount.amount


        return discount_amount


    def get_discount_start_date(self,instance):

        discount_start_date = ""

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_start_date = discount.start_date


        return discount_start_date



    def get_discount_end_date(self,instance):

        discount_end_date = ""

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_end_date = discount.end_date


        return discount_end_date


    def get_point(self,instance):

        point_amount = 0

        try:

            point = ProductPoint.objects.filter(product_id=instance.id).last()

        except:

            point = None

            


        if point:

            point_amount = point.point


        return point_amount



    def get_point_start_date(self,instance):

        point_start_date = 0

        try:

            point = ProductPoint.objects.filter(product_id=instance.id).last()

        except:

            point = None

            


        if point:

            point_start_date = point.start_date


        return point_start_date



    def get_point_end_date(self,instance):

        point_end_date = 0

        try:

            point = ProductPoint.objects.filter(product_id=instance.id).last()

        except:

            point = None

            


        if point:

            point_end_date = point.end_date


        return point_end_date


    def get_seller_name(self,instance):

        name = ""

        try:

            username = User.objects.get(id=instance.seller)

        except:

            username = None

            


        if username:

            name = username.username


        return name



# class ProductAdminSerializer1(serializers.ModelSerializer):
#     images = serializers.SerializerMethodField(method_name='get_images')
#     purchase_price = serializers.SerializerMethodField(method_name='get_purchase_price')
#     new_price = serializers.SerializerMethodField(method_name='get_new_price')
#     old_price = serializers.SerializerMethodField(method_name='get_old_price')
#     specification = serializers.SerializerMethodField(method_name='get_specification')
#     quantity = serializers.SerializerMethodField(method_name='get_quantity')
#     category = serializers.SerializerMethodField(method_name='get_cat')
#     sub_category = serializers.SerializerMethodField(method_name='get_sub_cat')
#     sub_sub_category = serializers.SerializerMethodField(method_name='get_sub_sub_cat')
#     discount_type = serializers.SerializerMethodField(method_name='get_discount_type')
#     discount_start_date = serializers.SerializerMethodField(method_name='get_discount_start_date')
#     discount_end_date = serializers.SerializerMethodField(method_name='get_discount_end_date')
#     discount_amount = serializers.SerializerMethodField(method_name='get_discount_amount')
#     point = serializers.SerializerMethodField(method_name='get_point')
#     point_start_date = serializers.SerializerMethodField(method_name='get_point_start_date')
#     point_end_date = serializers.SerializerMethodField(method_name='get_point_end_date')
#     seller_name = serializers.SerializerMethodField(method_name='get_seller_name')
#     specifications = serializers.SerializerMethodField(method_name='get_specifications')
#     seller_email = serializers.SerializerMethodField(method_name='get_seller_email')
#     specific_status = serializers.SerializerMethodField(method_name='get_specific_status')





#     #comment_name = serializers.SerializerMethodField(method_name='get_name')
#     class Meta:
#         model = Product
#         fields = ('id','seller_name','seller_email','product_admin_status','title','brand','date','description','key_features','properties','origin','shipping_country','purchase_price','old_price','new_price','discount_type','discount_amount','discount_start_date','discount_end_date','point','point_start_date','point_end_date','images','specification','quantity','category','sub_category','sub_sub_category','specifications','product_status')







#     def get_specifications(self,instance):

#         try:

#             product = ProductSpecification.objects.filter(product_id=instance.id)


#         except:

#             product = None 


#         if product: 


#             product_serializer = ProductSpecificationSerializer1(product,many=True)

#             product_data = product_serializer.data



#         else:

#             product_data = []



#         return product_data

#     def get_images(self,instance):
#         try:

#             replys = ProductImage.objects.filter(product_id=instance.id).values()

#         except:
#             replys = None

#         if replys:
#             list_result = [entry for entry in replys] 

#         else:
#             list_result = []
    
#         return list_result





#     def get_purchase_price(self,instance):

#         old_price = 0 


#         try:


#             p_price = ProductPrice.objects.filter(product_id = instance.id).last()

#         except:

#             p_price = None 


#         if p_price is not None:

#             old_price =p_price.purchase_price

#         else:
#             old_price = 0


#         float_total = format(old_price, '0.2f')
#         return float_total


#     def get_old_price(self,instance):



#         new_price = 0
    

#         product_id = instance.id

#         try:
#             p_spec = ProductSpecification.objects.filter(product_id = instance.id)

#         except:

#             p_spec = None 


#         if p_spec:

#             spec_ids = list(p_spec.values_list('id',flat=True).distinct())

#             new_prices = []

#             old_prices = []

#             for i in range(len(spec_ids)):

#                 try:

#                     specz = ProductSpecification.objects.get(id = spec_ids[i])

#                 except:

#                     specz = None 

#                 if specz:

#                     specz_serializer = ProductSpecificationSerializer1(specz,many=False)

#                     specz_data = specz_serializer.data

#                     price_value = specz_data["new_price"]

#                     old_price_value = specz_data["old_price"]

#                     new_prices.append(float(price_value))
#                     old_prices.append(float(old_price_value))



#             print(new_prices)
#             print(old_prices)


#             new_price = min(new_prices)
#             min_index = new_prices.index(min(new_prices))
#             old_price = old_prices[min_index]


#         else:
#             old_price = 0
        


#         float_total = format(old_price, '0.2f')
#         return float_total



#     def get_new_price(self,instance):

#         new_price = 0
#         discount = 0  

#         product_id = instance.id

#         try:
#             p_spec = ProductSpecification.objects.filter(product_id = instance.id)

#         except:

#             p_spec = None 


#         if p_spec:

#             spec_ids = list(p_spec.values_list('id',flat=True).distinct())

#             new_prices = []

#             for i in range(len(spec_ids)):

#                 try:

#                     specz = ProductSpecification.objects.get(id = spec_ids[i])

#                 except:

#                     specz = None 

#                 if specz:

#                     specz_serializer = ProductSpecificationSerializer1(specz,many=False)

#                     specz_data = specz_serializer.data

#                     price_value = specz_data["new_price"]

#                     new_prices.append(float(price_value))



#             print(new_prices)


#             new_price = min(new_prices)


#         else:
#             new_price = 0
        


#         float_total = format(new_price, '0.2f')
#         return float_total





#     def get_specification(self,instance):

#         arr =  {'colors':[],'sizes':[]}


        
#         try:


#             p_spec = ProductSpecification.objects.filter(product_id = instance.id)

#         except:

#             p_spec = None 


#         if p_spec is not None:

#             colors = list(p_spec.values_list('color',flat=True).distinct())
#             sizes = list(p_spec.values_list('size',flat=True).distinct())
#             #units = list(p_spec.values_list('unit',flat=True).distinct())

#             arr =  {'colors':colors,'sizes':sizes}

#             return arr

#         else:

#             return arr


#     def get_quantity(self,instance):

#         #arr =  {'colors':[],'sizes':[],'units':[]}

#         total_sum = 0


        
#         try:


#             p_spec = ProductSpecification.objects.filter(product_id = instance.id)

#         except:

#             p_spec = None 


#         if p_spec is not None:

#             quantities = list(p_spec.values_list('quantity',flat=True))

#             #total_sum = 0
#             for i in range(len(quantities)):

#                 total_sum = total_sum + quantities[i]



            

#             return total_sum

#         else:

#             return total_sum



#     def get_cat(self,instance):

#         title = ""

#         try:

#             category = Category.objects.get(id=instance.category_id)

#         except:

#             category = None


#         if category:

#             title = category.title


#         return title


#     def get_sub_cat(self,instance):

#         title = ""

#         try:

#             category = Sub_Category.objects.get(id=instance.sub_category_id)

#         except:

#             category = None


#         if category:

#             title = category.title


#         return title



#     def get_sub_sub_cat(self,instance):

#         title = ""

#         try:

#             category = Sub_Sub_Category.objects.get(id=instance.sub_sub_category_id)

#         except:

#             category = None


#         if category:

#             title = category.title


#         return title


#     def get_discount_type(self,instance):

#         discount_type = ""

#         try:

#             discount = discount_product.objects.filter(product_id=instance.id).last()

#         except:

#             discount = None

            


#         if discount:

#             discount_type = discount.discount_type


#         return discount_type



#     def get_discount_amount(self,instance):

#         discount_amount = 0

#         try:

#             discount = discount_product.objects.filter(product_id=instance.id).last()

#         except:

#             discount = None

            


#         if discount:

#             discount_amount = discount.amount


#         return discount_amount


#     def get_discount_start_date(self,instance):

#         discount_start_date = ""

#         try:

#             discount = discount_product.objects.filter(product_id=instance.id).last()

#         except:

#             discount = None

            


#         if discount:

#             discount_start_date = discount.start_date


#         return discount_start_date



#     def get_discount_end_date(self,instance):

#         discount_end_date = ""

#         try:

#             discount = discount_product.objects.filter(product_id=instance.id).last()

#         except:

#             discount = None

            


#         if discount:

#             discount_end_date = discount.end_date


#         return discount_end_date


#     def get_point(self,instance):

#         point_amount = 0

#         try:

#             point = ProductPoint.objects.filter(product_id=instance.id).last()

#         except:

#             point = None

            


#         if point:

#             point_amount = point.point


#         return point_amount



#     def get_point_start_date(self,instance):

#         point_start_date = 0

#         try:

#             point = ProductPoint.objects.filter(product_id=instance.id).last()

#         except:

#             point = None

            


#         if point:

#             point_start_date = point.start_date


#         return point_start_date



#     def get_point_end_date(self,instance):

#         point_end_date = 0

#         try:

#             point = ProductPoint.objects.filter(product_id=instance.id).last()

#         except:

#             point = None

            


#         if point:

#             point_end_date = point.end_date


#         return point_end_date


#     def get_seller_name(self,instance):

#         name = ""

#         try:

#             username = User.objects.get(id=instance.seller)

#         except:

#             username = None

            


#         if username:

#             name = username.username


#         return name


#     def get_seller_email(self,instance):

#         name = ""

#         try:

#             username = User.objects.get(id=instance.seller)

#         except:

#             username = None

            


#         if username:

#             name = username.email


#         return name


# class ProductAdminSerializer1(serializers.ModelSerializer):
#     images = serializers.SerializerMethodField(method_name='get_images')
#     purchase_price = serializers.SerializerMethodField(method_name='get_purchase_price')
#     new_price = serializers.SerializerMethodField(method_name='get_new_price')
#     old_price = serializers.SerializerMethodField(method_name='get_old_price')
#     specification = serializers.SerializerMethodField(method_name='get_specification')
#     quantity = serializers.SerializerMethodField(method_name='get_quantity')
#     category = serializers.SerializerMethodField(method_name='get_cat')
#     sub_category = serializers.SerializerMethodField(method_name='get_sub_cat')
#     sub_sub_category = serializers.SerializerMethodField(method_name='get_sub_sub_cat')
#     discount_type = serializers.SerializerMethodField(method_name='get_discount_type')
#     discount_start_date = serializers.SerializerMethodField(method_name='get_discount_start_date')
#     discount_end_date = serializers.SerializerMethodField(method_name='get_discount_end_date')
#     discount_amount = serializers.SerializerMethodField(method_name='get_discount_amount')
#     point = serializers.SerializerMethodField(method_name='get_point')
#     point_start_date = serializers.SerializerMethodField(method_name='get_point_start_date')
#     point_end_date = serializers.SerializerMethodField(method_name='get_point_end_date')
#     seller_name = serializers.SerializerMethodField(method_name='get_seller_name')
#     specifications = serializers.SerializerMethodField(method_name='get_specifications')
#     seller_email = serializers.SerializerMethodField(method_name='get_seller_email')
#     specific_status = serializers.SerializerMethodField(method_name='get_specific_status')




#     #comment_name = serializers.SerializerMethodField(method_name='get_name')
#     class Meta:
#         model = Product
#         fields = ('id','seller_name','seller_email', "specific_status" , 'product_admin_status','title','brand','date','description','key_features','properties','origin','shipping_country','purchase_price','old_price','new_price','discount_type','discount_amount','discount_start_date','discount_end_date','point','point_start_date','point_end_date','images','specification','quantity','category','sub_category','sub_sub_category','specifications','product_status')

#     def get_specifications(self,instance):

#         try:

#             product = ProductSpecification.objects.filter(product_id=instance.id)


#         except:

#             product = None 


#         if product: 


#             product_serializer = ProductSpecificationSerializer1(product,many=True)

#             product_data = product_serializer.data



#         else:

#             product_data = []



#         return product_data



#     def get_specific_status(self , instance):
        
#         try:

#             product = ProductSpecification.objects.filter(product_id=instance.id)


#         except:

#             product = None 
           

#         if product : 

#             product_data = "YES"



#         else:

#             product_data = "NO"



#         return product_data


#     def get_images(self,instance):
#         try:

#             replys = ProductImage.objects.filter(product_id=instance.id).values()

#         except:
#             replys = None

#         if replys:
#             list_result = [entry for entry in replys] 

#         else:
#             list_result = []
    
#         return list_result





#     def get_purchase_price(self,instance):

#         old_price = 0 


#         try:


#             p_price = ProductPrice.objects.filter(product_id = instance.id).last()

#         except:

#             p_price = None 


#         if p_price is not None:

#             old_price =p_price.purchase_price

#         else:
#             old_price = 0


#         float_total = format(old_price, '0.2f')
#         return float_total


#     def get_old_price(self,instance):



#         new_price = 0
    

#         product_id = instance.id

#         try:
#             p_spec = ProductSpecification.objects.filter(product_id = instance.id)

#         except:

#             p_spec = None 


#         if p_spec:

#             spec_ids = list(p_spec.values_list('id',flat=True).distinct())

#             new_prices = []

#             old_prices = []

#             for i in range(len(spec_ids)):

#                 try:

#                     specz = ProductSpecification.objects.get(id = spec_ids[i])

#                 except:

#                     specz = None 

#                 if specz:

#                     specz_serializer = ProductSpecificationSerializer1(specz,many=False)

#                     specz_data = specz_serializer.data

#                     price_value = specz_data["new_price"]

#                     old_price_value = specz_data["old_price"]

#                     new_prices.append(float(price_value))
#                     old_prices.append(float(old_price_value))





#             new_price = min(new_prices)
#             min_index = new_prices.index(min(new_prices))
#             old_price = old_prices[min_index]


#         else:
#             old_price = 0
        


#         float_total = format(old_price, '0.2f')
#         return float_total



#     def get_new_price(self,instance):

#         new_price = 0
#         discount = 0  

#         product_id = instance.id

#         try:
#             p_spec = ProductSpecification.objects.filter(product_id = instance.id)

#         except:

#             p_spec = None 


#         if p_spec:

#             spec_ids = list(p_spec.values_list('id',flat=True).distinct())

#             new_prices = []

#             for i in range(len(spec_ids)):

#                 try:

#                     specz = ProductSpecification.objects.get(id = spec_ids[i])

#                 except:

#                     specz = None 

#                 if specz:

#                     specz_serializer = ProductSpecificationSerializer1(specz,many=False)

#                     specz_data = specz_serializer.data

#                     price_value = specz_data["new_price"]

#                     new_prices.append(float(price_value))



#             print(new_prices)


#             new_price = min(new_prices)


#         else:
#             new_price = 0
        


#         float_total = format(new_price, '0.2f')
#         return float_total





#     def get_specification(self,instance):

#         arr =  {'colors':[],'sizes':[]}


        
#         try:


#             p_spec = ProductSpecification.objects.filter(product_id = instance.id)

#         except:

#             p_spec = None 


#         if p_spec is not None:

#             colors = list(p_spec.values_list('color',flat=True).distinct())
#             sizes = list(p_spec.values_list('size',flat=True).distinct())
#             #units = list(p_spec.values_list('unit',flat=True).distinct())

#             arr =  {'colors':colors,'sizes':sizes}

#             return arr

#         else:

#             return arr


#     def get_quantity(self,instance):

#         #arr =  {'colors':[],'sizes':[],'units':[]}

#         total_sum = 0


        
#         try:


#             p_spec = ProductSpecification.objects.filter(product_id = instance.id)

#         except:

#             p_spec = None 


#         if p_spec is not None:

#             quantities = list(p_spec.values_list('quantity',flat=True))

#             #total_sum = 0
#             for i in range(len(quantities)):

#                 total_sum = total_sum + quantities[i]



            

#             return total_sum

#         else:

#             return total_sum



#     def get_cat(self,instance):

#         title = ""

#         try:

#             category = Category.objects.get(id=instance.category_id)

#         except:

#             category = None


#         if category:

#             title = category.title


#         return title


#     def get_sub_cat(self,instance):

#         title = ""

#         try:

#             category = Sub_Category.objects.get(id=instance.sub_category_id)

#         except:

#             category = None


#         if category:

#             title = category.title


#         return title



#     def get_sub_sub_cat(self,instance):

#         title = ""

#         try:

#             category = Sub_Sub_Category.objects.get(id=instance.sub_sub_category_id)

#         except:

#             category = None


#         if category:

#             title = category.title


#         return title


#     def get_discount_type(self,instance):

#         discount_type = ""

#         try:

#             discount = discount_product.objects.filter(product_id=instance.id).last()

#         except:

#             discount = None

            


#         if discount:

#             discount_type = discount.discount_type


#         return discount_type



#     def get_discount_amount(self,instance):

#         discount_amount = 0

#         try:

#             discount = discount_product.objects.filter(product_id=instance.id).last()

#         except:

#             discount = None

            


#         if discount:

#             discount_amount = discount.amount


#         return discount_amount


#     def get_discount_start_date(self,instance):

#         discount_start_date = ""

#         try:

#             discount = discount_product.objects.filter(product_id=instance.id).last()

#         except:

#             discount = None

            


#         if discount:

#             discount_start_date = discount.start_date


#         return discount_start_date



#     def get_discount_end_date(self,instance):

#         discount_end_date = ""

#         try:

#             discount = discount_product.objects.filter(product_id=instance.id).last()

#         except:

#             discount = None

            


#         if discount:

#             discount_end_date = discount.end_date


#         return discount_end_date


#     def get_point(self,instance):

#         point_amount = 0

#         try:

#             point = ProductPoint.objects.filter(product_id=instance.id).last()

#         except:

#             point = None

            


#         if point:

#             point_amount = point.point


#         return point_amount



#     def get_point_start_date(self,instance):

#         point_start_date = 0

#         try:

#             point = ProductPoint.objects.filter(product_id=instance.id).last()

#         except:

#             point = None

            


#         if point:

#             point_start_date = point.start_date


#         return point_start_date



#     def get_point_end_date(self,instance):

#         point_end_date = 0

#         try:

#             point = ProductPoint.objects.filter(product_id=instance.id).last()

#         except:

#             point = None

            


#         if point:

#             point_end_date = point.end_date


#         return point_end_date


#     def get_seller_name(self,instance):

#         name = ""

#         try:

#             username = User.objects.get(id=instance.seller)

#         except:

#             username = None

            


#         if username:

#             name = username.username


#         return name


#     def get_seller_email(self,instance):

#         name = ""

#         try:

#             username = User.objects.get(id=instance.seller)

#         except:

#             username = None

            


#         if username:

#             name = username.email


#         return name



class ProductPOSSerializer1(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    #purchase_price = serializers.SerializerMethodField(method_name='get_purchase_price')
    #new_price = serializers.SerializerMethodField(method_name='get_new_price')
    #old_price = serializers.SerializerMethodField(method_name='get_old_price')
    #specification = serializers.SerializerMethodField(method_name='get_specification')
    #quantity = serializers.SerializerMethodField(method_name='get_quantity')
    category = serializers.SerializerMethodField(method_name='get_cat')
    sub_category = serializers.SerializerMethodField(method_name='get_sub_cat')
    sub_sub_category = serializers.SerializerMethodField(method_name='get_sub_sub_cat')
    # discount_type = serializers.SerializerMethodField(method_name='get_discount_type')
    # discount_start_date = serializers.SerializerMethodField(method_name='get_discount_start_date')
    # discount_end_date = serializers.SerializerMethodField(method_name='get_discount_end_date')
    # discount_amount = serializers.SerializerMethodField(method_name='get_discount_amount')
    # point = serializers.SerializerMethodField(method_name='get_point')
    # point_start_date = serializers.SerializerMethodField(method_name='get_point_start_date')
    # point_end_date = serializers.SerializerMethodField(method_name='get_point_end_date')
    seller_name = serializers.SerializerMethodField(method_name='get_seller_name')
    specifications = serializers.SerializerMethodField(method_name='get_specifications')
    seller_email = serializers.SerializerMethodField(method_name='get_seller_email')
    category_object = serializers.SerializerMethodField(method_name='get_category_object')
    sub_category_object= serializers.SerializerMethodField(method_name='get_sub_category_object')
    sub_sub_category_object= serializers.SerializerMethodField(method_name='get_sub_sub_category_object')





    #comment_name = serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = Product
        fields = ('id','seller','seller_name','seller_email','product_admin_status','product_status','title','brand','date','description','key_features','properties','is_deleted','is_group','origin','shipping_country','images','category_id','sub_category_id','sub_sub_category_id','category','sub_category','sub_sub_category','category_object','sub_category_object','sub_sub_category_object','specifications')

    def get_category_object(self,instance):

        data = {}


        try:

            category = Category.objects.get(id=instance.category_id)

        except:

            category = None


        if category:

            category_serializer = CatSerializer(category,many=False)

            data = category_serializer.data



        return data



    def get_sub_category_object(self,instance):

        data = {}


        try:

            category = Sub_Category.objects.get(id=instance.sub_category_id)

        except:

            category = None


        if category:

            category_serializer = SubCatSerializer(category,many=False)

            data = category_serializer.data



        return data


    def get_sub_sub_category_object(self,instance):

        data = {}


        try:

            category = Sub_Sub_Category.objects.get(id=instance.sub_sub_category_id)

        except:

            category = None


        if category:

            category_serializer = SubSubCatSerializer(category,many=False)

            data = category_serializer.data



        return data



    def get_specifications(self,instance):

        try:

            product = ProductSpecification.objects.filter(product_id=instance.id)


        except:

            product = None 


        if product: 


            product_serializer = ProductSpecificationSerializer5(product,many=True)

            product_data = product_serializer.data



        else:

            product_data = []



        return product_data

    def get_images(self,instance):
        try:

            replys = ProductImage.objects.filter(product_id=instance.id).values()

        except:
            replys = None

        if replys:
            list_result = [entry for entry in replys] 

        else:
            list_result = []
    
        return list_result





    def get_purchase_price(self,instance):

        old_price = 0 


        try:


            p_price = ProductPrice.objects.filter(product_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            old_price =p_price.purchase_price

        else:
            old_price = 0


        float_total = format(old_price, '0.2f')
        return float_total


    def get_old_price(self,instance):



        new_price = 0
    

        product_id = instance.id

        try:
            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            spec_ids = list(p_spec.values_list('id',flat=True).distinct())

            new_prices = []

            old_prices = []

            for i in range(len(spec_ids)):

                try:

                    specz = ProductSpecification.objects.get(id = spec_ids[i])

                except:

                    specz = None 

                if specz:

                    specz_serializer = ProductSpecificationSerializer1(specz,many=False)

                    specz_data = specz_serializer.data

                    price_value = specz_data["new_price"]

                    old_price_value = specz_data["old_price"]

                    new_prices.append(float(price_value))
                    old_prices.append(float(old_price_value))



            print(new_prices)
            print(old_prices)


            new_price = min(new_prices)
            min_index = new_prices.index(min(new_prices))
            old_price = old_prices[min_index]


        else:
            old_price = 0
        


        float_total = format(old_price, '0.2f')
        return float_total



    def get_new_price(self,instance):

        new_price = 0
        discount = 0  

        product_id = instance.id

        try:
            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            spec_ids = list(p_spec.values_list('id',flat=True).distinct())

            new_prices = []

            for i in range(len(spec_ids)):

                try:

                    specz = ProductSpecification.objects.get(id = spec_ids[i])

                except:

                    specz = None 

                if specz:

                    specz_serializer = ProductSpecificationSerializer1(specz,many=False)

                    specz_data = specz_serializer.data

                    price_value = specz_data["new_price"]

                    new_prices.append(float(price_value))



            print(new_prices)


            new_price = min(new_prices)


        else:
            new_price = 0
        


        float_total = format(new_price, '0.2f')
        return float_total





    def get_specification(self,instance):

        arr =  {'colors':[],'sizes':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            colors = list(p_spec.values_list('color',flat=True).distinct())
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            #units = list(p_spec.values_list('unit',flat=True).distinct())

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



    def get_cat(self,instance):

        title = ""

        try:

            category = Category.objects.get(id=instance.category_id)

        except:

            category = None


        if category:

            title = category.title


        return title


    def get_sub_cat(self,instance):

        title = ""

        try:

            category = Sub_Category.objects.get(id=instance.sub_category_id)

        except:

            category = None


        if category:

            title = category.title


        return title



    def get_sub_sub_cat(self,instance):

        title = ""

        try:

            category = Sub_Sub_Category.objects.get(id=instance.sub_sub_category_id)

        except:

            category = None


        if category:

            title = category.title


        return title


    def get_discount_type(self,instance):

        discount_type = ""

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_type = discount.discount_type


        return discount_type



    def get_discount_amount(self,instance):

        discount_amount = 0

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_amount = discount.amount


        return discount_amount


    def get_discount_start_date(self,instance):

        discount_start_date = ""

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_start_date = discount.start_date


        return discount_start_date



    def get_discount_end_date(self,instance):

        discount_end_date = ""

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_end_date = discount.end_date


        return discount_end_date


    def get_point(self,instance):

        point_amount = 0

        try:

            point = ProductPoint.objects.filter(product_id=instance.id).last()

        except:

            point = None

            


        if point:

            point_amount = point.point


        return point_amount



    def get_point_start_date(self,instance):

        point_start_date = 0

        try:

            point = ProductPoint.objects.filter(product_id=instance.id).last()

        except:

            point = None

            


        if point:

            point_start_date = point.start_date


        return point_start_date



    def get_point_end_date(self,instance):

        point_end_date = 0

        try:

            point = ProductPoint.objects.filter(product_id=instance.id).last()

        except:

            point = None

            


        if point:

            point_end_date = point.end_date


        return point_end_date


    def get_seller_name(self,instance):

        name = ""

        try:

            username = User.objects.get(id=instance.seller)

        except:

            username = None

            


        if username:

            name = username.username


        return name


    def get_seller_email(self,instance):

        name = ""

        try:

            username = User.objects.get(id=instance.seller)

        except:

            username = None

            


        if username:

            name = username.email


        return name


class SearchSerializer1(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    new_price = serializers.SerializerMethodField(method_name='get_new_price')
    old_price = serializers.SerializerMethodField(method_name='get_old_price')
    specification = serializers.SerializerMethodField(method_name='get_specification')
    ratings = serializers.SerializerMethodField(method_name='get_ratings')


    #comment_name = serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = Product
        fields = ('id','title','old_price','new_price','brand','images','specification','ratings')

    def get_images(self,instance):
        try:

            replys = ProductImage.objects.filter(product_id=instance.id).values()

        except:
            replys = None

        if replys:
            list_result = [entry for entry in replys] 

        else:
            list_result = []
    
        return list_result


    def get_old_price(self,instance):



        new_price = 0
    

        product_id = instance.id

        try:
            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            spec_ids = list(p_spec.values_list('id',flat=True).distinct())

            new_prices = []

            old_prices = []

            for i in range(len(spec_ids)):

                try:

                    specz = ProductSpecification.objects.get(id = spec_ids[i])

                except:

                    specz = None 

                if specz:

                    specz_serializer = ProductSpecificationSerializer1(specz,many=False)

                    specz_data = specz_serializer.data

                    price_value = specz_data["new_price"]

                    old_price_value = specz_data["old_price"]

                    new_prices.append(float(price_value))
                    old_prices.append(float(old_price_value))



            print(new_prices)
            print(old_prices)


            new_price = min(new_prices)
            min_index = new_prices.index(min(new_prices))
            old_price = old_prices[min_index]


        else:
            old_price = 0
        


        float_total = format(old_price, '0.2f')
        return float_total




    def get_new_price(self,instance):

        new_price = 0
        discount = 0  

        product_id = instance.id

        try:
            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            spec_ids = list(p_spec.values_list('id',flat=True).distinct())

            new_prices = []

            for i in range(len(spec_ids)):

                try:

                    specz = ProductSpecification.objects.get(id = spec_ids[i])

                except:

                    specz = None 

                if specz:

                    specz_serializer = ProductSpecificationSerializer1(specz,many=False)

                    specz_data = specz_serializer.data

                    price_value = specz_data["new_price"]

                    new_prices.append(float(price_value))



            print(new_prices)


            new_price = min(new_prices)


        else:
            new_price = 0
        


        float_total = format(new_price, '0.2f')
        return float_total





    def get_specification(self,instance):

        arr =  {'colors':[],'sizes':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            colors = list(p_spec.values_list('color',flat=True).distinct())
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            #units = list(p_spec.values_list('unit',flat=True).distinct())

            arr =  {'colors':colors,'sizes':sizes}

            return arr

        else:

            return arr


    def get_ratings(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/ratings/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values







class SearchSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    new_price = serializers.SerializerMethodField(method_name='get_new_price')
    old_price = serializers.SerializerMethodField(method_name='get_old_price')
    specification = serializers.SerializerMethodField(method_name='get_specification')
    ratings = serializers.SerializerMethodField(method_name='get_ratings')


    #comment_name = serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = Product
        fields = ('id','title','old_price','new_price','brand','unit','images','specification','ratings')

    def get_images(self,instance):
        try:

            replys = ProductImage.objects.filter(product_id=instance.id).values()

        except:
            replys = None

        if replys:
            list_result = [entry for entry in replys] 

        else:
            list_result = []
    
        return list_result


    def get_old_price(self,instance):

        old_price = 0 


        try:


            p_price = ProductPrice.objects.filter(product_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:



            old_price =p_price.price

        else:
            old_price = 0


        float_total = format(old_price, '0.2f')
        return float_total



    def get_new_price(self,instance):

        new_price = 0
        discount = 0  


        try:


            p_price = ProductPrice.objects.filter(product_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            new_price =p_price.price

            try:

                p_discount = discount_product.objects.filter(product_id = instance.id).last()

            except:

                p_discount = None


            if p_discount is not None:

                current_date = timezone.now().date()

                if p_discount.amount:

                    discount = p_discount.amount

                else:
                    discount = 0


                if p_discount.start_date:

                    discount_start_date = p_discount.start_date

                else:
                    discount_start_date = current_date

                if p_discount.end_date:
                    discount_end_date = p_discount.end_date

                else:
                    discount_end_date = current_date
                

                if (current_date >= discount_start_date) and (current_date <= discount_end_date):

                    new_price = new_price - discount

                else:
                    discount =0 
                    new_price = new_price - discount

            else:
                discount = 0
                new_price = new_price - discount




        else:

            new_price = 0
            


        float_total = format(new_price, '0.2f')
        return float_total


    def get_specification(self,instance):

        arr =  {'colors':[],'sizes':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            colors = list(p_spec.values_list('color',flat=True).distinct())
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            #units = list(p_spec.values_list('unit',flat=True).distinct())
            colors.remove(None)
            colors.remove(None)

            arr =  {'colors':colors,'sizes':sizes}

            return arr

        else:

            return arr


    def get_ratings(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/ratings/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= [
            "id",
            "title",
            'active',
            'timestamp'

            ]

class GroupProductSerialyzer(serializers.ModelSerializer):
    #count =serializers.SerializerMethodField(method_name='get_Products_ids')
    class Meta:
        model= GroupProduct
        fields = [
            'id',
            "products_ids",
            'title',
            
            'startdate',
            'enddate',
            'flashsellname',
            'active',
            'timestamp',
            'product_id'
        ]
 
    # def get_Products_ids(self, obj):
    #     return len(obj.products_ids)


class SerpyProductSerializer(serpy.Serializer):
    seller = serpy.StrField()
    category = serpy.StrField()
    title = serpy.StrField()
    price = serpy.FloatField()
    image = serpy.StrField()
    description = serpy.StrField()
    quantity = serpy.IntField()
    views = serpy.IntField()

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # read_only_fields = ('id', 'seller', 'category', 'title', 'price', 'image', 'description', 'quantity', 'views',)

#------------Comment Serializers---------------
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(method_name='get_replies')
    comment_name = serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = Comment
        fields = ('id','comment','date_created','product_id','user_id','non_verified_user_id','comment_name','replies',)

    def get_replies(self,instance):

        replys = CommentReply.objects.filter(comment_id=instance.id).values()
        list_result = [entry for entry in replys]

    
        return list_result

    def get_name(self,instance):
            user_id = instance.user_id
            non_verified_user_id = instance.non_verified_user_id
            comment_name=""
            
    
            if user_id is not None:
                user_id = int(user_id)
                non_verified_user_id =0

            else:
                non_verified_user_id = non_verified_user_id
                user_id = 0

            

            if non_verified_user_id == 0:


                try:


                    name = User.objects.filter(id=user_id).last()
                except:
                    name = None
                if name is not None:
                    comment_name = name.username
                    return comment_name
                else:
                    
                    return comment_name

            else:

                comment_name = "Anonymous"
                return comment_name



class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = ('id','comment_id','reply','date_created','user_id','non_verified_user_id','name')


#------------Review Serializers--------------------
class ReviewsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_name')
    image_link = serializers.SerializerMethodField(method_name='get_image')
    
    class Meta:
        model = Reviews
        fields = ('id','product_id','user_id','non_verified_user_id','name','content','image','image_link','rating','date_created')

    def get_name(self,instance):
            user_id = instance.user_id
            non_verified_user_id = instance.non_verified_user_id
            comment_name=""
            
    
            if user_id is not None:
                user_id = int(user_id)
                non_verified_user_id =0

            else:
                non_verified_user_id = non_verified_user_id
                user_id = 0

            

            if non_verified_user_id == 0:


                try:


                    name = User.objects.filter(id=user_id).last()
                except:
                    name = None
                if name is not None:
                    comment_name = name.username
                    return comment_name
                else:
                    
                    return comment_name

            else:

                comment_name = "Anonymous"
                return comment_name


    def get_image(self,instance):

        #print("Coming here2")

        try:
            logo_image = Reviews.objects.get(id=instance.id)
        except:
            logo_image = None

        if logo_image is None:
            #print("Coming here3")
            return ""

        else:
            if logo_image.image:

                logo = logo_image.image

                return "{0}{1}".format(host_name,logo.url)

            else:

                return ""

            





class ProductReviewSerializer(serializers.ModelSerializer):
    total_no_of_ratings = serializers.SerializerMethodField(method_name='total_ratings')
    total_no_of_reviews = serializers.SerializerMethodField(method_name='total_reviews')
    average_ratings = serializers.SerializerMethodField(method_name='average_rating')
    each_ratings = serializers.SerializerMethodField(method_name='each_rating')
    class Meta:
        model = Reviews
        fields = ('product_id','total_no_of_ratings','total_no_of_reviews','average_ratings','each_ratings')

    def total_ratings(self,instance):
        try:

            product = Reviews.objects.filter(product_id=instance.product_id).count()

        except:

            product = None

        if product:
            return int(product)

        else:

            return 0

       

        

    def total_reviews(self,instance):
        try:

            product = Reviews.objects.filter(product_id=instance.product_id).count()

        except:

            product = None

        if product:
            return int(product)

        else:

            return 0




    def average_rating(self,instance):


    
        num = 0



        try:

            product = Reviews.objects.filter(product_id=instance.product_id)

        except:

            product = None


        if product:

            product_count = Reviews.objects.filter(product_id=instance.product_id).count()
            review_ids = product.values_list('rating' , flat = True)
            total_count = 0
            #print(len(review_ids))

            for i in range(len(review_ids)):

                total_count += int(review_ids[i])

            average = total_count/product_count


            num1 = int(average)
            num2 = average%1
            if num2>0.5:
                num2=1
            elif num2 == 0.5:
                num2=0.5
            else:
                num2=0

            #print(num2)

            num = num1 + num2

            return num

        else:


            num = 0

            return num
            


       

      

    def each_rating(self,instance):

        sum_one = 0
        sum_two = 0
        sum_three = 0
        sum_four = 0
        sum_five =0 

        try:
            product = Reviews.objects.filter(product_id=instance.product_id)
            review_ids = product.values_list('rating' , flat = True)

            for i in range(len(review_ids)):
                if review_ids[i] == 1:
                    sum_one += 1

                elif review_ids[i] == 2:
                    sum_two += 1


                elif review_ids[i] == 3:
                    sum_three += 1


                elif review_ids[i] == 4:
                    sum_four += 1

                else:
                    sum_five += 1



            nums = [{"rating":1,"count":sum_one},{"rating":2,"count":sum_two},{"rating":3,"count":sum_three},{"rating":4,"count":sum_four},{"rating":5,"count":sum_five}]




        except:
            product = None

        if product:
            return nums

        else:
            return ""


# ---------------------------- Product Code ------------------

class ProductCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCode
        fields = "__all__"

class ScannerProductSerializer(serializers.ModelSerializer):
    scan_product_id = serializers.SerializerMethodField('scanned_product_value')

    class Meta:
        model = ProductCode
        fields = ('scan_product_id','date')

    def scanned_product_value(self,obj):
        return obj.product_id

#---------------------------- Group Product----------------------

class AllGroupProductSerialyzer (serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField(method_name='get_product')
    images = serializers.SerializerMethodField(method_name='get_images')
    Group_data = serializers.SerializerMethodField(method_name='get_group_info')
    price = serializers.SerializerMethodField(method_name='get_price')

    specification = serializers.SerializerMethodField(method_name='get_specification')
    point = serializers.SerializerMethodField(method_name='get_point')
    discount = serializers.SerializerMethodField(method_name='get_discount')
    
    code = serializers.SerializerMethodField(method_name='get_code')
    
    class Meta:
        model = Product
        fields = ('product_details','Group_data','price','specification','point','discount','images','code')
        #fields = ('product_details','images','price','specification','code','discount','point')

    def get_images(self,instance):
        try:

            Images = ProductImage.objects.filter(product_id=instance.id).values()

        except:
            Images = None

        if Images:
            list_result = [entry for entry in Images] 

        else:
            list_result = []
    
        return list_result

    def get_product (self,instance):
        
        try:
            values= Product.objects.filter(id=instance.id).values()[0]
            return values
        except:
            return ''

    def get_group_info (self,instance):
        
        try:
          
            values= GroupProduct.objects.filter(product_id=instance.id).values()[0]
            return values
        except:
            return ''
       

    def get_price (self,instance):
    
        try:
            values= ProductPrice.objects.filter(product_id=instance.id).values()[0]
            return values
        except:
            return " "

    def get_specification (self,instance):
        try:
            values= ProductSpecification.objects.filter(product_id=instance.id).values()[0]
            return values
        except:
            return " "

    def get_code (self,instance):
        try:
            values= ProductCode.objects.filter(product_id=instance.id).values()[0]
            return values
        except:
            return " "

    def get_discount (self,instance):
        try:
            values= discount_product.objects.filter(product_id=instance.id).values()[0]
            return values
        except:
            return " "

    def get_point (self,instance):
        try:
            values= ProductPoint.objects.filter(product_id=instance.id).values()[0]
            return values
        except:
            return " "




class SellerInfoSerializer(serializers.ModelSerializer):


    name = serializers.SerializerMethodField(method_name='get_name')
    address = serializers.SerializerMethodField(method_name='get_address')
    area = serializers.SerializerMethodField(method_name='get_area')
    location = serializers.SerializerMethodField(method_name='get_location')
    total_approved_products = serializers.SerializerMethodField(method_name='get_approved')
    total_cancelled_products = serializers.SerializerMethodField(method_name='get_cancelled')
    total_pending_products = serializers.SerializerMethodField(method_name='get_pending')



    class Meta:
        model = User
        fields = ('id','username','email','phone_number','name','address','area','location','total_approved_products','total_pending_products','total_cancelled_products')


    def get_name(self,instance):



        try:

            profile = Profile.objects.get(email=instance.email,user_id=instance.id)


        except:

            profile = None 


        if profile:

            if profile.name:

                name = profile.name

            else:

                name = "N/A"




        else:

            name = "N/A"


        return name 



    def get_address(self,instance):



        try:

            profile = Profile.objects.get(email=instance.email,user_id=instance.id)


        except:

            profile = None 


        if profile:

            if profile.address:

                name = profile.address

            else:

                name = "N/A"




        else:

            name = "N/A"


        return name 



    def get_location(self,instance):



        try:

            profile = Profile.objects.get(email=instance.email,user_id=instance.id)


        except:

            profile = None 


        if profile:

            if profile.location:

                name = profile.location

            else:

                name = "N/A"




        else:

            name = "N/A"


        return name



    def get_area(self,instance):



        try:

            profile = Profile.objects.get(email=instance.email,user_id=instance.id)


        except:

            profile = None 


        if profile:

            if profile.area:

                name = profile.area

            else:

                name = "N/A"




        else:

            name = "N/A"


        return name 


    def get_approved(self,instance):



        try:

            products = Product.objects.filter(seller=instance.id,product_admin_status="Confirmed")

        except:

            products = None 


        if products:


            seller_ids = list(products.values_list('id',flat=True))


            product_count = int(len(seller_ids))


        else:

            product_count = 0 


        return product_count




    def get_cancelled(self,instance):



        try:

            products = Product.objects.filter(seller=instance.id,product_admin_status="Cancelled")

        except:

            products = None 


        if products:


            seller_ids = list(products.values_list('id',flat=True))


            product_count = int(len(seller_ids))


        else:

            product_count = 0 


        return product_count



    def get_pending(self,instance):



        try:

            products = Product.objects.filter(seller=instance.id,product_admin_status="Processing")

        except:

            products = None 


        if products:


            seller_ids = list(products.values_list('id',flat=True))


            product_count = int(len(seller_ids))


        else:

            product_count = 0 


        return product_count





class SellerInfoProductSerializer(serializers.ModelSerializer):

    # product_color = serializers.SerializerMethodField(method_name='get_color')
    # product_size = serializers.SerializerMethodField(method_name='get_size')
    # variant = serializers.SerializerMethodField(method_name='get_variant')
    # selling_price = serializers.SerializerMethodField(method_name='get_selling_price')
    # purchase_price = serializers.SerializerMethodField(method_name='get_purchase_price')
    specifications = serializers.SerializerMethodField(method_name='get_specifications')



    class Meta:
        model = Product
        # fields = ('id','title','brand','product_color','product_size','variant','selling_price','purchase_price')
        fields = ('id','title','brand','origin','shipping_country','specifications')




    def get_specifications(self,instance):

        try:

            product = ProductSpecification.objects.filter(product_id=instance.id)


        except:

            product = None 


        if product: 


            product_serializer = ProductSpecificationSerializer1(product,many=True)

            product_data = product_serializer.data



        else:

            product_data = []



        return product_data






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



    def get_selling_price(self,instance):



        new_price = 0
    

        product_id = instance.id

        try:
            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            spec_ids = list(p_spec.values_list('id',flat=True).distinct())

            new_prices = []

            old_prices = []

            for i in range(len(spec_ids)):

                try:

                    specz = ProductSpecification.objects.get(id = spec_ids[i])

                except:

                    specz = None 

                if specz:

                    specz_serializer = ProductSpecificationSerializer1(specz,many=False)

                    specz_data = specz_serializer.data

                    price_value = specz_data["new_price"]

                    old_price_value = specz_data["old_price"]

                    new_prices.append(float(price_value))
                    old_prices.append(float(old_price_value))



            print(new_prices)
            print(old_prices)


            new_price = min(new_prices)
            min_index = new_prices.index(min(new_prices))
            old_price = old_prices[min_index]


        else:
            old_price = 0
        


        float_total = format(old_price, '0.2f')
        return float_total





    def get_purchase_price(self,instance):



        new_price = 0
    

        product_id = instance.id

        try:
            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            spec_ids = list(p_spec.values_list('id',flat=True).distinct())

            new_prices = []

            old_prices = []

            purchase_prices = []

            for i in range(len(spec_ids)):

                try:

                    specz = ProductSpecification.objects.get(id = spec_ids[i])

                except:

                    specz = None 

                if specz:

                    specz_serializer = ProductSpecificationSerializer1(specz,many=False)

                    specz_data = specz_serializer.data

                    price_value = specz_data["new_price"]

                    old_price_value = specz_data["old_price"]

                    purchase_price_value = specz_data["purchase_price"]

                    new_prices.append(float(price_value))
                    old_prices.append(float(old_price_value))
                    purchase_prices.append(float(purchase_price_value))



            print(new_prices)
            print(old_prices)


            new_price = min(new_prices)
            min_index = new_prices.index(min(new_prices))
            old_price = old_prices[min_index]
            purchase_price = purchase_prices[min_index]


        else:
            purchase_price = 0
        


        float_total = format(purchase_price, '0.2f')
        return float_total






class ProductAdminSerializer1(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    purchase_price = serializers.SerializerMethodField(method_name='get_purchase_price')
    new_price = serializers.SerializerMethodField(method_name='get_new_price')
    old_price = serializers.SerializerMethodField(method_name='get_old_price')
    specification = serializers.SerializerMethodField(method_name='get_specification')
    quantity = serializers.SerializerMethodField(method_name='get_quantity')
    category = serializers.SerializerMethodField(method_name='get_cat')
    sub_category = serializers.SerializerMethodField(method_name='get_sub_cat')
    sub_sub_category = serializers.SerializerMethodField(method_name='get_sub_sub_cat')
    discount_type = serializers.SerializerMethodField(method_name='get_discount_type')
    discount_start_date = serializers.SerializerMethodField(method_name='get_discount_start_date')
    discount_end_date = serializers.SerializerMethodField(method_name='get_discount_end_date')
    discount_amount = serializers.SerializerMethodField(method_name='get_discount_amount')
    point = serializers.SerializerMethodField(method_name='get_point')
    point_start_date = serializers.SerializerMethodField(method_name='get_point_start_date')
    point_end_date = serializers.SerializerMethodField(method_name='get_point_end_date')
    seller_name = serializers.SerializerMethodField(method_name='get_seller_name')
    specifications = serializers.SerializerMethodField(method_name='get_specifications')
    seller_email = serializers.SerializerMethodField(method_name='get_seller_email')
    specific_status = serializers.SerializerMethodField(method_name='get_specific_status')




    #comment_name = serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = Product
        fields = ('id','seller_name','seller_email', "specific_status" , 'product_admin_status','title','brand','date','description','key_features','properties','origin','shipping_country','purchase_price','old_price','new_price','discount_type','discount_amount','discount_start_date','discount_end_date','point','point_start_date','point_end_date','images','specification','quantity','category','sub_category','sub_sub_category','specifications','product_status')

    def get_specifications(self,instance):

        try:

            product = ProductSpecification.objects.filter(product_id=instance.id)


        except:

            product = None 


        if product: 


            product_serializer = ProductSpecificationSerializer1(product,many=True)

            product_data = product_serializer.data



        else:

            product_data = []



        return product_data


   

    def get_specific_status(self , instance):
        
        try:

            product = ProductSpecification.objects.filter(product_id=instance.id)


        except:

            product = None 
           

        if product : 

            product_serializer = ProductSpecificationSerializer1(product,many=True)

            product_data = len(product_serializer.data)

            # product_data = "YES"



        else:

            product_data = "0"



        return product_data

    def get_images(self,instance):
        try:

            replys = ProductImage.objects.filter(product_id=instance.id).values()

        except:
            replys = None

        if replys:
            list_result = [entry for entry in replys] 

        else:
            list_result = []
    
        return list_result





    def get_purchase_price(self,instance):

        old_price = 0 


        try:


            p_price = ProductPrice.objects.filter(product_id = instance.id).last()

        except:

            p_price = None 


        if p_price is not None:

            old_price =p_price.purchase_price

        else:
            old_price = 0


        float_total = format(old_price, '0.2f')
        return float_total


    def get_old_price(self,instance):



        new_price = 0
    

        product_id = instance.id

        try:
            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            spec_ids = list(p_spec.values_list('id',flat=True).distinct())

            new_prices = []

            old_prices = []

            for i in range(len(spec_ids)):

                try:

                    specz = ProductSpecification.objects.get(id = spec_ids[i])

                except:

                    specz = None 

                if specz:

                    specz_serializer = ProductSpecificationSerializer1(specz,many=False)

                    specz_data = specz_serializer.data

                    price_value = specz_data["new_price"]

                    old_price_value = specz_data["old_price"]

                    new_prices.append(float(price_value))
                    old_prices.append(float(old_price_value))





            new_price = min(new_prices)
            min_index = new_prices.index(min(new_prices))
            old_price = old_prices[min_index]


        else:
            old_price = 0
        


        float_total = format(old_price, '0.2f')
        return float_total



    def get_new_price(self,instance):

        new_price = 0
        discount = 0  

        product_id = instance.id

        try:
            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            spec_ids = list(p_spec.values_list('id',flat=True).distinct())

            new_prices = []

            for i in range(len(spec_ids)):

                try:

                    specz = ProductSpecification.objects.get(id = spec_ids[i])

                except:

                    specz = None 

                if specz:

                    specz_serializer = ProductSpecificationSerializer1(specz,many=False)

                    specz_data = specz_serializer.data

                    price_value = specz_data["new_price"]

                    new_prices.append(float(price_value))



            print(new_prices)


            new_price = min(new_prices)


        else:
            new_price = 0
        


        float_total = format(new_price, '0.2f')
        return float_total





    def get_specification(self,instance):

        arr =  {'colors':[],'sizes':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            colors = list(p_spec.values_list('color',flat=True).distinct())
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            #units = list(p_spec.values_list('unit',flat=True).distinct())

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



    def get_cat(self,instance):

        title = ""

        try:

            category = Category.objects.get(id=instance.category_id)

        except:

            category = None


        if category:

            title = category.title


        return title


    def get_sub_cat(self,instance):

        title = ""

        try:

            category = Sub_Category.objects.get(id=instance.sub_category_id)

        except:

            category = None


        if category:

            title = category.title


        return title



    def get_sub_sub_cat(self,instance):

        title = ""

        try:

            category = Sub_Sub_Category.objects.get(id=instance.sub_sub_category_id)

        except:

            category = None


        if category:

            title = category.title


        return title


    def get_discount_type(self,instance):

        discount_type = ""

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_type = discount.discount_type


        return discount_type



    def get_discount_amount(self,instance):

        discount_amount = 0

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_amount = discount.amount


        return discount_amount


    def get_discount_start_date(self,instance):

        discount_start_date = ""

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_start_date = discount.start_date


        return discount_start_date



    def get_discount_end_date(self,instance):

        discount_end_date = ""

        try:

            discount = discount_product.objects.filter(product_id=instance.id).last()

        except:

            discount = None

            


        if discount:

            discount_end_date = discount.end_date


        return discount_end_date


    def get_point(self,instance):

        point_amount = 0

        try:

            point = ProductPoint.objects.filter(product_id=instance.id).last()

        except:

            point = None

            


        if point:

            point_amount = point.point


        return point_amount



    def get_point_start_date(self,instance):

        point_start_date = 0

        try:

            point = ProductPoint.objects.filter(product_id=instance.id).last()

        except:

            point = None

            


        if point:

            point_start_date = point.start_date


        return point_start_date



    def get_point_end_date(self,instance):

        point_end_date = 0

        try:

            point = ProductPoint.objects.filter(product_id=instance.id).last()

        except:

            point = None

            


        if point:

            point_end_date = point.end_date


        return point_end_date


    def get_seller_name(self,instance):

        name = ""

        try:

            username = User.objects.get(id=instance.seller)

        except:

            username = None

            


        if username:

            name = username.username


        return name


    def get_seller_email(self,instance):

        name = ""

        try:

            username = User.objects.get(id=instance.seller)

        except:

            username = None

            


        if username:

            name = username.email


        return name








 



























