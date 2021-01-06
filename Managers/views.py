from django.shortcuts import render

# Create your views here.
from django.shortcuts import render , redirect
from rest_framework import generics, status, views
from .serializers import ManagerListSerializer
from rest_framework.response import Response
from Intense.models import User,Managers_list,manager_inventory_status


from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.decorators import api_view

from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from django.contrib import auth
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView , UpdateAPIView 

from rest_framework.exceptions import PermissionDenied, NotAcceptable, ValidationError

from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from Intense.models import (Profile, User , user_relation,Guest_user,Warehouse,
Shop,inventory_report,ProductSpecification,ProductCode,ProductImage,Product,TransferRequest,TransferProductSpec,
WarehouseInfo,ShopInfo)

from django.contrib.auth.models import Group
from django.contrib import messages
from django.db import transaction
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from random import randint
import requests
from django.core.serializers import serialize
# from rest_framework import serializers
import json

@api_view (["GET","POST"])
def manager_create (request):
    try:
        if request.method == 'POST':
            pwd = make_password(request.data['password'])
            user_creation = User.objects.create(
                username = request.data['username'],
                email = request.data['email'],
                role = request.data['role'],
                is_staff=True,
                is_verified=True,
                is_active=True,
                phone_number = request.data['phone_number'],
                password = pwd,
                pwd = request.data['password']
            )
            user_creation.save()
            user_id = user_creation.id
            created = False
            if 'shop_id' in request.data:
                manager_create = Managers_list.objects.create(
                   shop_id =  request.data['shop_id'],
                   user_id=user_id,
                )
                manager_create.save()
                created = True
            elif 'warehouse_id' in request.data:
                manager_create = Managers_list.objects.create(
                   warehouse_id =  request.data['warehouse_id'],
                   user_id=user_id,
                )
                manager_create.save()
                created = True
            if created:
                return Response({
                    'success': True,
                    'message': 'Role has been created successfully !!'
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Role Could not be created !!'
                })
    except Exception as e:
        print("here is the exception", e.args[0])
        return Response({
            'success': False,
            'message': e.args[0]
        })


@api_view (["GET","POST"])
def active_deactive_manager (request,number,mang_id):
    try:
        if request.method == 'POST':
            try:
                manager=Managers_list.objects.get(id = mang_id)
            except:
                manager = None
            changed = False
            if manager and number == 0:
                manager.is_active = False
                manager.save()
                changed = True
            elif manager and number == 1:
                manager.is_active = True
                manager.save()
                changed = True

            if changed:
                return Response ({
                    'success': True,
                    'message': 'Manager status has been updated !!',
                })
            else:
                return Response ({
                    'success': False,
                    'message': "Manager status could not be updated !!"
                })
    
    except Exception as e:
        return Response({
            'success': False,
            'message': e.args[0]
        })


def get_manager_info(manager):
    all_data=[]
    for man in manager:
        user_info = User.objects.filter(id = man.user_id)
        data = serialize('json', user_info, fields=('username','email','phone_number','role'))
        val_d=json.loads(data)
        val_d[0]['fields'].update({'is_active':man.is_active, 'manager_id':man.id, 'shop_id': man.shop_id, 'warehouse_id': man.warehouse_id, 'user_id':man.user_id})
        update_data = val_d[0]['fields']
        all_data.append(update_data)
    return all_data

@api_view (["GET","POST"])
def get_particular_manager (request,number,house_id):
    try:
        if request.method == 'GET':
            data_val = None
            if number == 0:
                manager=Managers_list.objects.filter(shop_id = house_id)
                data_val = get_manager_info(manager)
                    
            if number == 1:
                manager=Managers_list.objects.filter(warehouse_id = house_id)
                data_val = get_manager_info(manager)
            if data_val:
                return Response({
                    'success': True,
                    'data': data_val
                })
            else:
                return Response({
                    'success': False,
                    'message': " Requested data does not exists !!"
                })
    except Exception as e:
        return Response({
            'success': False,
            'message': e.args[0]
        })
 
