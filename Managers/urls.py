from django.conf import settings
from django.urls import path, include
from . import views

#from .views import ProductDetailView,CreateProductAPIView,DestroyProductAPIView, ProductListAPIView,VariationListView ,GroupProductDetailView ,CategoryListAPIView ,CategoryAPIView , CreateCategoryAPIView , DestroyCategoryAPIView
#from .views import CategoryListAPIView , CategoryRetrieveAPIView

app_name = 'Product'

urlpatterns = [

    path("assign_manager/", views.manager_create),
    path("active_manager/<int:number>/<int:mang_id>/", views.active_deactive_manager),
    path("get_manager/<int:number>/<int:house_id>/", views.get_particular_manager),
    path("product_insert/", views.manager_product_insertion),
    path("unattend_products/<int:user_id>", views.manager_unattendee_product),
    path("house_lists/", views.get_combine_houses),
    path("manager_assign/", views.assign_manager),
    path("all_managers/", views.get_all_users),
    path("manager_info/<int:user_id>", views.particular_manager_shop),
    path("manager_delete/", views.del_managers),
    path("transfer_request/", views.transfer_product_request),
    path("get_house_product/<int:number>/<int:house_id>", views.get_particular_user_all_products),
    path("get_pending_transfer_product/<str:request_getter>", views.get_transfer_request_products),
    path("transferable_list/", views.all_shops_warehouse_lists),
    path("transfer_product_attend/", views.attend_transfer_product),
    path("user_information/<int:user_id>", views.get_user_info),
    path("all_setter_transfer/<int:number>/<int:house_id>", views.all_transfer_data_setter),
    path("pending_trans_req/<int:number>/<int:house_id>", views.get_pending_transfer_data),
    path("specific_transfer/<int:trans_id>", views.get_particular_transfer_products),
    path("all_getter_transfer/<int:number>/<int:house_id>", views.all_transfer_data_getter),

    
 
]
