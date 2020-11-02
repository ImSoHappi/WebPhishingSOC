from django.db import models
import uuid

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
    empresa = models.CharField(max_length=120, blank=True)
    rut = models.CharField(max_length=10, blank=True)
    cargo = models.CharField(max_length=100, blank=True)
    org1 = models.CharField(max_length=100, blank=True)
    org2 = models.CharField(max_length=100, blank=True)
    org3 = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    ubicacion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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