def man_pro_insert(value):
    try:
        for val in value['status_data']:
            saving_value = manager_inventory_status.objects.create(
                inv_rep_id = value['inv_rep_id'],
                manager_status = val['status'],
                product_quantity = val['quantity'],
                manager_id = value['manager_id']
            )
        saving_value.save()
        return True
    except:
        return False

@api_view (["GET","POST"])
def manager_product_insertion (request):
    if request.method =='POST':
        demo_data = request.data
        # demo_data = {
        #     'inv_rep_id': 443,
        #     'manager_id': 2,
        #     'status_data': [
        #         {
        #             'status': 'Approved',
        #             'quantity': 20
        #         },
        #         {
        #             'status': 'Not Found',
        #             'quantity': 5
        #         },
        #         {
        #             'status': 'Damaged',
        #             'quantity': 10
        #         }
        #     ]
        # }
        value = man_pro_insert(demo_data)
        if value:
            inv_data_val = inventory_report.objects.get(pk =demo_data['inv_rep_id'])
            inv_data_val.manager_attend = True
            inv_data_val.save()
            return Response({
                'success': True,
                'message': "manager inventory record has been created successfully"
            })
        else:
            return Response({
                'success': False,
                'message': "manager inventory record could not be created !!"
            })

@api_view (["GET","POST"])
def get_combine_houses(request):
    if request.method == 'GET':
        all_ware_houses = []
        all_shop_data=[]
        ware_houses = Warehouse.objects.all()
        data = serialize('json', ware_houses, fields=('pk','warehouse_name','warehouse_location'))
        val_d=json.loads(data)
        for all_info in val_d:
            ware_h={
                'id': all_info['pk'],
                'warehouse_name': all_info['fields']['warehouse_name'],
                'warehouse_location': all_info['fields']['warehouse_location'],
                'number': 1
            }
            all_ware_houses.append(ware_h)

        shops_data = Shop.objects.all()
        data = serialize('json', shops_data, fields=('pk','shop_name','shop_location'))
        shop_val_d=json.loads(data)
        for shop in shop_val_d:
            shop_h={
                'id': shop['pk'],
                'shop_name': shop['fields']['shop_name'],
                'shop_name': shop['fields']['shop_location'],
                'number': 0
            }
            all_shop_data.append(shop_h)
        return Response({
            'success': True,
            'warehouse': all_ware_houses,
            'shops': all_shop_data
        })


@api_view (["GET","POST"])
def assign_manager(request):
    if request.method == 'POST':
        created_uer_list =[]
        houses_val = request.data
        # houses_val = [
        #     {
        #         'shop_id': 1,
        #         'user_id': 22
        #     },
        #     {
        #         'shop_id':2,
        #         'user_id':22
        #     }
        # ]
        for house in houses_val:
            if 'shop_id' in house:
                check_manager = Managers_list.objects.filter(shop_id = house['shop_id'], user_id = house['user_id'])
                if check_manager.exists():
                    pass
                else:
                    manager_insertion = Managers_list.objects.create (
                        shop_id=house['shop_id'],
                        user_id = house['user_id']
                        )
                    manager_insertion.save()
                    man_log={
                        'man_id':manager_insertion.id,
                        'message': "successfully created",
                        'user_id': house['user_id']
                    }
                    created_uer_list.append(man_log)
            elif 'warehouse_id' in house:
                check_manager = Managers_list.objects.filter(warehouse_id = house['warehouse_id'], user_id = house['user_id'])
                if check_manager.exists():
                    pass
                else:
                    manager_insertion = Managers_list.objects.create (
                        warehouse_id=house['warehouse_id'],
                        user_id = house['user_id']
                        )
                    manager_insertion.save()
                    man_log={
                        'man_id':manager_insertion.id,
                        'message': "successfully created",
                        'user_id': house['user_id']
                    }
                    created_uer_list.append(man_log)
        if created_uer_list:
            return Response({
                'success': True,
                'message': 'user has been assigned successfully !!',
                'log': created_uer_list
            })

        else:
            all_managers = Managers_list.objects.filter(id__in = created_uer_list)
            all_managers.delete()
            return Response({
                'success': False,
                'message': 'User could not be assigned !! Check any duplicate entry !!'
            })


    
