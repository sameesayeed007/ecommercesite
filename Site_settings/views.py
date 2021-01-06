from django.http.request import QueryDict
from django.shortcuts import render
from rest_framework.decorators import api_view
from Intense.models import CompanyInfo, Banner, RolesPermissions, OTP_track, Banner_Image, Currency, Settings, Theme, APIs, FAQ, ContactUs, Product, inventory_report , ProductSpecification
from .serializers import CompanyInfoSerializer, BannerSerializer, RolesPermissionsSerializer, BannerImageSerializer, CurrencySerializer, SettingsSerializer 
from .serializers import ThemeSerializer, APIsSerializer, FaqSerializer, ContactUsSerializer, ProductPdfSerializer
from Product_details.serializers import InventoryReportSerializer
from rest_framework.response import Response
from rest_framework import status
from Intense.utils import get_image, get_roles_id
import datetime
from django.http.response import JsonResponse

# Create your views here.
from rest_framework.views import APIView
from random import randint
import requests

from django.http import HttpResponse

from django.views.generic import View
from .utails import render_to_pdf , render_to_pdf_product
from django.template.loader import get_template
from django.template.loader import render_to_string 
from xhtml2pdf import pisa


@api_view(["GET", "POST"])
def CompanyInfos(request):
    '''
    This is Compnay Info API.
    This api will be invoked after calling url : localhost:8000/site/info
    This API expected JSON format data. It uses get_image function to resize the logo and icon images.
    This API is developed using rest framework and serializers.
    POST request expected arguments:
        name: CharField, max_length=500,
        logo: ArrayField,
        address: TextField, max_length=1500,
        icon: ArrayField,
        Facebook: CharField,max_length=264,
        twitter : CharField,max_length=264,
        linkedin: CharField,max_length=264,
        youtube: CharField,max_length=264,
        email: CharField,max_length=264,
        phone: CharField,max_length=264,
        help_center: harField,max_length=264,
        About: CharField,max_length=5000,
        policy: ArrayField , max_length = 100000,
        terms_condition: ArrayFiled, max_length=100000,
        role_id : IntegerFiled, max_length= 264,
        slogan: CharField,max_length=264,
        cookies: CharField,max_length=100000

    GET request expected response:
        name: CharField,
        logo: ArrayField,
        address: TextField,
        icon: ArrayField,
        Facebook: CharField,
        twitter : CharField,
        linkedin: CharField,
        youtube: CharField,
        email: CharField,
        phone: CharField,
        help_center: harField,
        About: CharField,
        policy: ArrayField,
        terms_condition: ArrayFiled,
        role_id : IntegerFiled,
        slogan: CharField,
        cookies: CharField

    '''

    data = request.data

    if(request.method == "GET"):
        try:
            queryset = CompanyInfo.objects.all()

        except:
            queryset = None

        if queryset:
            serializers = CompanyInfoSerializer(queryset, many=True)
            return JsonResponse({
            'success': True,
            'message': 'The data is shown below',
            'data': serializers.data
        })

        else:
            return JsonResponse({
            'success': False,
            'message': 'No data is available',
            'data': {}
        })

    elif(request.method == "POST"):

        print(data['terms_condition'])

        terms = data['terms_condition']
        term = terms.split(",")
        print(term)
        # terms = ['fuhfuyhew','fhweyfgewyfgew']

        policy = data['policy']
        policies = policy.split(",")
        print(policies)
        # policies = ['fuhfuyhew','fhweyfgewyfgew']

        # This data will come from frontend API
        Info_Api_data = {'name': data['name'], 'address': data['address'], 'Facebook': data['Facebook'], 'twitter': data['twitter'],
        'linkedin': data['linkedin'], 'youtube': data['youtube'], 'email': data['email'], 'phone': data['phone'], 'help_center': data['help_center'], 'About': data['About'],
        'policy': policies, 'terms_condition': term, 'role_id': 1, 'slogan': data['slogan'], 'cookies': 'fdfdfd'}
        # est = request.data.get('logo')
        # print(request.data)
        # print(est)
        # print(type(est))
        # print(Info_Api_data)
        serializers = CompanyInfoSerializer(data=Info_Api_data)
        # print(serializers)
        if(serializers.is_valid()):
            print("Hochche")
            serializers.save()
            return Response({
                'success': True,
                'message': 'Data has been retrived successfully',
                'data': serializers.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializers.errors)


@api_view(['POST', ])
def add_company_info(request):

    data = request.data

    policy = data['policy']
    # policies = policy.split(",")

    term = data['terms_condition']
    # terms = term.split(",")

    Info_Api_data = {'name': data['name'], 'address': data['address'], 'Facebook': data['Facebook'], 'twitter': data['twitter'],
        'linkedin': data['linkedin'], 'youtube': data['youtube'], 'email': data['email'], 'phone': data['phone'], 'help_center': data['help_center'], 'About': data['About'],
        'policy': policy, 'terms_condition': term, 'role_id': 1, 'slogan': data['slogan'], 'cookies': data['cookies']}

    try:

        company = CompanyInfo.objects.all().last()

    except:

        company = None

    if company:

        company_serializers = CompanyInfoSerializer(
            company, data=Info_Api_data)
        if company_serializers.is_valid():
            company_serializers.save()
            return JsonResponse({'success': True, 'message': 'The info has been updated', 'data': company_serializers.data})

        else:
            print(company_serializers.errors)
            return JsonResponse({'success': False, 'message': 'The info could not be updated'})

    else:
        # Create a new company

        company_serializers = CompanyInfoSerializer(data=Info_Api_data)
        if company_serializers.is_valid():

            company_serializers.save()
            return JsonResponse({'success': True, 'message': 'The info has been created', 'data': company_serializers.data})

        else:

            print(company_serializers.errors)
            return JsonResponse({'success': False, 'message': 'The compnay info could not be created'})


@api_view(['POST', ])
def update_CompanyInfos(request):
    '''
        This Api is for update a particular company information. It is assumes that, for a particular company there will be exactly one information.
        In case of multiple information, always it will retrive last added information and will be availabe for update.
        Calling  http://127.0.0.1:8000/site/update_info will invoke this Api.

    '''

    try:
        print("hdwfubgyubfgbguyb")
        queryset = CompanyInfo.objects.all().last()
        print(queryset)
        print("hdwfubgyubfgbguyb")

    except:
        queryset = None

    if queryset:

        serializers = CompanyInfoSerializer(queryset, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse({
            'success': True,
            'message': 'The data is shown below',
            'data': serializers.data
        })

        else:

            return JsonResponse({
            'success': False,
            'message': 'No data is available',
            'data': {}
        })

    else:

        return JsonResponse({
        'success': False,
        'message': 'No data is available',
        'data': {}
    })


@api_view(['POST', 'GET'])
def update_CompanyInfo(request):
    '''
        This Api is for update a particular company information. It is assumes that, for a particular company there will be exactly one information.
        In case of multiple information, always it will retrive last added information and will be availabe for update.
        Calling  http://127.0.0.1:8000/site/update_info will invoke this Api.

    '''
    if request.method == 'GET':
        try:
            queryset = CompanyInfo.objects.all()

        except:
            queryset = None

        if queryset:

            serializers = CompanyInfoSerializer(queryset, many=False)
            return JsonResponse({
            'success': True,
            'message': 'The data is shown below',
            'data': serializers.data
        })

        else:

            return JsonResponse({
            'success': False,
            'message': 'No data is available',
            'data': {}
        })

    elif request.method == "POST":

        try:
            serializers = CompanyInfoSerializer(queryset, data=request.data)
            if(serializers.is_valid()):
                serializers.save()
                return Response({
                'success': True,
                'message': 'Data has been retrived successfully',
                'data': serializers.data
            }, status=status.HTTP_201_CREATED)
            return Response(serializers.errors)
        except:

            return Response({
            'success': True,
            'message': 'No data is available',
            'data': {}
        }, status=status.HTTP_201_CREATED)


@api_view(['POST', 'GET'])
def delete_CompanyInfos(request, info_id):

    # This API is for deleting company informations.
    # This API will be invoked after calling : http://127.0.0.1:8000/site/delete_info/1/
    # dmin will have the permission to delete and add company informations.
    # If requested information is not present in the database then this API will through a message saying there is no information.
    # If the information is present this will delete the requested information and after deleting it will through successfull message.

    try:
        companyInfo = CompanyInfo.objects.get(pk=info_id)
        if request.method == 'POST':
            companyInfo.delete()
            return Response({'message': 'Company Informations is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except:
        return Response({'message': 'There is no infomation'})


@api_view(["POST", ])
def change_status(request, banner_id):

    try:
        banner = Banner.objects.get(id=banner_id)

    except:

        banner = None

    print(banner)

    if banner:

        banner_status = banner.is_active
        print(banner_status)

        if banner_status == True:
            banner.is_active = False
            banner.save()

        elif banner_status == False:

            banner.is_active = True
            banner.save()

        print(banner.is_active)

        serializers = BannerSerializer(banner, many=False)
        # banner_ids = banner.values_list('id' , flat = True)
        # image_serializers = []
        # for i in range(len(banner_ids)):

        #     try:
        #         banner_image = Banner_Image.objects.filter(Banner_id = banner_ids[i])
        #     except:
        #         banner_image = None
        #     if banner_image is not None:
        #         image_serializer = BannerImageSerializer (banner_image,many = True)
        #         image_serializers += image_serializer.data

        return JsonResponse({'success': True,
                'message': 'The values are inserted below',
                'banner_data': serializers.data})
                # 'images' : image_serializers})

    else:

        return JsonResponse({'success': False, 'message': 'the banner does not exist'})


@api_view(["POST", ])
def change_image_status(request, image_id):

    try:
        banner = Banner_Image.objects.get(id=image_id)

    except:

        banner = None

    print(banner)

    if banner:

        banner_status = banner.is_active
        print(banner_status)

        if banner_status == True:
            banner.is_active = False
            banner.save()

        elif banner_status == False:

            banner.is_active = True
            banner.save()

        print(banner.is_active)

        serializers = BannerImageSerializer(banner, many=False)
        # banner_ids = banner.values_list('id' , flat = True)
        # image_serializers = []
        # for i in range(len(banner_ids)):

        #     try:
        #         banner_image = Banner_Image.objects.filter(Banner_id = banner_ids[i])
        #     except:
        #         banner_image = None
        #     if banner_image is not None:
        #         image_serializer = BannerImageSerializer (banner_image,many = True)
        #         image_serializers += image_serializer.data

        return JsonResponse({'success': True,
                'message': 'The values are inserted below',
                'data': serializers.data})
                # 'images' : image_serializers})

    else:

        return JsonResponse({'success': False, 'message': 'the banner image does not exist'})


@api_view(["GET", "POST"])
def get_Banners(request):
    '''
    This is for getting specific Banner. Site does have multiple banner and in each banner there will be multiple images. While performing the
    Get request it will have following response. While calling this API, desired banner id must need to be sent. Calling http://127.0.0.1:8000/site/banner/14
    will cause to invoke this Api.

    Get Response:
        In get response it will send banner related information as an object and images as an array filed. Follwoing is the get response for tjis Api.

    [
        {
            "id": 14,
            "count": 2,
            "set_time": 3
        },
        [
            {
                "id": 22,
                "Banner_id": 14,
                "image": null,
                "link": "abc.link",
                "content": "content"
            },
            {
                "id": 23,
                "Banner_id": 14,
                "image": null,
                "link": "efg.link",
                "content": "nothing"
            }
        ]
    ]

    '''

    if(request.method == "GET"):
        try:
            queryset = Banner.objects.filter(is_active=True)
            print("banner er eikhane ashtese")
            print(queryset)
        except:
            queryset = None
        if queryset:

            serializers = BannerSerializer(queryset, many=True)
            banner_data = serializers.data
            # banner_ids = queryset.values_list('id' , flat = True)

            # image_serializers = []
            # for i in range(len(banner_ids)):
            #     try:
            #         banner_image = Banner_Image.objects.all()
            #     except:
            #         banner_image = None
            #     if banner_image is not None:
            #         image_serializer = BannerImageSerializer (banner_image,many = True)
            #         image_serializers += image_serializer.data

        else:

            banner_data = []

        try:

            banner_image = Banner_Image.objects.all()

        except:

            banner_image = None

        if banner_image:

            image_serializers = BannerImageSerializer(banner_image, many=True)
            image_data = image_serializers.data

        else:

            image_data = []

            # banner_data = [serializers.data,image_serializers.data]
        return Response({
                'success': True,
                'message': 'The values are inserted below',
                'banner_data': banner_data,
                'images': image_data
                })


@api_view(["GET", "POST"])
def get_specific_Banners(request):
    '''
    This is for getting specific Banner. Site does have multiple banner and in each banner there will be multiple images. While performing the
    Get request it will have following response. While calling this API, desired banner id must need to be sent. Calling http://127.0.0.1:8000/site/banner/14
    will cause to invoke this Api.

    Get Response:
        In get response it will send banner related information as an object and images as an array filed. Follwoing is the get response for tjis Api.

    [
        {
            "id": 14,
            "count": 2,
            "set_time": 3
        },
        [
            {
                "id": 22,
                "Banner_id": 14,
                "image": null,
                "link": "abc.link",
                "content": "content"
            },
            {
                "id": 23,
                "Banner_id": 14,
                "image": null,
                "link": "efg.link",
                "content": "nothing"
            }
        ]
    ]

    '''

    if(request.method == "GET"):
        try:
            queryset = Banner.objects.filter(is_active=True)
            print("banner er eikhane ashtese")
            print(queryset)
        except:
            queryset = None
        if queryset:

            serializers = BannerSerializer(queryset, many=True)
            banner_data = serializers.data
            # banner_ids = queryset.values_list('id' , flat = True)

            # image_serializers = []
            # for i in range(len(banner_ids)):
            #     try:
            #         banner_image = Banner_Image.objects.all()
            #     except:
            #         banner_image = None
            #     if banner_image is not None:
            #         image_serializer = BannerImageSerializer (banner_image,many = True)
            #         image_serializers += image_serializer.data

        else:

            banner_data = []

        try:

            banner_image = Banner_Image.objects.filter(is_active=True)

        except:

            banner_image = None

        if banner_image:

            image_serializers = BannerImageSerializer(banner_image, many=True)
            image_data = image_serializers.data

        else:

            image_data = []

            # banner_data = [serializers.data,image_serializers.data]
        return Response({
                'success': True,
                'message': 'The values are inserted below',
                'banner_data': banner_data,
                'images': image_data
                })


# @api_view (["GET","POST"])
# def get_specific_Banners(request):

#     '''
#     This is for getting specific Banner. Site does have multiple banner and in each banner there will be multiple images. While performing the
#     Get request it will have following response. While calling this API, desired banner id must need to be sent. Calling http://127.0.0.1:8000/site/banner/14
#     will cause to invoke this Api.

#     Get Response:
#         In get response it will send banner related information as an object and images as an array filed. Follwoing is the get response for tjis Api.

#     [
#         {
#             "id": 14,
#             "count": 2,
#             "set_time": 3
#         },
#         [
#             {
#                 "id": 22,
#                 "Banner_id": 14,
#                 "image": null,
#                 "link": "abc.link",
#                 "content": "content"
#             },
#             {
#                 "id": 23,
#                 "Banner_id": 14,
#                 "image": null,
#                 "link": "efg.link",
#                 "content": "nothing"
#             }
#         ]
#     ]

#     '''


#     if(request.method == "GET"):
#         try:
#             queryset = Banner.objects.filter(is_active=True)
#             print("banner er eikhane ashtese")
#             print(queryset)
#         except:
#             queryset = None
#         if queryset:

#             serializers = BannerSerializer (queryset,many = True)
#             banner_ids = queryset.values_list('id' , flat = True)

#             image_serializers = []
#             for i in range(len(banner_ids)):
#                 try:
#                     banner_image = Banner_Image.objects.filter(Banner_id = banner_ids[i],is_active=True)
#                 except:
#                     banner_image = None
#                 if banner_image is not None:
#                     image_serializer = BannerImageSerializer (banner_image,many = True)
#                     image_serializers += image_serializer.data

        #     #banner_data = [serializers.data,image_serializers.data]
        #     return Response({
        #         'success': True,
        #         'message': 'The values are inserted below',
        #         'banner_data': serializers.data ,
        #         'images' : image_serializers
        #         })

        # else:
        #     return Response({
        #         'success': False,
        #         'message': 'There are no values to show',
        #         'data': ''
        #         })


@api_view(["GET", "POST"])
def Banner_Insertion(request):
    '''
    This Api is for inserting data into the banner. Data will be inserted here through the Post request. Calling http://127.0.0.1:8000/site/banner_insert/
    will cause to invoke this api. While performing the Post response it expects data according the following structures.

    post Response:
    {   'count': '2',
        'set_time': '3',
        'images':
            [
                {
                    'link': "abc.link",
                    'content': "content"
                },
                {
                    'link': "efg.link",
                    'content': "nothing"
                }
            ]
    }

    '''
    data = request.data
    banner_data = {'count': data['count'],
        'set_time': data['set_time'], 'is_active': True}
    count = data['count']
    if request.method == "POST":

        # banner_data = {'count': api_banner_data['count'], 'set_time': api_banner_data['set_time']}

        # banner_image_data = {'link': data['images[0][link]'], 'content': data['images[0][content]'],'image': data['images[0][image]']}

        # myDict = dict(data.iterlists())
        # print(data)
        # print("fwhbefuwhefuwehfuwehuwehweuhweuhfuwerhfwuehf")
        # print(data['images[0][link]'])
        # print(data['images[0][content]'])
        # print(data['images[0][image]'])
        # print(data['count'])

        # <QueryDict: {'images[0][link]': ['dedsd'], 'images[0][content]': ['sdsadasd'], 'count': ['1'], 'set_time': ['1'], 'images[0][image]': [<InMemoryUploadedFile: banner1.jpeg (image/jpeg)>]}>
        # print(myDict)
        # print(request.data.get('count'))
        # print(request.data.get('set_time'))
        # print(request.data.get('images'))
        # print("###############################")
        # print(request.data.get('count')

        try:

            banner = Banner.objects.create(
                count=data['count'], set_time=data['set_time'], is_active=True)
            banner_serializer = BannerSerializer(banner, data=banner_data)
            if(banner_serializer.is_valid()):

                banner_serializer.save()

            banner_id = Banner.objects.latest('id')
            bannerid = banner_id.id
            # print(bannerid)
            for i in range(int(count)):

                link = data['images['+str(i)+'][link]']

                content = data['images['+str(i)+'][content]']
                image = data['images['+str(i)+'][image]']
                banner_image_data = {
                    'link': link, 'content': content, 'image': image, 'is_active': True}
                banner_image = Banner_Image.objects.create(
                    Banner_id=bannerid, link=link, content=content, image=image, is_active=True)
                banner_image.save()
                banner_image_serializer = BannerImageSerializer(
                    banner_image, data=banner_image_data)
                if(banner_image_serializer.is_valid()):
                    banner_image_serializer.save()
        # for val in request.data.get('image'):
        #     val.update( {'Banner_id' : banner_id.pk} )
        #     banner_serializers = BannerImageSerializer (data= val)
        #     if(banner_serializers.is_valid()):
        #         banner_serializers.save()
            return Response({
                'success': True,
                'message': 'Value successfully added',
                })

        except:
            banner_image = Banner_image.objects.filter(Banner_id=bannerid)
            if banner_image.exists():
                banner_image.delete()

            banner = Banner.objects.filter(id=bannerid)
            if banner.exists():
                banner.delete()

            return Response({
                'success': False,
                'message': 'Banner insertion could not be completed'
                })


@api_view(["GET", "POST"])
def Banner_value_update(request, banner_id):
    '''
    This field is to update banner related information like updating time. Calling http://127.0.0.1:8000/site/banner_value_update/16 will cause to invoke
    this Api. While calling this Api, desired banner id needs to be sent.

    Get Response:
        {
            "id": 16,
            "count": 500,
            "set_time": 3
        }
    Post Response:
        After updating set time the response will be:
        {
            "id": 16,
            "count": 500,
            "set_time": 30
        }
    '''
    try:
        queryset = Banner.objects.get(pk=banner_id)
    except:
        return Response({'message': 'There is no value'})

    if(request.method == "GET"):
        serializers = BannerSerializer(queryset, many=False)
        return Response({
                'success': True,
                'data': serializers.data,
                'message': 'Values are shown below',
                })

    if request.method == "POST":
        serializers = BannerSerializer(queryset, data=request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response({
                'success': True,
                'message': 'Value successfully added'
                }, status=status.HTTP_201_CREATED)
        return Response(serializers.errors)


@api_view(["GET", "POST"])
def Banner_image_add(request, banner_id):
    '''
    This Api is for adding banner image in an existing banner. Calling http://127.0.0.1:8000/site/banner_img_update/16 will cause to invoke this Api.
    While calling this Api, banner_id must need to be sent in parameter.
    '''
    try:
        banner_image = Banner_Image.objects.filter(Banner_id=banner_id)
    except:
        return Response({'message': 'There is no value'})

    if(request.method == "GET"):
        serializers = BannerImageSerializer(banner_image, many=True)
        return Response({
                'success': True,
                'data': serializers.data,
                'message': 'Values are shown below'
                })

    if request.method == "POST":
        value = request.data.copy()
        value.update({'Banner_id': banner_id})
        serializers = BannerImageSerializer(data=value)
        if(serializers.is_valid()):
            serializers.save()
            return Response({
                'success': True,
                'data': serializers.data,
                'message': 'Values are shown below',
                }, status=status.HTTP_201_CREATED)
        return Response(serializers.errors)


@api_view(["GET", "POST"])
def Banner_image_delete(request, banner_id, img_id):
    '''
    This Api is for deleting specific banner image within the banner. While performing this operation, banner id, in which that specific image belongs
    and the specific image id must need to be provided. Calling http://127.0.0.1:8000/site/banner_img_delete/16/30/ will cause to invoke this Api.
    '''

    banner_image = Banner_Image.objects.filter(Banner_id=banner_id, pk=img_id)
    print(banner_image)
    if request.method == "POST":
        if banner_image.exists():
            banner_image.delete()
            return Response({'message': 'Banner image is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:

            return Response({'message': 'There is no value'})


@api_view(['POST', 'GET'])
def delete_Banner(request, banner_id):
    '''
    This API for deleting the banner. As there will be only one banner for each site, therefore calling this API will cause to delete
    all the banner related information. If the delete action is performed, this will send a message to user.
    This API will be invoked after calling : http://127.0.0.1:8000/site/delete_banner/
    '''
    try:
        Banners = Banner.objects.get(pk=banner_id)
        banner_image = Banner_Image.objects.filter(Banner_id=banner_id)
        if request.method == 'POST':
            Banners.delete()
            banner_image.delete()
            return Response({'message': 'Banner is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except Banner.DoesNotExist:
        return Response({'message': 'There is no infomation to delete'})


@api_view(["GET", "POST"])
def All_Roles(request):
    '''
    This is Roles and Permissions API.
    This api will be invoked after calling url : localhost:8000/site/roles
    All the field of this api is expected from front end.
    This API is developed using rest framework and serializers.

    POST request expected arguments:
        roleType: CharField, max_length=264,
        roleDetails: CharField, max_length=264

    GET request expected arguments:
        roleType: CharField,
        roleDetails: CharField
    '''
    if(request.method == "GET"):
        queryset = RolesPermissions.objects.all()
        serializers = RolesPermissionsSerializer(queryset, many=True)
        return Response({
                'success': True,
                'data': serializers.data,
                'message': 'Values are shown below',
                })

    elif(request.method == "POST"):
        serializers = RolesPermissionsSerializer(data=request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response({
                'success': True,
                'data': serializers.data,
                'message': 'Values are successfully inserted',
                }, status=status.HTTP_201_CREATED)
        return Response(serializers.errors)


@api_view(["GET", "POST"])
def Specific_Roles(request, roles_id):
    '''
    This API is for retriving and updating a particular roles information.
    This api will be invoked after calling url : localhost:8000/site/specific_roles/id
    This API will first check whether particular roles is exists in the database or not. If roles does not exist, it will
    through an error. If role is found, it will retrive and update the necessary informations.
    This API is developed using rest framework and serializers.

    POST request expected arguments:
        roleType: CharField, max_length=264,
        roleDetails: CharField, max_length=264

    GET request expected arguments:
        roleType: CharField,
        roleDetails: CharField
    '''
    try:
        Roles = RolesPermissions.objects.get(pk=roles_id)
    except:
        return Response({'message': 'This Role does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if(request.method == "GET"):
        Roles_serializer = RolesPermissionsSerializer(Roles, many=False)
        return Response({
                'success': True,
                'data': Roles_serializer.data,
                'message': 'Values are shown below',
                })

    elif(request.method == "POST"):
        Roles = RolesPermissions.objects.get(pk=roles_id)
        Roles_serializers = RolesPermissionsSerializer(
            Roles, data=request.data)
        if(Roles_serializers.is_valid()):
            Roles_serializers.save()
            return Response({
                'success': True,
                'data': Roles_serializers.data,
                'message': 'Values are inserted below',
                }, status=status.HTTP_201_CREATED)
        return Response(Roles_serializers.errors)


@api_view(['POST', 'GET'])
def delete_Roles(request, role_id):

    # This API for deleting the Roles. This API will delted the Roles information based on the provided id.
    # If the delete action is performed, this will send a message to user.
    # This API will be invoked after calling : http://127.0.0.1:8000/site/delete_role/1/

    Roles = RolesPermissions.objects.filter(pk=role_id)
    if request.method == 'POST':
        if Roles.exists():
            Roles.delete()
            return Response({'message': 'Roles and Permissions has been deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'There is no Roles and Permissions infomation to delete'})


# ------------------------------------------------------------------------------------------------------------------------------------
@api_view(["GET", "POST"])
def Currency_value(request):
    '''
    This API is for adding and retriving values to currency table. The default currency of a site will be taka and Currency database will
    store currecncy value compare will per unit taka. For example, 1 dollar = 85 taka. It will store currency type as dollar and value 85.
    For default value will be 1. After being called, this API will provide all the values from the currency table.
    This API can be called using : http://127.0.0.1:8000/site/currency/
    GET Response:
        After the get response this will return all the information of the currency table database including the follwoing fields:
        currency_type : deafult taka,
        value : FloatField,
        dates : date and Time field

    POST Response:
        Post response will store the value into the currency table. The fileds are following:
        currency_type : CharField (default taka)
        value : float (for taka it will be deafult 01.00)
        dates: Date and Time field,
        role_id : IntegerField(This will act as a foriegn key)
    '''
    currency_api_data = {'currency_type': "Dollar",
        'value': "85.00", 'dates': "12-08-2020", 'role_id': "Admin"}
    if(request.method == "GET"):
        currency_data = Currency.objects.all()
        currency_serializers = CurrencySerializer(currency_data, many=True)
        return Response({
                'success': True,
                'data': currency_serializers.data,
                'message': 'Values are shown below',
                })

    elif(request.method == "POST"):
        currency_data = {}
        if(get_roles_id(currency_api_data['role_id']) is not None):
            currency_data = {'currency_type': currency_api_data['currency_type'], 'value': currency_api_data['value'],
            'dates': currency_api_data['dates'], 'role_id': get_roles_id(currency_api_data['role_id'])}

            currency_serializers = CurrencySerializer(data=request.data)
            if(currency_serializers.is_valid()):
                currency_serializers.save()
                return Response({
                'success': True,
                'data': currency_serializers.data,
                'message': 'Values are shown below',
                }, status=status.HTTP_201_CREATED)
            return Response(currency_serializers.errors)
        else:
            return Response({'message': 'Please make sure you have Roles value'})


@api_view(["GET", "POST"])
def latest_Currency_value(request):
    '''
    This API is for getting the last currency data based on date. This is required while calculating the product price. Currency table
    will have multiple currency values but for the calculation always latest data will be used.
    This API will be invoked after calling : http://127.0.0.1:8000/site/last_currency/
    GET Response:
        After the get response this will return the last entry of the currency table database including the follwoing fields:
        currency_type : deafult taka,
        value : FloatField,
        dates : date and Time field
    '''
    if(request.method == "GET"):
        last_currency_data = Currency.objects.latest("dates")
        last_currency_serializers = CurrencySerializer(last_currency_data)
        return Response({
                'success': True,
                'data': last_currency_serializers.data,
                'message': 'Values are shown below',
                })


@api_view(["GET", "POST"])
def Specific_Currency_get_delete(request, currency_id):
    '''
    This is for retriving and deleting a particular currency data. Admin will have the access to retrive and delete the data.
    This API will be invoked after calling: http://127.0.0.1:8000/site/specific_currency/6
    GET Response:
        If the requested value exists it will send all the data of that specific id. If requested data is not present, it will through a message
        as a response.
    POST Response:
        After successfully deleting a value, it will send a successful message as a response.
    '''
    try:
        currency_value = Currency.objects.get(pk=currency_id)
    except:
        return Response({'message': 'This value does not exist'})

    if request.method == "GET":

        currency_serializer_value = CurrencySerializer(
            currency_value, many=False)
        return Response({
                'success': True,
                'data': currency_serializer_value.data,
                'message': 'Values are shown below',
                })

    elif request.method == 'POST':
        currency_value.delete()
        return Response({'message': 'Currency value has been deleted successfully!'})


# -----------------------------------------------------------------------------------------------

@api_view(["GET", "POST"])
def all_theme_infos(request):
    '''
    This API is for inserting and retreiving all the theme infos data. Site admin or anyone having special permission will have access to
    add and change the theme. If no theme is added, the deafult theme will be used as the site theme.
    This API will be revoked after calling : http://127.0.0.1:8000/site/theme/ . Simply calling this API will cause to integrate with front end.
    GET Response:
        id : IntegerField (This is the primary key)
        name : Charfield (This is the name of the theme)
        details : CharFiled (Any description related the theme or pros and cons will be in this column.)

    POST Response:
        This API expected following fields while integrating with the others throug post request.
        name : CharField (CharFiled containg name must need to provide)
        details : CharFiled (It expects details to be provided while integrating through Post request)

    '''
    if request.method == 'GET':
        Theme_value = Theme.objects.all()
        theme_serializer_value = ThemeSerializer(Theme_value, many=True)
        return Response(theme_serializer_value.data)

    if request.method == 'POST':
        theme_serializers_value = ThemeSerializer(data=request.data)
        if(theme_serializers_value.is_valid()):
            theme_serializers_value.save()
            return Response(theme_serializers_value.data, status=status.HTTP_201_CREATED)
        return Response(theme_serializers_value.errors)


@api_view(["GET", "POST"])
def Specific_theme(request, theme_id):
    '''
    This API is for retriving and updating a particular theme data. This Api will find the requested theme through the id number. If it gets the desired
    information it will send it to update via get request and through post request it will update the requested information in a particular data.
    Simply calling http://127.0.0.1:8000/site/specific_theme/1 will cause to integrate this Api.
    GET Response:
        id : IntegerField (This is the primary key of the requested field)
        name : Charfield (This is the name of the theme of the requested field)
        details : CharFiled (Any description related the theme or pros and cons of the requested field will be in this column.)

    POST Response:
        This API expected following fields while making post request after the value updatation.
        name : CharField (CharFiled containg name must need to provide)
        details : CharFiled (It expects details to be provided while integrating through Post request)

    '''

    try:
        theme = Theme.objects.get(pk=theme_id)
    except:
        return Response({'message': 'This Theme does not exist'})

    if(request.method == "GET"):
        themes_serializer = ThemeSerializer(theme, many=False)
        return Response(themes_serializer.data)

    elif(request.method == "POST"):
        themes_serializer = ThemeSerializer(theme, data=request.data)
        if(themes_serializer.is_valid()):
            themes_serializer.save()
            return Response(themes_serializer.data, status=status.HTTP_201_CREATED)
        return Response(themes_serializer.errors)


@api_view(['POST', 'GET'])
def delete_theme(request, theme_id):

    # This API is for deleting a particular theme entity. This Api will find the requested theme through the id number. If it gets the desired
    # information it will delete the information and will send a successful message as response. In case of any failure, it will send an error message
    # as a response. Simply calling http://127.0.0.1:8000/site/theme_delete/1 will cause to integrate this Api.

    try:
        themes_value = Theme.objects.get(pk=theme_id)
        if request.method == 'POST':
            themes_value.delete()
            return Response({'message': 'Theme is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except:
        return Response({'message': 'There is no infomation to delete'})


@api_view(["GET", "POST"])
def all_APIs_infos(request):
    '''
    This Api is for retreving and inserting the third party APIs which are integrated with the site. All the third party integrated Apis will
    be stored in APIs table having name and details information. Admin or individual with special permission will have the access add new integrated API
    in this table through this API or retreving all the third party api related information. Simple calling http://127.0.0.1:8000/site/Api/ will cause
    to integrate this Api.

    GET Response :
        While getting the GET request it will send the following information:
        id : IntegerField ( This is the primary key)
        name : CharField ( This will be the name of the API)
        details : CharField ( This will be the details information of the API)

    POST Response:
        While getting the POST request this api expected following values:
        name : CharField (This will be the name of the API. Basically a string)
        details : Charfield ( This will be the details information of that particular API. This will also be a string)
    '''
    if request.method == 'GET':
        Api_value = APIs.objects.all()
        Api_serializer_value = APIsSerializer(Api_value, many=True)
        return Response({
                'success': True,
                'data': Api_serializer_value.data,
                'message': 'Values are shown below',
                })

    if request.method == 'POST':
        Api_serializer_value = APIsSerializer(data=request.data)
        if(Api_serializer_value.is_valid()):
            Api_serializer_value.save()
            return Response({
                'success': True,
                'data': Api_serializer_value.data,
                'message': 'Values are shown below',
                }, status=status.HTTP_201_CREATED)
        return Response(Api_serializer_value.errors)


@api_view(["GET", "POST"])
def Specific_Api(request, Api_id):
    '''
    This API is for retreiving and updating a particular information of an Api. This Api will find the requested Api through the id number.
    If it gets the desired information it will send it to update via get request and through post request it will update the requested information
    in a particular data. Simply calling http://127.0.0.1:8000/site/specific_Api/1 will cause to integrate this Api.

    GET Response:
        id : IntegerField (This is the primary key of the requested field)
        name : Charfield (This is the name of the theme of the requested field)
        details : CharFiled (Any description related the theme or pros and cons of the requested field will be in this column.)

    POST Response:
        This API expected following fields while making post request after the value updatation.
        name : CharField (CharFiled containg name must need to provide)
        details : CharFiled (It expects details to be provided while integrating through Post request)

    '''

    try:
        Api = APIs.objects.get(pk=Api_id)
    except:
        return Response({'message': 'This Theme does not exist'})

    if(request.method == "GET"):
        Api_serializer_value = APIsSerializer(Api, many=False)
        return Response({
                'success': True,
                'data': Api_serializer_value.data,
                'message': 'Values are shown below',
                })

    elif(request.method == "POST"):
        Api_serializer_value = APIsSerializer(Api, data=request.data)
        if(Api_serializer_value.is_valid()):
            Api_serializer_value.save()
            return Response({
                'success': True,
                'data': Api_serializer_value.data,
                'message': 'Values are shown below',
                }, status=status.HTTP_201_CREATED)
        return Response(Api_serializer_value.errors)


@api_view(['POST', 'GET'])
def delete_Api(request, Api_id):

    # This API is for deleting a particular Api entity. This Api will find the requested Api through the id number. If it gets the desired
    # information it will delete the information and will send a successful message as response. In case of any failure, it will send an error message
    # as a response. Simply calling http://127.0.0.1:8000/site/Api_delete/1 will cause to integrate this Api.

    try:
        Api_value = APIs.objects.get(pk=Api_id)
        if request.method == 'POST':
            Api_value.delete()
            return Response({'message': 'Api is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except:
        return Response({'message': 'There is no infomation to delete'})


@api_view(["GET", "POST"])
def site_all_settings(request):
    '''
    This api is for site settings. All the site related information will be inserted and retreving through this Api. Site settings will be created once
    and there will be delete option. Destroying the site will cause to delete this table. The site related information can be taken while developing the
    site or later via update. Simply calling http://127.0.0.1:8000/site/settings/ will cause to integrate this Api.

    GET response:
        While getting the get response it is expected to return the following fields
        id : IntegerField (This is the primary key)
        tax : FloatFiled (This will be a float value in a percentage. Example : tax = 5 means 5 %. This tax will be applied to all the price of the products)
        vat : FloatFiled (Like tax it will also be in percentage. This will be used to calculate price where required)
        point_value : FloatField (This point is the reward point. The idea here is to add the points based on the purchachisng. And point values need to be
                    converted into taka which will be saved into user wallet. This field will contain the corresponding point values to make a particular
                    amount of money. For example : 1000 points = 10 taka. Here 1000 points will be stored)

        point_converted_value : FloatFiled ( This will store the corresnponding money of the points. from the example 1000 points = 10 taka, it will store
                                10 taka. This value will be used while updating user wallet.)

    POST response:
        While getting the post response this api expect following values:
        tax : FloatField (a value wich will be converted in percentage. example : inserting 5 here means 5%)
        vat : FloatFiled (Same as tax)
        point_value : FloatFiled (Number of point wchi will be converted later to corresponding money and will save in user wallet)
        point_converted_value : FloatField (The amount which will be the value after acheiving a certain amount of point)

    Additionally it expects follwoing two filed. These two will be required to get the corresponding id which will act as the foreign key. The name of
    this two field must be same.
        role : expects a filed name 'role' having the user roles like Admin/ Suppot. using this a query will be perfomred to RolesAndPermission table
               to get the corresponding id. Then the corresponding id will be stored as a foreign key.
        theme : expects a field name 'theme' having the theme name like Dark/Night. like role this will be used to perform query theme table to
                get the corresponding id which will be added to the settings table as foreign key.

    Note: Before inserting the values please make sure, keys which will act as foreign key having proper data in their corresponding table.

    '''
    if request.method == 'GET':
        settings_value = Settings.objects.all()
        settings_serializer_value = SettingsSerializer(
            settings_value, many=True)
        return Response(settings_serializer_value.data)

    if request.method == 'POST':
        # role = request.data['role']
        # theme = request.data['theme']
        try:
            # role_id = RolesPermissions.objects.filter(roleType= role).values('id')
            # theme_id = Theme.objects.filter(name = theme).values('id')

            # settings_values = {'tax': request.data['tax'], 'vat': request.data['vat'], 'role_id': '2', 'point_value': request.data['point_value'],
            # 'point_converted_value':request.data['point_converted_value'],'theme_id': '3'}
            settings_serializers_value = SettingsSerializer(data=request.data)
            if(settings_serializers_value.is_valid()):
                settings_serializers_value.save()
                return Response(settings_serializers_value.data, status=status.HTTP_201_CREATED)
            return Response(settings_serializers_value.errors)
        except:
            return Response({'message': 'It occurs some problem to insert values'})


@api_view(["GET", "POST"])
def settings_update(request, setting_id):
    '''
    This api is for updating the site information. Simply calling http://127.0.0.1:8000/site/update_setting/1 will cause to integrate this Api.

    GET response:
        While getting the get response it is expected to return the following fields of the requested data
        id : IntegerField (This is the primary key)
        tax : FloatFiled (This will be a float value in a percentage. Example : tax = 5 means 5 %. This tax will be applied to all the price of the products)
        vat : FloatFiled (Like tax it will also be in percentage. This will be used to calculate price where required)
        point_value : FloatField (This point is the reward point. The idea here is to add the points based on the purchachisng. And point values need to be
                    converted into taka which will be saved into user wallet. This field will contain the corresponding point values to make a particular
                    amount of money. For example : 1000 points = 10 taka. Here 1000 points will be stored)

        point_converted_value : FloatFiled ( This will store the corresnponding money of the points. from the example 1000 points = 10 taka, it will store
                                10 taka. This value will be used while updating user wallet.)

    POST response:
        While getting the post response this api expect following values:
        tax : FloatField (a value wich will be converted in percentage. example : inserting 5 here means 5%)
        vat : FloatFiled (Same as tax)
        point_value : FloatFiled (Number of point wchi will be converted later to corresponding money and will save in user wallet)
        point_converted_value : FloatField (The amount which will be the value after acheiving a certain amount of point)

    Additionally it expects follwoing two filed. These two will be required to get the corresponding id which will act as the foreign key. The name of
    this two field must be same.
        role : expects a filed name 'role' having the user roles like Admin/ Suppot. using this a query will be perfomred to RolesAndPermission table
               to get the corresponding id. Then the corresponding id will be stored as a foreign key.
        theme : expects a field name 'theme' having the theme name like Dark/Night. like role this will be used to perform query theme table to
                get the corresponding id which will be added to the settings table as foreign key.
    Note: Before inserting the values please make sure, keys which will act as foreign key having proper data in their corresponding table.
    '''

    try:
        setting_values = Settings.objects.get(pk=setting_id)
    except:
        return Response({'message': 'This value does not exist'})

    if(request.method == "GET"):
        setting_serializer_value = SettingsSerializer(
            setting_values, many=False)
        return Response(setting_serializer_value.data)

    elif(request.method == "POST"):
        # role = request.data['role']
        # theme = request.data['theme']
        try:
            # role_id = RolesPermissions.objects.filter(roleType= role).values('id')
            # theme_id = Theme.objects.filter(name = theme).values('id')

            # settings_values = {'tax': request.data['tax'], 'vat': request.data['vat'], 'role_id': '2', 'point_value': request.data['point_value'],
            # 'point_converted_value':request.data['point_converted_value'],'theme_id': '3'}
            settings_serializers_value = SettingsSerializer(
                setting_values, data=request.data)
            if(settings_serializers_value.is_valid()):
                settings_serializers_value.save()
                return Response(settings_serializers_value.data, status=status.HTTP_201_CREATED)
            return Response(settings_serializers_value.errors)
        except:
            return Response({'message': 'Setting values could not be updated'})

# ------------------------------- FAQ --------------------------------------


@api_view(["GET", "POST"])
def Faq_insertion(request):
    '''
    This method is for inserting frequently ask questions. It has only post response. Calling http://127.0.0.1:8000/site/insert_faq/ will cause to invoke
    this Api.
    Fileds:
        'question' : This is CharField. This filed will contain the frequently asked question.
        'ans' : This is also a CharField. This filed will contain the answear of the specific question. In both case admin will have the access
                to add the frequently asking questions and their corresponding answear.
    Expected Post Response:
        {
            "question" : "any question"
            "ans" : "Ans of that corresponding question"
        }
    Successful Post Response:
        {
            "id": 6,
            "question": "What is the return policy",
            "ans": "Thank you for you question. You have to contact within 3 days to our support team.",
            "date": "2020-08-30"
        }
    '''
    if request.method == 'POST':
        try:
            faq_value = FaqSerializer(data=request.data)
            if(faq_value.is_valid()):
                faq_value.save()
                return Response({
                'success': True,
                'data': faq_value.data,
                'message': 'Values are inserted successfully',
                }, status=status.HTTP_201_CREATED)
            return Response(faq_value.errors)
        except:
            return Response({'message': 'It occurs some problem to insert values'})


@api_view(["GET", "POST"])
def show_all_Faq(request):
    '''
    This method is for showing all the frequently asked question and their corresponding answear. Calling http://127.0.0.1:8000/site/show_faq/ will
    cause to invoke this Api. This Api has just Get response.

    Expected data from successful GET Response:
        [
            {
                "id": 2,
                "question": "How is the day?",
                "ans": "Brilliant",
                "date": "2020-08-30"
            },
            {
                "id": 1,
                "question": "Our general rules",
                "ans": "Will be updated very soon",
                "date": "2020-08-30"
            },
            {
                "id": 6,
                "question": "What is the return policy",
                "ans": "Thank you for you question. You have to contact within 3 days to our support team.",
                "date": "2020-08-30"
            }
        ]
    '''
    try:
        if request.method == 'GET':
            faq_value = FAQ.objects.all()
            faq_serializer_value = FaqSerializer(faq_value, many=True)
            return Response({
                'success': True,
                'data': faq_serializer_value.data,
                'message': 'Values are shown',
                })
    except:
        return Response({'message': 'It occurs some problem to show the values'})


@api_view(["GET", "POST"])
def specific_faq(request, faq_id):
    '''
    This is for updating a particular question or answear. The id of that specific question must need to be sent through parameter to get acess
    the request data. Calling http://127.0.0.1:8000/site/specific_faq/1/ will cause to invoke this particular Api. It has both get and post response.
    Successful Get response will provide the stored information correspond to the requested id and through post response the data will be updated.

    Unsuccessful get Response:
        {
            "message": "It occurs some problem"
        }
    Successful Get Response:
        {
            "id": 1,
            "question": "Our general rules",
            "ans": "Will be updated very soon",
            "date": "2020-08-30"
        }
    After updating Successful Post Response:
        {
            "id": 1,
            "question": "Our general rules",
            "ans": "Please follow our general terms and conditions.",
            "date": "2020-08-30"
        }
    '''
    try:
        faq_value = FAQ.objects.get(pk=faq_id)
    except:
        return Response({'message': 'It occurs some problem'})

    if request.method == 'GET':
        faq_serializer_value = FaqSerializer(faq_value, many=False)
        return Response({
                'success': True,
                'data': faq_serializer_value.data,
                'message': 'Values are shown',
                })

    if request.method == 'POST':
        try:
            faq_serializer_value = FaqSerializer(faq_value, data=request.data)
            if(faq_serializer_value.is_valid()):
                faq_serializer_value.save()
                return Response({
                'success': True,
                'data': faq_serializer_value.data,
                'message': 'Values are shown below',
                }, status=status.HTTP_201_CREATED)
            return Response(faq_serializer_value.errors)
        except:
            return Response({'message': 'This value could not be updated'})


@api_view(["GET", "POST"])
def delete_specific_faq(request, faq_id):
    '''
    This is for deleting a particular faq. The value will be deleted through the post response To delete the faq, id of the particular data must need
    to be sent. Calling http://127.0.0.1:8000/site/delete_faq/2/ will cause to invoke this Api.

    Successful Post Response:
        {
            "message": "The value has been deleted successfully"
        }

    Unsuccessful Post Response:
        {
            "message": "It occurs some problem"
        }

    '''
    try:
        faq_value = FAQ.objects.get(pk=faq_id)
    except:
        return Response({'message': 'It occurs some problem'})

    if request.method == 'POST':
        faq_value.delete()
        return Response({'message': 'The value has been deleted successfully'})


@api_view(["GET", "POST"])
def insert_contact(request):

    if request.method == 'POST':
        try:
            contact_value = ContactUsSerializer(data=request.data)
            if(contact_value.is_valid()):
                contact_value.save()
                return Response({
                    'success': True,
                    'message': 'Data has been inserted successfully',
                    'data': contact_value.data
                    }, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'message': 'Data could not record',
                'error': contact_value.errors
                })
        except:
            return Response({
                'success': False,
                'message': 'It occurs some problem to insert values',
                'data': ''
                })


@api_view(["GET", "POST"])
def get_all_contact(request):

    try:
        contact_value = ContactUs.objects.all()
    except:
        return Response({
            'success': False,
            'message': 'Some internal problem occurs',
            'data': ''
            })

    if request.method == 'GET':
        contact_serializer_value = ContactUsSerializer(
            contact_value, many=True)
        return Response({
            'success': True,
            'message': 'Value has been retrieved successfully',
            'data': contact_serializer_value.data
            })


@api_view(["GET", "POST"])
def delete_specific_contactUs(request, contact_id):

    try:
        contact_value = ContactUs.objects.get(pk=contact_id)
    except:
        return Response({
            'success': False,
            'message': 'It occurs some problem',
            'data': ''
            })

    if request.method == 'POST':
        contact_value.delete()
        return Response({
            'success': True,
            'message': 'The value has been deleted successfully'
            })


@api_view(["GET", "POST"])
def get_all_unattended_contact(request):

    try:
        contact_value = ContactUs.objects.filter(is_attended=False)
    except:
        return Response({
            'success': False,
            'message': 'It occurs some problem',
            'data': ''
            })

    if request.method == 'GET':
        contact_serializer_value = ContactUsSerializer(
            contact_value, many=True)
        return Response(
            {
                'success': True,
                'message': 'Value has been retrived successfully.',
                'data': contact_serializer_value.data
            })


@api_view(["GET", "POST"])
def admin_attend_contact(request, contact_id):

    try:
        contact_value = ContactUs.objects.get(pk=contact_id)
    except:
        return Response({'message': 'It occurs some problem'})

    if request.method == 'GET':
        contact_serializer_value = ContactUsSerializer(
            contact_value, many=False)
        return Response(contact_serializer_value.data)

    if request.method == 'POST':
        try:
            if not contact_value.is_attended:
                contact_value.is_attended = True
                contact_value.save()
                return Response({
                    'success': True,
                    'message': 'Thank you for attending'
                    })
            else:
                return Response({
                    'success': False,
                    'message': 'You have already attended this.'
                })
        except:
            return Response({
                'success': False,
                'message': 'Some problems while attending'
                })


class ValidatePhoneSendOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        user = request.data.get('user_id')
        try:
            company_data = CompanyInfo.objects.all()
            if len(company_data) > 0:
                company_name = company_data[0].name
            else:
                company_name = "Test"

            OTP_track_value = OTP_track.objects.filter(
                phone_number=phone, isVerified=True)

            print("otp track", OTP_track_value)
            if len(OTP_track_value) == 0:
                key = random_with_N_digits(4)
                if key:
                    # old = OTP_track.objects.filter(phone_number = phone)
                    obj = OTP_track.objects.create(
                                phone_number=phone,
                                otp_token=key,
                                user_id=user
                            )
                    result = requests.get("http://alphasms.biz/index.php?app=ws&u=sawari&h=a175553f64cd19577d43f2b55c0bf3bb&op=pv&to=" +
                                          phone+"&msg= Your OTP M-"+str(key) + ". Thank you for choosing " + company_name)
                    data = result.json()
                    obj.otp_session_id = str(data['timestamp'])
                    obj.save()
                    return Response({
                            'success': True,
                            'status': 'non_verified',
                            'message': 'OTP sent successfully'
                        })
                else:
                    return Response({
                            'success': False,
                            'detail': 'OTP sending Failed'
                        })
            else:
                    return Response({
                        'success': False,
                        'status': 'verified',
                        'message': 'You are already verified'
                    })
        except:
                return Response({
                    'success': False,
                    'Message': 'Some internal problem '
                    })


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


@api_view(["GET", "POST"])
def otp_validation(request, otp_val, phone, user):
    try:
        if request.method == 'GET':
            OTP_track_value = OTP_track.objects.filter(
                user_id=user, otp_token=otp_val, phone_number=phone)
            if OTP_track_value.exists():
                OTP_track_value_data = OTP_track_value[0]
                # OTP_track_value_data.isVerified = True
                # OTP_track_value_data.save()
                return Response({
                    'success': True,
                    'message': 'Congratulations!! Valid Credential !!',
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Credentials Invalid',
                    })
    except:
        return Response({
            'success': False,
            'message': 'Something went wrong !!'
            })


# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         queryset = Product.objects.all().order_by('-date')
#         product_serializers = ProductPdfSerializer(queryset , many = True)
#         template = get_template('index.html' , ctx)

#         data=product_serializers.data
#         print("html data", data)
#         html = template.render(data)

#         pdf = render_to_pdf('invoice.html', data)
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Product_%s.pdf" %("12341231")
#             content = "inline; filename='%s'" %(filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" %(filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")



# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         report = Product.objects.all().order_by('-date')
#         template_path = 'index.html'
#         html = render_to_string(template_path, {'report': report})
#         pdf = render_to_pdf_product('index.html', report)
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Product_Report_%s.pdf" % ("12341231")
#             content = "inline; filename='%s'" % (filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" % (filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")








# class GeneratePdf(View):

#     def get(self, request, *args, **kwargs):


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

#         try:

#             report = Product.objects.all()

#         except:

#             report = None

#         # Finding out the individual dates

#         if report:
#             main_serializers = ProductPdfSerializer(company_info, many=True)

#             main_data = main_serializers.data

#             report =  main_data
#             company = company_data
#             #print("here is the report", report[0])
#             return JsonResponse({"success":True,"message":"The products dont exist" ,'data':  report})

         
#             # template_path = 'ProductReport.html'
#             # html = render_to_string(template_path, {'report': report , 'company':company})
#             # pdf = render_to_pdf('ProductReport.html', report , company)
#             # if pdf:
#             #     response = HttpResponse(pdf, content_type='application/pdf')
#             #     filename = "Product_Report_%s.pdf" % ("12341231")
#             #     content = "inline; filename='%s'" % (filename)
#             #     download = request.GET.get("download")
#             #     if download:
#             #         content = "attachment; filename='%s'" % (filename)
#             #     response['Content-Disposition'] = content
#             #     return response
#             # return HttpResponse("Not found")

#         else:

#             return HttpResponse({"success": False, "message": "The products dont exist"})


class GeneratePdf(View):

    def get(self, request, *args, **kwargs):


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

        try:

            report = Product.objects.all()

        except:

            report = None

        # Finding out the individual dates

        if report:
            
            queryset = Product.objects.all().order_by('id')
            
            product_serializers = ProductPdfSerializer(queryset , many = True)
            product_data = product_serializers.data

    

            report =  product_data
            company = company_data
            #print("here is the report", report[0])
            #return JsonResponse({"success":True,"message":"The products dont exist" ,'data':  company})

         
            template_path = 'index.html'
            html = render_to_string(template_path, {'report': report , 'company':company})
            pdf = render_to_pdf('index.html', report , company)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Product_Report_%s.pdf" % ("12341231")
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")

        else:

            return HttpResponse({"success": False, "message": "The products dont exist"})








class GenerateProductReportPdf(View):

    def get(self, request, *args, **kwargs):


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

        try:

            report = inventory_report.objects.all()

        except:

            report = None

        # Finding out the individual dates

        if report:

            main_data = []

      

            specification_ids = list(report.values_list(
                'specification_id', flat=True).distinct())

            for i in range(len(specification_ids)):

                try:
                    # Finding out the entries for that specification_id

                    reports = inventory_report.objects.filter(
                        specification_id=specification_ids[i])

                except:

                    reports = None

                if reports:

                    # Finding out different purchase prices for that specification

                    different_prices = []

                    different_purchase_prices = list(reports.values_list(
                        'purchase_price', flat=True).distinct())

                    for j in range(len(different_purchase_prices)):

                        try:

                            specific_rows = inventory_report.objects.filter(
                                purchase_price=different_purchase_prices[j], specification_id=specification_ids[i])

                        except:

                            specific_rows = None

                        if specific_rows:

                            debit_sum_list = list(
                                specific_rows.values_list('debit', flat=True))
                            credit_sum_list = list(
                                specific_rows.values_list('credit', flat=True))
                            selling_prices = list(
                                specific_rows.values_list('selling_price', flat=True))

                            inventory_ids = list(
                                specific_rows.values_list('id', flat=True))
                            debit_sum = int(sum(debit_sum_list))
                            credit_sum = int(sum(credit_sum_list))
                            if selling_prices[0] == None:
                                selling_prices[0] = 0
                            selling_price = float(selling_prices[0])
                            purchase_price = different_purchase_prices[j]

                            try:

                                specific_inventory = inventory_report.objects.get(
                                    id=inventory_ids[0])

                            except:

                                specific_inventory = None

                            if specific_inventory:

                                inventory_serializer = InventoryReportSerializer(
                                    specific_inventory, many=False)
                                inventory_data = inventory_serializer.data

                                product_name = inventory_data["product_name"]
                                product_brand = inventory_data["product_brand"]
                                product_sku = inventory_data["product_sku"]
                                product_barcode = inventory_data["product_barcode"]
                                product_id = inventory_data["product_id"]
                                specification_id = inventory_data["specification_id"]
                                discount=inventory_data["discount"]

                                response_data = {"product_id": product_id, "specification_id": specification_id, "product_name": product_name, "product_sku": product_sku, "product_barcode": product_barcode,
                                    "product_brand": product_brand, "purchase_price": purchase_price, "selling_price": selling_price, "debit_sum": debit_sum, "credit_sum": credit_sum ,"discount":discount}
                                different_prices.append(response_data)

                            else:

                                pass

                        else:
                            pass

                else:

                    pass
                main_data.append(different_prices)

            report =  main_data
            company = company_data
            #print("here is the report", report[0])
            #return JsonResponse({"success":True,"message":"The products dont exist" ,'data':  report})

         
            template_path = 'ProductReport.html'
            html = render_to_string(template_path, {'report': report , 'company':company})
            pdf = render_to_pdf('ProductReport.html', report , company)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Product_Report_%s.pdf" % ("12341231")
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")

            
            # template_path = 'indexdemo.html'
            # html = render_to_string(template_path, {'report': report , 'company':company})
            # pdf = render_to_pdf('indexdemo.html', report , company)
            # if pdf:
            #     response = HttpResponse(pdf, content_type='application/pdf')
            #     filename = "Product_Report_%s.pdf" % ("12341231")
            #     content = "inline; filename='%s'" % (filename)
            #     download = request.GET.get("download")
            #     if download:
            #         content = "attachment; filename='%s'" % (filename)
            #     response['Content-Disposition'] = content
            #     return response
            # return HttpResponse("Not found")

        else:

            return HttpResponse({"success": False, "message": "The products dont exist"})



class GenerateProductStockReport(View):

    def get(self, request, *args, **kwargs):

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

        try:

            report = inventory_report.objects.all()

        except:

            report = None

        if report:

            main_data = []



            specification_ids = list(report.values_list(
                'specification_id', flat=True).distinct())

            for i in range(len(specification_ids)):

                different_prices = []
                try:

                    reports = inventory_report.objects.filter(
                        specification_id=specification_ids[i])

                except:

                    reports = None

                print("report", report)

                if reports:

                    try:

                        specific_rows = inventory_report.objects.filter(
                            specification_id=specification_ids[i])

                    except:

                        specific_rows = None

                    if specific_rows:

                        debit_sum_list = list(
                            specific_rows.values_list('requested', flat=True))
                        credit_sum_list = list(
                            specific_rows.values_list('credit', flat=True))
                        inventory_ids = list(
                            specific_rows.values_list('id', flat=True))
                        debit_sum = int(sum(debit_sum_list))
                        credit_sum = int(sum(credit_sum_list))
                        available_quantity = credit_sum - debit_sum
                        try:

                            specific_inventory = inventory_report.objects.get(
                                id=inventory_ids[0])

                        except:

                            specific_inventory = None

                        if specific_inventory:

                            inventory_serializer = InventoryReportSerializer(
                                specific_inventory, many=False)
                            inventory_data = inventory_serializer.data

                            product_name = inventory_data["product_name"]
                            product_brand = inventory_data["product_brand"]
                            product_sku = inventory_data["product_sku"]
                            product_barcode = inventory_data["product_barcode"]
                            product_id = inventory_data["product_id"]
                            specification_id = inventory_data["specification_id"]

                            response_data = {"product_id": product_id, "specification_id": specification_id, "product_name": product_name, "product_sku": product_sku, "product_barcode": product_barcode,
                                "product_brand": product_brand, "debit_sum": debit_sum, "credit_sum": credit_sum, "available_quantity": available_quantity,}
                            different_prices.append(response_data)

                        else:

                            pass

                    else:
                        pass

                else:
                  pass
                main_data.append(different_prices)

            report = (company_data , main_data)
            return JsonResponse({"success": True, "message": "The products dont exist", 'data': report})

        else:

            return HttpResponse({"success": False, "message": "The products dont exist"})





class GenerateProductStockReportPDF(View):

    def get(self, request, *args, **kwargs):
   

        try:

            report = inventory_report.objects.all()

        except:

            report = None

        if report:

            main_data = []

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

            specification_ids = list(report.values_list('specification_id',flat=True).distinct())          
        
            for i in range(len(specification_ids)):

                different_prices=[]
                try:

                    reports = inventory_report.objects.filter(specification_id=specification_ids[i])

                except:

                    reports = None 

                print("report" , report)

                if reports:

                    try:

                        specific_rows = inventory_report.objects.filter(specification_id=specification_ids[i])

                    except:

                        specific_rows = None 

                    if specific_rows:

                        debit_sum_list = list(specific_rows.values_list('requested', flat=True))
                        credit_sum_list = list(specific_rows.values_list('credit', flat=True))
                        inventory_ids = list(specific_rows.values_list('id', flat=True))
                        debit_sum = int(sum(debit_sum_list))
                        credit_sum = int(sum(credit_sum_list))
                        available_quantity = credit_sum - debit_sum
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


                            response_data = {"product_id":product_id,"specification_id":specification_id,"product_name":product_name,"product_sku":product_sku,"product_barcode":product_barcode,"product_brand":product_brand,"debit_sum":debit_sum,"credit_sum":credit_sum  , "available_quantity":available_quantity , "company_data":company_data} 
                            different_prices.append(response_data)


                                

                        else:

                            pass


                    else:
                        pass
                       

                else:
                  pass
                main_data.append( different_prices)   

                
            report = report
            company = company_data
            #return JsonResponse({"success":True,"message":"The products dont exist" ,'data': company})

            report = main_data
            template_path = 'ProductStock.html'
            html = render_to_string(template_path, {'report': report , 'company':company})
            pdf = render_to_pdf('ProductStock.html', report , company)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Product_Stock_Report_%s.pdf" %("12341231")
                content = "inline; filename='%s'" %(filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" %(filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")




        else:

            return HttpResponse({"success":False,"message":"The products dont exist"})



class GenerateNoSpecificationPdf(View):

    def get(self, request, *args, **kwargs):


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

        try:

            report = Product.objects.all()

        except:

            report = None

        # Finding out the individual dates

        if report:
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
            else:
                return HttpResponse({"success": False, "message": "SomeThing Went Wrong"})
            report = product_serializer.data
            company = company_data
            #print("here is the report", report[0])
           # return JsonResponse({"success":True,"message":"The products dont exist" ,'data':  report.data})

         
            template_path = 'noSpec.html'
            html = render_to_string(template_path, {'report': report , 'company':company})
            pdf = render_to_pdf('noSpec.html', report , company)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Product_Report_%s.pdf" % ("12341231")
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")

        else:

            return HttpResponse({"success": False, "message": "The products dont exist"})








class GenerateNoSpecificationPricePdf(View):

    def get(self, request, *args, **kwargs):


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

        try:

            report = Product.objects.all()

        except:

            report = None

        # Finding out the individual dates

        if report:
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
                
            else:
                return JsonResponse({"success":False,"message":"No data could be shown"})
                


            report = product_serializer.data
            company = company_data
            #print("here is the report", report[0])
           # return JsonResponse({"success":True,"message":"The products dont exist" ,'data':  report.data})

         
            template_path = 'no_Price.html'
            html = render_to_string(template_path, {'report': report , 'company':company})
            pdf = render_to_pdf('no_Price.html', report , company)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Product_Report_%s.pdf" % ("12341231")
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")

        else:

            return HttpResponse({"success": False, "message": "The products dont exist"})



