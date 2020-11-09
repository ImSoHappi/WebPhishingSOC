from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from webphishingClient.models import Colaborator, Campaign, ColaboratorCampaign
from .models import ApiKeys
from .decorators import required_fields

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

@api_view(['POST'])
@csrf_exempt
@required_fields((
    ("privateKey", "webphishingApi.models.ApiKeys"),
    ("colaboratorId", "webphishingClient.models.Colaborator"),
    ("campaignId", "webphishingClient.models.Campaign"),
    ("stage", ["sent", "open", "clicked", "compromised"]),
))
def api_ex_reportSent(request):
    # Check needed fields

    # Process
    context = {}
    context['errors'] = []
    context['result'] = ""
    context['messages'] = []

    # ###########
    # Load obj
    colaborator = Colaborator.Get(request.colaboratorId)
    campaign = Campaign.Get(request.campaignId)

    # Check if camp exists
    if not ColaboratorCampaign.Exists(colaborator, campaign):
        context['errors'].append("Colaborator does not exists or its not related to that campaign")

    if len(context['errors']) > 0:
        context['result'] = "FAILED"
    else:
        context['result'] = "SUCCESS"

        # Register mailsent
        ccObj = ColaboratorCampaign.Get(colaborator, campaign)
        ccObj.setStatus("sent")

    return JsonResponse(context)

'''
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
'''