@api_view (["GET","POST"])
def get_all_users (request):
    if request.method == 'GET':
        all_managers = Managers_list.objects.all()
        print("all managers", all_managers)
        data_val = get_manager_info(all_managers)
        return Response({
            'success': True,
            'data': data_val
        })

def unattend_details(value, flag):
    # print("here is the value", value)
    all_val_info =[]
    for spec_id_s in value:
        
        spec_id = spec_id_s.specification_id
        qty = ''
        date=''
        inv_rep_id = ''
        if flag == 0:
            inv_rep_id = spec_id_s.id
            qty = spec_id_s.credit
            date = spec_id_s.date
        elif flag ==1:
            qty = spec_id_s.quantity

        elif flag == 3:
            qty = spec_id_s.requested_qty
            qty = int(qty)
            
        spec_data = ProductSpecification.objects.filter(id=spec_id)
        if spec_data.exists():
            all_data = {}
            product_info = Product.objects.filter(id=spec_data[0].product_id)
            product_info = serialize('json', product_info,fields=('pk','title','brand','date','description','key_features','origin','shipping_country'))
            product_info=json.loads(product_info)
            if len(product_info) >0:
                all_data.update({'inv_rep_id':inv_rep_id,'quantity': qty,'specification_id': spec_id,'date': date,'Product':product_info[0]['fields']})

                 
            spec_data_val = serialize('json', spec_data,fields=('pk','product_id','size','unit','weight','color'))
            spec_data_val=json.loads(spec_data_val)
            if len(spec_data_val) >0:
                all_data.update({'product_specification':spec_data_val[0]['fields']})

            Product_img = ProductImage.objects.filter(product_id=spec_data[0].product_id)
            Product_img = serialize('json', Product_img,fields=('product_image','image_url','content','mother_url'))
            Product_img=json.loads(Product_img)
            all_img =[]
            for img in Product_img:
                all_img.append(img['fields'])
            if len(all_img)>0:
                all_data.update({'Product_image':all_img})
            pro_code = ProductCode.objects.filter(specification_id=spec_id)
            pro_code = serialize('json', pro_code,fields=('pk','Barcode','SKU','date','manual_Barcode','manual_SKU'))
            pro_code=json.loads(pro_code)
            if len(pro_code) >0:
                all_data.update({'Product_code':pro_code[0]['fields']})
            all_val_info.append(all_data)
    return all_val_info


@api_view (["GET","POST"])
def manager_unattendee_product (request, user_id):
    if request.method == 'GET':
        try:
            ware_house_data=[]
            shop_data =[]
            manager_data = Managers_list.objects.filter(user_id=user_id)
            # print("here is the manager data", manager_data)
            for manager in manager_data:
                res_data ={}
                if manager.shop_id != -1:
                    pass
                    shop = manager.shop_id
                    # print("shop info", shop)
                    unattend_products = inventory_report.objects.filter(shop_id = shop)
                    res_data = unattend_details(unattend_products,0)

                    shop_info = Shop.objects.filter(id =manager.shop_id)
                    if shop_info.exists():
                        shop_info = serialize('json', shop_info, fields=('pk','shop_name','shop_location'))
                        shop_info=json.loads(shop_info)
                        shop_info[0]['fields'].update({'id': manager.shop_id,'data': res_data})
                        shop_data.append(shop_info[0]['fields'])

                if manager.warehouse_id != -1:
                    warehouse = manager.warehouse_id
                    unattend_products = inventory_report.objects.filter(warehouse_id = warehouse, manager_attend = False)
                    res_data = unattend_details(unattend_products,0)

                    # print("here is the res data", res_data)
                    warehouse_info = Warehouse.objects.filter(id =manager.warehouse_id)
                    if warehouse_info.exists():
                        warehouse_info = serialize('json', warehouse_info, fields=('pk','warehouse_name','warehouse_location'))
                        warehouse_info=json.loads(warehouse_info)
                        warehouse_info[0]['fields'].update({'id': manager.warehouse_id,'data': res_data})
                        ware_house_data.append(warehouse_info[0]['fields'])

            return Response({
                "success": True,
                'ware_house': ware_house_data,
                'shop': shop_data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': e.args[0]
            })

