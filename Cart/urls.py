from django.urls import include, path
from . import views

urlpatterns = [
  
    #path('add/<int:productid>/<int:userid>/', views.add_to_cart),
    #path('addcart/<int:productid>/', views.add_cart),
    path('addcart/<int:specificationid>/', views.add_cart1),
    #path('increase/<int:productid>/', views.increase_quantity),
    path('increase/<int:specificationid>/', views.increase_quantity1),
    # path('decrease/<int:productid>/', views.decrease_quantity),
    path('decrease/<int:specificationid>/', views.decrease_quantity1),
    #path('delete/<int:productid>/', views.delete_product),
    path('delete/<int:specificationid>/', views.delete_product1),
    path('checkout/<int:order_id>/', views.checkout),
    path('cart_view/', views.cart_view),
    path('cart_details/', views.cart_details),
    path('allorders/', views.all_orders),
    path('orders/', views.orders),
    path('orders_pending/', views.orders_pending),
    path('admin_approval/<int:order_id>', views.admin_approval),
    path('admin_cancellation/<int:order_id>', views.admin_cancellation),
    path('specific_order/<int:order_id>/', views.specific_order),
    path('orders_to_pay/', views.orders_to_pay),
    path('orders_to_ship/', views.orders_to_ship),
    path('orders_received/', views.orders_received),
    path('orders_cancelled/', views.orders_cancelled),
    path('cancel_order/', views.cancel_order),
    path('cancel_specific_order/<int:order_id>/', views.cancel_specific_order),
    path('cancel_cart/', views.cancel_cart),
    path('unpaidorders/', views.orders_not_paid),
    path('notdeliveredorders/', views.orders_not_delivered),
    path('deliveryinfo/', views.order_delivery),
    path('create_address/', views.create_address),
    path('show_address/', views.show_address),
    path('edit_address/', views.edit_address),
    path('check_coupon/', views.check_coupon),
    path('cancelorder/<int:order_id>/', views.cancelorder),
    path('order_info/', views.order_info),
    # path('create_invoice/<int:order_id>/', views.create_invoice),
    path('sales_report/', views.sales_report),
    path('edit_invoice/<int:invoice_id>/', views.edit_invoice),
    path('create_invoice/<int:invoice_id>/', views.create_invoice),
    path('check_location/<int:specification_id>/<int:billing_address_id>/', views.check_location),
    path('check_delivery_location/<int:order_id>/', views.check_delivery_location),


    # path('insert_quantity/', views.insert_product_quantity),

    path('insert_quantity/', views.insert_product_quantity),
    path('create_order/<int:seller_id>/', views.create_order),
    path('seller_invoices/<int:seller_id>/', views.seller_invoices),
    path('seller_individual_invoice/<int:invoice_id>/', views.seller_individual_invoice),
    path('admin_seller_invoices/', views.admin_seller_invoices),
    path('individual_orders/', views.individual_orders),
    path('checkout_data/', views.checkout_data),
    path('create_pos_order/', views.create_pos_order),
    path('check_user/', views.check_user),
    path('verify_payment/', views.verify_payment),
  
    path('change_order_date/<int:order_id>', views.change_order_date),
    path('get_last_order_address/', views.get_last_order_address),
   
    path('get_terminal_users/<int:terminal_id>/', views.get_terminal_users),
    path('pos_report/<int:terminal_id>/<int:user_id>/', views.pos_report),
    path('pos_invoice/<int:order_id>/', views.pos_invoice),
    path('create_mothersite_orders/', views.create_mothersite_orders),
    path('create_mothersite_orders_purchase_invoice/', views.create_mothersite_orders_purchase_invoice),
    
   




    #path('addpoints/', views.add_points),
   

  
  

]