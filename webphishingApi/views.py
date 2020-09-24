from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from webphishingApi.models import fishinghookModel
from webphishingApi.serializers import phishinghookSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required


@api_view(['GET'])
def api_gethooks(request):
    if request.method == 'GET':

        fishinghooks = fishinghookModel.objects.all()
        fishinghooks_serializer = phishinghookSerializer(fishinghooks, many=True)

        return JsonResponse(fishinghooks_serializer.data, safe=False)
     

@api_view(['POST'])
def api_posthooks(request):
    if request.method == 'POST':

        fishinghooks = JSONParser().parse(request)
        fishinghooks_serializer = phishinghookSerializer(data=fishinghooks)

        if fishinghooks_serializer.is_valid():
            
            fishinghooks_serializer.save()

            return JsonResponse(fishinghooks_serializer.data, status=status.HTTP_201_CREATED) 

        return JsonResponse(fishinghooks_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def fishinghook_list(request):
    
    context = {}
    context['fishinghook_list'] =  fishinghookModel.objects.all()

    return render(request, 'api/fishing_hook.html', context=context)
    