@api_view (["GET","POST"])
def particular_manager_shop (request, user_id):
    if request.method == 'GET':
        try:
            manager_data = Managers_list.objects.filter(user_id = user_id)
            all_houses = []
            all_shops = []
            for res in manager_data:
                if res.shop_id != -1:
                    shop_info = Shop.objects.filter(id = res.shop_id)
                    if shop_info.exists():
                        shop_data = serialize('json', shop_info,fields=('id','shop_name','shop_location'))
                        shop_data=json.loads(shop_data)
                        shop_data[0]['fields'].update({'shop_id':shop_data[0]['pk'], 'manager_id': res.id})
                        all_shops.append(shop_data[0]['fields'])

                if res.warehouse_id != -1:
                    ware_info = Warehouse.objects.filter(id = res.warehouse_id)
                    if ware_info.exists():
                        ware_data = serialize('json', ware_info,fields=('id','warehouse_name','warehouse_location'))
                        ware_data=json.loads(ware_data)
                        ware_data[0]['fields'].update({'id':ware_data[0]['pk'],'manager_id': res.id})
                        all_houses.append(ware_data[0]['fields'])
            return Response({
                'success': True,
                'warehouse': all_houses,
                'shops': all_shops
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': e.args[0]
            })

@api_view (["GET","POST"])
def del_managers (request):
    managers = Managers_list.objects.all()
    managers.delete()
    return Response({
        'success': True
    })

@api_view (["GET","POST"])
def transfer_product_request (request):
    if request.method == 'POST':
        data_val = request.data
        # data_val = {
        #     'request_setter': 'sh_2',
        #     'request_getter': 'wh_1',
        #     'requestee_user': 2,
        #     'requested_products':[
        #         {
        #             'specification_id': 391,
        #             'requested_qty' : 20
        #         },
        #         {
        #             'specification_id': 377,
        #             'requested_qty' : 15
        #         },
        #         {
        #             'specification_id': 378,
        #             'requested_qty' : 25
        #         }
        #     ]
        # }
    try:
        transfer_data = TransferRequest.objects.create(
            request_setter = data_val['request_setter'],
            request_getter = data_val['request_getter'],
            requestee_user = data_val['requestee_user']
        )

        transfer_data.save()
        transfer_id = transfer_data.id
        trans_all_produt_id = []
        try:
            for pro_val in data_val['requested_products']:
                product_trans = TransferProductSpec.objects.create(
                    specification_id = pro_val['specification_id'],
                    requested_qty = pro_val['requested_qty'],
                    transfer_id = transfer_id
                )
                product_trans .save()
                trans_all_produt_id.append(product_trans.id)
                all_spec_data = TransferProductSpec.objects.filter(id__in = trans_all_produt_id)
        except Exception as e:
            all_spec_data = TransferProductSpec.objects.filter(id__in = trans_all_produt_id)
            all_spec_data.delete()
            transfer = TransferRequest.objects.filter(id = transfer_id)
            transfer.delete()
            return Response ({
                'success': False,
                'message': e.args[0]
            })
        return Response ({
            'success': True,
            'message': 'Transfer request has been successfully generated !!',
            'transfer_id': transfer_id
        })
    except Exception as e:
        return Response ({
            'success': False,
            'message': e.args[0]
        })
    

