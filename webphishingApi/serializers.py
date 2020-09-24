from rest_framework import serializers 
from webphishingApi.models import *
 
 
class phishinghookSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = fishinghookModel
        fields = ('id',
                'name',
                'hostname',
                'ip')