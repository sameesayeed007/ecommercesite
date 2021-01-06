from django.shortcuts import render,redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
import datetime
from kombu.utils import json
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from random import randint
from django.db import connection
import requests
from django.contrib.sessions.models import Session
from django.db.models.functions import Lower
import hashlib 
site_path = "http://instapay.com.bd/"
class paymentInformation:
    def __init__ (self, store_info, api_key):
        self.store_info = store_info
        self.api_key = api_key
        self.validity={}
        self.store_page={}
        self.customer={}
        self.payment={}
        self.product_details =[]
    def store_page_url_info(self,success_page_url,unsuccess_page_url,cancel_page_url,failure_page_url,special_notification_url):
        store_data={
            'success':success_page_url,
            'unsuccess':unsuccess_page_url,
            'cancel': cancel_page_url,
            'failure':failure_page_url,
            'special':special_notification_url
        }
        self.store_page=store_data
    def customer_information(self,name,email,address,city,post_code,country,phone):
        customer_data={
            'name':name,
            'email':email,
            'address_1': address,
            'city':city,
            'post_code':post_code,
            'country':country,
            'phone':phone
        }
        self.customer=customer_data
    def payment_information(self,total_amount,currency,product_category,number_of_items,shipping_method,invoice_number,product_details):
        payment_data={
            'total_amount':total_amount,
            'currency':currency,
            'product_category': product_category,
            'number_of_items':number_of_items,
            'shipping_method':shipping_method,
            'invoice_number':invoice_number         
        }
        self.product_details = product_details
        # print("alhamdulliah value is here 8888888888888")
        # print(self.product_details)
        self.payment=payment_data
    def validate_user (self):
        url_validate = site_path+ "valid_credit/"
        url_customer = site_path+ "customer_insertion/"
        url_page = site_path+ "update_page_urls/"
        url_payment = site_path + "payment_info_insertion/"
        url_session = site_path + "insert_session/"
        url_product_details = site_path + "insert_details/"
        customer_id = -1
        value = requests.post(url = url_validate,data = {'store':self.store_info, 'Api_key':self.api_key}) 
        self.validity=value.json()
        try:
            if self.validity['success']:
                self.customer.update({'user_id':self.validity['user_id']})
                value_customer = requests.post(url = url_customer,data = self.customer) 
                customer_res= value_customer.json()
                customer_id = customer_res['data']['id']
                self.store_page.update({'user_id':self.validity['user_id']})
                value_urls = requests.post(url = url_page,data = self.store_page)
                value_urls_page=value_urls.json()
                self.payment.update({'customer':customer_id})
                value_payment = requests.post(url = url_payment,data = self.payment)
                value_payment_response = value_payment.json()
                for details_val in self.product_details:
                    details_val.update({'Payment_info':value_payment_response['data']['id']})
                    details_urls = requests.post(url = url_product_details,data = details_val)
                if value_urls_page['success'] and value_payment_response['success']:
                    session_key = self.customer['name']+"-"+str(datetime.now().time())+"-"+str(datetime.now().date())+"-"+str(customer_id)
                    session_data={'session_key':session_key, 'session_time' : 600, 
                                'created_at': datetime.now(),'customer':customer_id, 'invoice_number': self.payment['invoice_number']}
                    value_session = requests.post(url = url_session,data = session_data)
                    return {
                        'success': True,
                        'url_path': site_path+'url_path/'+session_key +"/",
                        'transaction':session_key
                    }
                else:
                    if customer_id > 0:
                        url_delte_customer = site_path + "delete_customer_info/"+str(customer_id)+'/'
                        value_urls = requests.post(url = url_delte_customer)
                        return {
                            'success': False,
                            'message': 'Something went wrong !!'
                        }
            else:
                return {
                            'success': False,
                            'message': 'Something went wrong !!'
                        }
        except:
             if customer_id > 0:
                url_delte_customer = site_path + "delete_customer_info/"+str(customer_id)+'/'
                value_urls = requests.post(url = url_delte_customer)
                return {
                    'success': False,
                    'message': 'Something went wrong !!'
                }