@api_view (["GET","POST"])
def get_particular_user_all_products (request,number,house_id):
    if request.method == 'GET':
        try:
            if number ==0:
                shop_data = ShopInfo.objects.filter(shop_id=house_id)
                data_val = unattend_details(shop_data,1)
            elif number ==1:
                ware_data = WarehouseInfo.objects.filter(warehouse_id=house_id)
                data_val = unattend_details(ware_data,1)
            else:
                data_val =[]
            return Response ({
                'success': True,
                'data': data_val
            })
        except Exception as e:
            return Response ({
                'success': False,
                'message': e.args[0]
            })



@api_view (["GET","POST"])
def get_transfer_request_products (request,request_getter):
    if request.method == 'GET':
        try:
            trans_req = TransferRequest.objects.filter(request_getter = request_getter, status = 'Pending')
            if trans_req.exists():
                print(trans_req)
                all_pending_requests =[]
                for trans in trans_req:
                    req_id = trans.id
                    trans_pro_spec = TransferProductSpec.objects.filter (transfer_id = req_id)
                    res_data = unattend_details (trans_pro_spec,3)
                    requestee_house = trans.request_setter.split('_')
                    house_name = ''
                    house_location = ''
                    if requestee_house[0] == 'sh':
                        shop_house = Shop.objects.get(id = int(requestee_house[1]))
                        house_name = shop_house.shop_name
                        house_location = shop_house.shop_location
                    elif requestee_house[0] == 'wh':
                        wrae_house = Warehouse.objects.get(id = int(requestee_house[1]))
                        house_name = wrae_house.warehouse_name
                        house_location = wrae_house.warehouse_location
                    requestee_info = {
                        'request_setter': trans_req[len(trans_req)-1].request_setter,
                        'request_getter': trans_req[len(trans_req)-1].request_getter,
                        'house_name': house_name,
                        'house_location': house_location,
                        'transfer_id': req_id
                    }
                    if res_data:
                        res_data.append(requestee_info)
                        all_pending_requests.append(res_data)
                return Response({
                    'success': True,
                    'requestee_info': all_pending_requests
                    
                })
            else:
                return Response ({
                    'success': False,
                    'message': "Requested transaction does not exists !!"
                })
        except Exception as e:
            return Response ({
                'success': False,
                'message': e.args[0]
            }) 
            
@api_view (["GET","POST"])
def all_shops_warehouse_lists (request):
    if request.method == 'GET':
        try:
            all_shop = Shop.objects.all()
            all_houses =[]
            for shop in all_shop:
                shop={
                    'shop_mod_id' : 'sh_'+str(shop.id),
                    'shop_id' : shop.id,
                    'name': shop.shop_name
                }
                all_houses.append(shop)

            all_warehouse = Warehouse.objects.all()
            for ware in all_warehouse:
                warehs={
                    'shop_mod_id' : 'wh_'+str(ware.id),
                    'ware_id': ware.id,
                    'name': ware.warehouse_name
                }
                
                all_houses.append(warehs)

            return Response ({
                'success': True,
                'data': all_houses
            })
        except Exception as e:
            return Response ({
                'success': False,
                'message': e.args[0]
            })

