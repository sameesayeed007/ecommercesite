from django.urls import include, path
from . import views

urlpatterns = [
  
  path('create_ticket/', views.create_ticket),
  path('create_reply/<int:ticket_id>/', views.create_reply),
  path('ticket_list/', views.ticket_list),
  path('unattended_ticket_list/', views.unattended_ticket_list),
  path('edit_ticket/<int:ticket_id>/', views.edit_ticketinfo),
  path('specific_ticket/<int:ticket_id>/', views.specific_ticket),
  path('active_ticket/', views.active_ticket),
  path('sender_ticket/<int:sender_id>/', views.sender_ticket),
  path('receiver_ticket/<int:receiver_id>/', views.receiver_ticket),
  path('edit_reply/<int:reply_id>/', views.edit_ticketreply),
  path('delete_ticket/<int:ticket_id>/', views.delete_ticket),
  path('dashboard/', views.dashboard),
  path('seller_dashboard/<int:user_id>/', views.seller_dashboard),
  path('addarea/', views.insert_area),
  path('addlocation/', views.insert_location),
  path('addcharge/', views.insert_delivery_charge),
  path('allareas/<int:order_id>/', views.get_all_areas),
  path('all_areas/', views.get_all_areaz),
  path('getlocation/<str:area_name>/', views.get_specific_locationz),
  path('getlocation/<str:area_name>/<int:order_id>/', views.get_specific_location),
  path('estimations/<str:area_name>/<str:location_name>', views.get_estimated_value),
  path('delete_estimate/<int:area_id>/', views.delete_estimation),
  path('all_info/', views.getall_info_data),
  path('check_enable/<str:api_name>/', views.enable_checking),
  path('enable_disable/<str:name>/<int:status>', views.make_enable_disable),
  path('apis_base_url', views.get_all_active_delivery_base_url),
  path('delivery_statistics/', views.delivery_statistics),
  path('order_statistics/', views.order_statistics),
  path('district_change_status/<str:name>/<int:status>', views.make_district_active_inactive),
  path('thana_change_status/<str:name>/<int:status>', views.make_thanas_active_inactive),
  path('change/', views.product_change),
  



]