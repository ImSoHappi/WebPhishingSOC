from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class clientModel(models.Model):

    name = models.CharField(max_length = 100)
    description = models.TextField()
    email = models.EmailField()
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

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