def data_insertion(setter,datas,house_data, number):
    is_approve = False
    if setter[0]=='sh':
        try:
            shop_data_setter = ShopInfo.objects.get(specification_id = datas['specification_id'], shop_id = int(setter[1]))
        except:
            shop_data_setter = None

        if shop_data_setter:
            new_qty = shop_data_setter.quantity+datas['approved_qty']
            shop_data_setter.quantity=new_qty
            shop_data_setter.save()
        else:
            shop_information = ShopInfo.objects.create(
                shop_id = int(setter[1]),
                specification_id =  datas['specification_id'],
                quantity = datas['approved_qty']
            )
            shop_information.save()

        house_data.quantity = house_data.quantity-datas['approved_qty']
        inv_data_setter = inventory_report.objects.create(
            specification_id = datas['specification_id'],
            credit = datas['approved_qty'],
            shop_id = int(setter[1])
        )
        if number ==0:
            inv_data_getter = inventory_report.objects.create(
                specification_id = datas['specification_id'],
                debit = datas['approved_qty'],
                shop_id = house_data.id
            )
        elif number == 1:
            inv_data_getter = inventory_report.objects.create(
                specification_id = datas['specification_id'],
                debit = datas['approved_qty'],
                warehouse_id = house_data.id
            )
        
        house_data.save()
        inv_data_setter.save()
        inv_data_getter.save()
        is_approve = True
       
    elif setter[0]=='wh':
        try:
            ware_data_setter = WarehouseInfo.objects.get(specification_id = datas['specification_id'], warehouse_id = int(setter[1]))
        except Exception as e:
            ware_data_setter = None
        if ware_data_setter:
            ware_data_setter.quantity = ware_data_setter.quantity+datas['approved_qty']
            ware_data_setter.save()
        else:
            ware_information = WarehouseInfo.objects.create(
                warehouse_id = int(setter[1]),
                specification_id =  datas['specification_id'],
                quantity = datas['approved_qty']
            )
            ware_information.save()
        
        house_data.quantity = house_data.quantity-datas['approved_qty']
        inv_data_setter = inventory_report.objects.create(
            specification_id = datas['specification_id'],
            credit = datas['approved_qty'],
            warehouse_id = int(setter[1])
        )
        if number ==0:
            inv_data_getter = inventory_report.objects.create(
                specification_id = datas['specification_id'],
                debit = datas['approved_qty'],
                shop_id = house_data.id
            )
        elif number == 1:
            inv_data_getter = inventory_report.objects.create(
                specification_id = datas['specification_id'],
                debit = datas['approved_qty'],
                warehouse_id = house_data.id
            )
        house_data.save()
        inv_data_setter.save()
        inv_data_getter.save()
        is_approve = True

    if is_approve:
        return True
    else:
        return False

@api_view (["GET","POST"])
def attend_transfer_product (request):
    if request.method == 'POST':
        try:
            data_val = request.data
            # data_val = {
            #     'transfer_id': 12,
            #     'status' : 'Approved',
            #     'approve_data':[
            #         {
            #             'specification_id': 390,
            #             'approved_qty' :1,
            #             'approved_user': 1
            #         },
            #         {
            #             'specification_id': 377,
            #             'approved_qty' :1,
            #             'approved_user': 1
            #         },
            #         {
            #             'specification_id': 375,
            #             'approved_qty' :3,
            #             'approved_user': 1
            #         },
            #     ]
            # }
            try:
                trans = TransferRequest.objects.get(id =int(data_val['transfer_id']),status = 'Pending')
            except Exception as e:
                # print(e)
                trans = None

            log_report = []
            is_approve = False
            if trans:
                for datas in data_val['approve_data']:
                    try:
                        trans_pro = TransferProductSpec.objects.get(transfer_id = data_val['transfer_id'],specification_id = datas['specification_id'])
                    except Exception as e:
                        trans_pro = None
                    if trans_pro:
                        getter = trans.request_getter
                        getter = getter.split("_")
                        setter = trans.request_setter
                        setter = setter.split("_")
                        is_approve = False
                        if getter[0]=='sh':
                            try:
                                shop_data= ShopInfo.objects.get(specification_id = datas['specification_id'],shop_id = int(getter[1]))
                            except Exception as e:
                                shop_data = None
                            if shop_data:
                                existing_qty = shop_data.quantity
                                if existing_qty>=datas['approved_qty']:
                                    res_val = data_insertion(setter,datas,shop_data,0)
                                    if res_val:
                                        trans_pro.approved_qty = datas['approved_qty']
                                        trans_pro.approved_user = datas['approved_user']
                                        trans_pro.save()
                                        is_approve = True
                                    else:
                                        log_list={
                                            'transfer_id': data_val['transfer_id'],
                                            'specification_id': datas['specification_id'],
                                            'message': "Error!! Data could not be updated !!"
                                        }
                                        log_report.append(log_list)
                                else:
                                    log_list={
                                        'transfer_id': data_val['transfer_id'],
                                        'specification_id': datas['specification_id'],
                                        'message': "Error!! Quantity Exceeds than itself has !!"
                                    }
                                    log_report.append(log_list)

                        elif getter[0]=='wh':
                            try:
                                ware_data = WarehouseInfo.objects.get(specification_id = datas['specification_id'],warehouse_id = int(getter[1]))
                            except Exception as e:
                                ware_data = None
                            if ware_data:
                                existing_qty = ware_data.quantity
                                if existing_qty>= datas['approved_qty']:
                                    res_val = data_insertion(setter,datas,ware_data,1)
                                    if res_val:
                                        trans_pro.approved_qty = datas['approved_qty']
                                        trans_pro.approved_user = datas['approved_user']
                                        trans_pro.save()
                                        is_approve = True
                                    else:
                                        log_list={
                                            'transfer_id': data_val['transfer_id'],
                                            'specification_id': datas['specification_id'],
                                            'message': "Error!! Data could not be updated !!"
                                        }
                                        log_report.append(log_list)

                                else:
                                    log_list={
                                        'transfer_id': data_val['transfer_id'],
                                        'specification_id': datas['specification_id'],
                                        'message': "Error!! Quantity Exceeds than itself has !!"
                                    }
                                    log_report.append(log_list)
                    else:
                        log_list={
                            'transfer_id': data_val['transfer_id'],
                            'specification_id': datas['specification_id'],
                            'message': "Error!! Requested specification does not exists !!"
                        }
                        log_report.append(log_list)

                if is_approve:
                    trans.status=data_val['status']
                    trans.save()
                    return Response ({
                        'success': True,
                        'log_report': log_report
                    })
                else:
                    return Response ({
                        'success': False,
                        'message':'Something went wrong',
                        'log_report': log_report
                    })
            else:
                return Response({
                    'success': False,
                    'message': 'Already attended !!',
                    'log': log_report
                })
        except Exception as e:
            return Response({
                'success': False,
                'message': e.args[0]
            })


