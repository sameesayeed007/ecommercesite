import json
import serpy
from rest_framework import serializers
#from user_profile.models import User
from Intense.models import (
    Managers_list
)
from drf_extra_fields.fields import Base64ImageField
from django.db.models import Avg



from rest_framework import serializers
from rest_framework import fields
from django.utils import timezone
from django.conf import settings
from django.forms.models import model_to_dict
import requests


class ManagerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Managers_list
        fields = "__all__"
