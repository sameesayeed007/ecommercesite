from django.conf import settings
from django.urls import path, include
from . import views

#from .views import ProductDetailView,CreateProductAPIView,DestroyProductAPIView, ProductListAPIView,VariationListView ,GroupProductDetailView ,CategoryListAPIView ,CategoryAPIView , CreateCategoryAPIView , DestroyCategoryAPIView
#from .views import CategoryListAPIView , CategoryRetrieveAPIView

app_name = 'Product'

urlpatterns = [

    path("create/", views.insert_specific_product_value),
    path('delete/<int:product_id>/', views.delete_product_value),
    path('edit/<int:product_id>/', views.get_update_product_value),
    path('get_product_using_barcode`tail/', views.get_all_product),
    path('category_detail/', views.get_all_product_category),
    path('category/create/', views.insert_specific_category_value),
    path('category/edit/<int:category_id>', views.get_update_category_value),
    path('category/delete/<int:category_id>', views.get_update_category_value),
    path('group/detail/', views.get_all_group_product),
    path('group/create/', views.insert_specific_group_product_value),
    path('group/edit/<int:gp_id>/', views.get_update_group_product_value),
    path('group/delete/<int:gp_id>', views.delete_group_product_value),
    path('list/' , views.ListProductView.as_view()),
    path('edit_group_product/<int:product_id>/' , views.get_update_group_product_value),

    
    #Product comments and reviews
    path('comments_product/<int:product_id>/', views.comments_product),
    #path('comments/<int:product_ids>/', views.comm),
    path('create_comment/', views.create_comment),
    path('create_reply/', views.create_reply),
    path('edit_comment/<int:comment_id>/', views.edit_comment),
    path('edit_reply/<int:reply_id>/', views.edit_reply),
    path('delete_comment/<int:comment_id>/', views.delete_comment),
    path('delete_reply/<int:reply_id>/', views.delete_reply),
    path('reviews_product/<int:product_id>/', views.reviews_product),
    path('create_review/', views.create_review),
    path('edit_review/<int:review_id>/', views.edit_review),
    path('delete_review/<int:review_id>/', views.delete_review),
    path('ratings/<int:product_id>/',views.product_ratings,name='ratings'),
    path('upload/',views.upload_product),
    path('edit/<int:product_id>/',views.edit_product),#*******
    path('update_product/<int:product_id>/',views.specific_product_update),
    
    path('display/<int:number>/',views.display_products),
    path('showmore/',views.show_more),
    path('reviews_list' , views.ListReviewView.as_view()),

    path('insert_product_image/',views.product_image_up),
    path('get_product_images/',views.get_all_product_image),
    path('get_specific_images/<int:image_id>/',views.get_specific_product_image),
    path('update_specific_images/<int:image_id>/',views.update_product_image_value),
    path('delete_specific_images/<int:image_id>/',views.delete_specific_product_image),
    path('add_product/',views.product_insertion_admin1),

    path('value/<int:product_id>/<int:height>/<int:width>/', views.get_specific_code_values), 
    path('delete_value/', views.specific_code_delete), 
    path('insert_value/', views.insert_specific_code_values),
    path('scanned_value/<str:scanned_code>/', views.get_product_using_barcode),

    path('delete_product/<int:product_id>/', views.specific_product_delete_admin),
    path('all_value/', views.all_product_detail),
    path('hide_delete/<int:product_id>/', views.specific_product_hidden_delete),
    path('modify_product/<int:product_id>/', views.modify_specific_product),
    
    path('group_product_insert/', views.group_product_insertion_admin),
    path('modify_group_product/<int:product_id>/', views.modify_specific_group_product),
    path('all_group_product/<int:number>/', views.get_all_detailed_group_product),
    path('search/<str:name>/', views.get_searched_product),
    path('approved/<int:user_id>/', views.approved_products),
    path('pending/<int:user_id>/', views.pending_products),
    path('cancelled/<int:user_id>/', views.cancelled_products),
    path('all/<int:user_id>/', views.all_products),
    path('product_details/', views.get_all_product),
    path('seller_products/', views.get_all_products),
    path('get_product_info/<int:product_id>/', views.get_product_info),
    path('inventory_price/<int:order_id>/', views.insert_inventory),
    path('merchent_approval/<int:product_id>/', views.merchant_approval),
    path('merchant_calcceled/<int:product_id>/', views.merchant_calcceled),
    path('shared_products/', views.shared_products),
    path('unshared_products/', views.unshared_products),
    path('unpublished_products/', views.unpublished_products),
    path('seller_list/', views.seller_list),
    path('seller_approved_products/<int:user_id>/', views.seller_approved_products),
    path('seller_cancelled_products/<int:user_id>/', views.seller_cancelled_products),
    path('seller_pending_products/<int:user_id>/', views.seller_pending_products),
    path('share_product/<int:product_id>/', views.share_product),
    path('publish_product/<int:product_id>/', views.publish_product),
    path('cancel_publish_product/<int:product_id>/', views.seller_pending_products),
    path('all_seller_approved_products/', views.all_seller_approved_products),
    path('all_seller_cancelled_products/', views.all_seller_cancelled_products),
    path('all_seller_pending_products/', views.all_seller_pending_products),
    path('barcode_value/<int:specification_id>/', views.get_specific_barcodecode_values), 
    path('generate_sku/<int:specification_id>/', views.get_specific_sku_values),    
    path('delete_value/<int:specification_id>/', views.specific_code_delete), 
    path('insert_value/', views.insert_specific_code_values),
    path('allproducts/', views.pos_products),
    path('edit_images/<int:product_id>/', views.edit_images),
    path('nospecification_products/', views.nospecification_products),
    path('noprice_products/', views.noprice_products),
    path('publish_unpublish_specification/<int:specification_id>/', views.publish_unpublish_specification),
    path('publish_unpublish_product/<int:product_id>/', views.publish_unpublish_product),


]