@api_view (["GET","POST"])
def get_user_info (request, user_id):
    if request.method == 'GET':
        try:
            manager_data = Managers_list.objects.filter(user_id = user_id)
            all_houses = []
            all_shops = []
            info_data = {}
            for res in manager_data:
                # print("data res", res.is_active)
                if res.shop_id != -1:
                    shop_info = Shop.objects.filter(id = res.shop_id)
                    if shop_info.exists():
                        shop_data = serialize('json', shop_info,fields=('id','shop_name','shop_location'))
                        shop_data=json.loads(shop_data)
                        shop_data[0]['fields'].update({'shop_id':shop_data[0]['pk'], 'manager_id': res.id})
                        # print(shop_data[0]['fields'])
                        info_data ={
                            'manager_id': res.id,
                            'name': shop_data[0]['fields']['shop_name'],
                            'location': shop_data[0]['fields']['shop_location'],
                            'id': shop_data[0]['pk'],
                            'number': 0,
                            'user_id': user_id,
                            'active': res.is_active
                        }
                        all_shops.append(info_data)

                if res.warehouse_id != -1:
                    ware_info = Warehouse.objects.filter(id = res.warehouse_id)
                    if ware_info.exists():
                        ware_data = serialize('json', ware_info,fields=('id','warehouse_name','warehouse_location'))
                        ware_data=json.loads(ware_data)
                        ware_data[0]['fields'].update({'warehouse_id':ware_data[0]['pk'],'manager_id': res.id})
                        info_data ={
                            'manager_id': res.id,
                            'name': ware_data[0]['fields']['warehouse_name'],
                            'location': ware_data[0]['fields']['warehouse_location'],
                            'id': ware_data[0]['pk'],
                            'number': 1,
                            'user_id': user_id,
                            'active': res.is_active
                        }
                        all_shops.append(info_data)
            return Response({
                'success': True,
                'houses': all_shops
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': e.args[0]
            })


def get_shop_info(id_val):
    try:
       shop_data = Shop.objects.get(id=id_val)
    except:
        shop_data = None
    
    if shop_data:
        return shop_data.shop_name, shop_data.shop_location
    else:
        return " ", " "

