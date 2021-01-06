from rest_framework import serializers
from Intense.models import Ticket,TicketReplies,User,Profile,DeliveryArea,DeliveryLocation,DeliveryInfo,APIs
# from .serializers import TicketSerializer ,TicketRepliesSerializer


# Serializers define the API representation.
class TicketSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(method_name='all_replies')
    sender_name = serializers.SerializerMethodField(method_name='ticket_sender')
    attender_name= serializers.SerializerMethodField(method_name='ticket_attender')
    sender_picture = serializers.SerializerMethodField(method_name='get_sender_picture')
    class Meta:
        model = Ticket
        fields = ('id','title','sender_id','sender_name','sender_picture','receiver_id','attender_name','department', 'status','complain','created', 'modified','is_active','is_attended','replies')

    def all_replies(self, obj):
        all_replies=[]
        replies = TicketReplies.objects.filter(ticket_id=obj.id).values()
        for rep in replies:
            try:
                senders = User.objects.filter(id= rep['user_id']).values('email')
                rep.update({'sender':senders[0]['email']})
            except:
                pass
            all_replies.append(rep)
        return all_replies

    def ticket_sender (self,obj):
        sender_email = ""
        try:
            sender = User.objects.get(id= obj.sender_id)
            
        except:
            sender = None 

        if sender:
            if sender.email:
                sender_email = sender.email
            else:
                sender_email = ""

        else:
            sender_email = ""

        return sender_email
            

    def ticket_attender (self, obj):

        sender_email = ""
        try:
            sender = User.objects.get(id= obj.receiver_id)
            
        except:
            sender = None 

        if sender:
            if sender.email:
                sender_email = sender.email
            else:
                sender_email = ""

        else:
            sender_email = ""

        return sender_email
 


    def get_sender_picture (self, obj):

        picture= ""
        try:
            sender = User.objects.get(id= obj.sender_id)
        except:
            sender = None

        if sender:
            print("email_id ase")
            email_id = sender.email

            print(email_id)

            try:

                profile_pic = Profile.objects.get(email=email_id)
            except:
                profile_pic = None

            print(profile_pic)

            if profile_pic:

                print("profile picture ase")

                picture = profile_pic.profile_picture_url

            else:

                print("profile picture nai")

                picture = ""

            print(picture)

        else:

            picture = ""


        return picture

         


class TicketRepliesSerializer(serializers.ModelSerializer):
    attender_name = serializers.SerializerMethodField(method_name='attender_reply')
    class Meta:
        model = TicketReplies
        fields = ('id','ticket_id','reply','created','user_id','attender_name','name','is_staff')

    def attender_reply (self, obj):
        try:
            receiver = User.objects.get(id= obj.user_id)
            return receiver.email
        except:
            return {"message": "Problem while retrieving attender name"}



class AreaSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = DeliveryArea

        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = DeliveryLocation

        fields = "__all__"

class DeliverySerializer(serializers.ModelSerializer):
    thana_name = serializers.SerializerMethodField(method_name='thanas')
    class Meta:
        model = DeliveryInfo

        fields = ('id','thana_name','unit_price','delivery_day','minimum_amount','location_id','height','width','length','weight', 'measument_unit')
    def thanas (self, obj):
        try:
            thana_info = DeliveryLocation.objects.get(id= obj.location_id)
            return thana_info.location_name
        except:
            return ""



class ApienabledisableSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIs
        fields = "__all__"