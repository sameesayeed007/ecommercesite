from django.contrib import admin

from Intense.models import (User,Profile,user_balance,user_relation,FAQ,Guest_user,Advertisement,PaymentInfo,Subscribers,ProductImpression,ProductImage,
discount_product,Comment,CommentReply,Reviews,Category,Sub_Category,Sub_Sub_Category,ProductCode,Cupons,
GroupProduct,Guest_user,Warehouse,Shop,WarehouseInfo,ShopInfo,OrderInfo,ProductBrand,DeliveryInfo,Terminal,BkashPaymentInfo,TerminalUsers,Invoice,
SpecificationImage,OTP_track,inventory_report,DeliveryArea,DeliveryLocation,product_delivery_area,SpecificationPrice)


from Intense.models import User,subtraction_track,Profile,user_balance,user_relation,FAQ,Guest_user,Advertisement,ProductImpression,TerminalUsers,ProductImage,discount_product,Comment,CommentReply,Reviews,Category,Sub_Category,Sub_Sub_Category,ProductCode,Cupons,GroupProduct,Guest_user,Warehouse,Shop,WarehouseInfo,ShopInfo


# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(user_balance)
admin.site.register(user_relation)
admin.site.register(FAQ)
admin.site.register(Guest_user)
admin.site.register(ProductImage)
admin.site.register(discount_product)
admin.site.register(ProductImpression)
admin.site.register(Comment)
admin.site.register(CommentReply)
admin.site.register(Reviews)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Sub_Sub_Category)
admin.site.register(ProductCode)
admin.site.register(Cupons)
admin.site.register(GroupProduct)
admin.site.register(Warehouse)
admin.site.register(Shop)
admin.site.register(WarehouseInfo)
admin.site.register(ShopInfo)

admin.site.register(OrderInfo)
admin.site.register(ProductBrand)
admin.site.register(DeliveryInfo)
admin.site.register(SpecificationImage)
admin.site.register(inventory_report)
admin.site.register(Invoice)
admin.site.register(DeliveryArea)
admin.site.register(DeliveryLocation)
admin.site.register(OTP_track)
admin.site.register(subtraction_track)
admin.site.register(product_delivery_area)
admin.site.register(Terminal)
admin.site.register(TerminalUsers)
admin.site.register(SpecificationPrice)
admin.site.register(PaymentInfo)
admin.site.register(Subscribers)
admin.site.register(BkashPaymentInfo)