def get_warehouse_info(id_val):
    try:
       ware_data = Warehouse.objects.get(id=id_val)
    except:
        ware_data = None
    
    if ware_data:
        return ware_data.warehouse_name, ware_data.warehouse_location
    else:
        return " ", " "

@api_view (["GET","POST"])
def all_transfer_data_setter (request,number,house_id):
    if request.method == 'GET':
        all_info = []
        name = ''
        location =''
        if number == 0:
            request_setter = 'sh_'+str(house_id)
        if number ==1:
            request_setter = 'wh_'+str(house_id)
        tans_data = TransferRequest.objects.filter(request_setter=request_setter).exclude(status ='Pending')
        tans_data = serialize('json', tans_data,fields=('date','request_setter','request_getter','status'))
        tans_data=json.loads(tans_data)
        for val in tans_data:
            data_val = val['fields']['request_getter']
            data_val=data_val.split("_")
            if data_val[0]=='sh':
                name, location = get_shop_info(int(data_val[1]))
                print(name, location)
            if data_val[0]=='wh':
                name, location = get_warehouse_info(int(data_val[1]))
            val['fields'].update({'getter_name':name, 'getter_location':location,'trans_id': val['pk']})
            all_info.append(val['fields'])
        return Response ({
            'success': True,
            'data': all_info
        })
    
@api_view (["GET","POST"])
def get_pending_transfer_data(request,number,house_id):
    if request.method == 'GET':
        try:
            name =''
            location = ''
            all_requests=[]
            if number ==0:
                request_getter = 'sh_'+str(house_id)
            if number ==1:
                request_getter = 'wh_'+str(house_id)
            trans_req = TransferRequest.objects.filter(request_getter=request_getter,status = 'Pending')
            for reqsts in trans_req:
                setter = reqsts.request_setter
                setter = setter.split('_')
                if setter[0]=='sh':
                    name,location = get_shop_info(int(setter[1]))
                if setter[0]=='wh':
                    name,location = get_warehouse_info(int(setter[1]))
                requests_info = {
                    'name': name,
                    'locaton': location,
                    'date': reqsts.date,
                    'transfer_id': reqsts.id,
                    'status': reqsts.status
                }
                all_requests.append(requests_info)

            return Response ({
                'success': True,
                'data': all_requests
            })
        except Exception as e:
            return Response ({
                'success': False,
                'message': e.args[0]
            })
@api_view (["GET","POST"])
def get_particular_transfer_products (request,trans_id):
    if request.method == 'GET':
        try:
            trans_pro_spec = TransferProductSpec.objects.filter (transfer_id = trans_id)
            res_data = unattend_details (trans_pro_spec,3)
            return Response ({
                'success': True,
                'data': res_data
            })
        except Exception as e:
            return Response ({
                'success': False,
                'message': e.args[0]
            })
       
@api_view (["GET","POST"])
def all_transfer_data_getter (request,number,house_id):
    if request.method == 'GET':
        all_info = []
        name = ''
        location =''
        if number == 0:
            request_getter = 'sh_'+str(house_id)
        if number ==1:
            request_getter = 'wh_'+str(house_id)
        tans_data = TransferRequest.objects.filter(request_getter=request_getter).exclude(status ='Pending')
        tans_data = serialize('json', tans_data,fields=('date','request_setter','request_getter','status'))
        tans_data=json.loads(tans_data)
        for val in tans_data:
            data_val = val['fields']['request_setter']
            data_val=data_val.split("_")
            if data_val[0]=='sh':
                name, location = get_shop_info(int(data_val[1]))
                print(name, location)
            if data_val[0]=='wh':
                name, location = get_warehouse_info(int(data_val[1]))
            val['fields'].update({'setter_name':name, 'setter_location':location,'trans_id': val['pk']})
            all_info.append(val['fields'])
        return Response ({
            'success': True,
            'data': all_info
        })