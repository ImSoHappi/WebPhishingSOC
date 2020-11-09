from django.db import models
from django_celery_results.models import TaskResult

import uuid, random
from datetime import datetime

class Colaborator(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default = False)
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

    # FK
    client = models.ForeignKey('webphishingAuth.ClientModel', on_delete=models.CASCADE)

    # Mandatory
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()

    # Optional
    extra_data = models.TextField(default='', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def Exists(email, client):
        return Colaborator.objects.filter(email = email, client = client).exists()

    @staticmethod
    def Exists(colabId):
        return Colaborator.objects.filter(pk = colabId).exists()

    @staticmethod
    def Get(colabId):
        return Colaborator.objects.get(pk = colabId)

def upload_to_uuid_folder(instance, filename):
    prefix = random.randrange(100000000000,999999999999)
    return "clients/{}/{}_{}".format(instance.client.uuid, prefix, filename)
class ClientFiles(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default = False)

    # FK
    client = models.ForeignKey('webphishingAuth.ClientModel', on_delete=models.CASCADE)

    # Data
    file_data = models.FileField(upload_to=upload_to_uuid_folder)

EXERCISE_STATUS = (
    ('pending','Pendiente'),
    ('preparing','Preparacion'),
    ('inprogress','En proceso'),
    ('finished','Finalizado')
)
class Exercise(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default = False)
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

    # FK
    client = models.ForeignKey('webphishingAuth.ClientModel', on_delete=models.CASCADE)

    # Datos ejercicio
    planification_date = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=10, choices=EXERCISE_STATUS, default="pending")

    def getCampaingById(self, campaignId):
        try:
            return Campaign.objects.get(exercise = self, pk = campaignId)
        except:
            return None

    def getCampanas(self):
        return Campaign.objects.filter(exercise = self)

def upload_to_uuid_campaign_folder(instance, filename):
    prefix = random.randrange(100000000000,999999999999)
    return "exercises/{}/campaign_{}_{}".format(instance.exercise.uuid, prefix, filename)
class Campaign(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default = False)
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    colaborators = models.ManyToManyField(Colaborator, through = 'ColaboratorCampaign')
    name = models.CharField(max_length=100, default='')

    # Data
    image_tracking = models.ImageField(upload_to=upload_to_uuid_campaign_folder, blank=True)
    html_text = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def getSigned(self):
        colaborators = self.colaborators.all()
        return colaborators

    def getSent(self):
        colaborators = self.colaborators.filter(colaboratorcampaign__sent__isnull=False)
        return colaborators

    def getClicked(self):
        colaborators = self.colaborators.filter(colaboratorcampaign__clicked__isnull=False)
        return colaborators
    
    def getOpened(self):
        colaborators = self.colaborators.filter(colaboratorcampaign__opened__isnull=False)
        return colaborators

    def getCompromised(self):
        colaborators = self.colaborators.filter(colaboratorcampaign__compromised__isnull=False)
        return colaborators

    def getColaborators(self):
        return self.colaborators.all()

    def getCampaignResults(self):
        return ColaboratorCampaign.objects.filter(campaign = self)

    def __str__(self):
        return self.name

    @staticmethod
    def Exists(campId):
        return Campaign.objects.filter(pk = campId).exists()

    @staticmethod
    def Get(campId):
        return Campaign.objects.get(pk = campId)

class ColaboratorCampaign(models.Model):
    colaborator = models.ForeignKey(Colaborator, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    
    # User tracking data
    sent = models.DateTimeField(blank=True, null=True)
    clicked = models.DateTimeField(blank=True, null = True)
    opened = models.DateTimeField(blank=True, null = True)
    compromised = models.DateTimeField(blank=True, null = True)

    @staticmethod
    def Get(colabId, campId):
        try:
            return ColaboratorCampaign.objects.get(colaborator = colabId, campaign = campId)
        except:
            return None

    @staticmethod
    def Exists(colabId, campId):
        return ColaboratorCampaign.objects.filter(colaborator = colabId, campaign = campId).exists()


'''
class exerciseModel(models.Model):
    client = models.ForeignKey('clientModel', on_delete = models.CASCADE)
    campaigns = models.ManyToManyField('campaignModel', blank=True)
    name = models.CharField(max_length = 100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class employeesModel(models.Model):

    exercise = models.ForeignKey('exerciseModel', on_delete = models.CASCADE)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    data = models.TextField()
    
    received = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    click = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class campaignModel(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()

    subject = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.name

class csvModel(models.Model):

    csvfile = models.FileField(validators=[FileExtensionValidator(['csv'])])
'''