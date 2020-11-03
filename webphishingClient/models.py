from django.db import models
from django_celery_results.models import TaskResult

import uuid, random

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

    @staticmethod
    def Exists(email, client):
        return Colaborator.objects.filter(email = email, client = client).exists()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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