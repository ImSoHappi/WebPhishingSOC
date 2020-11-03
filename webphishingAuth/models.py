from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from webphishingClient.models import *

import uuid, random

#################
## Uusuario de plataforma
#################
class UserModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    disabled = models.BooleanField(default = True)

    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True, related_name="extend")
    client = models.ForeignKey('ClientModel', on_delete = models.CASCADE)   
    phone = models.CharField(max_length = 12)
    email = models.EmailField()

    def isAdmin(self):
        if self.user.is_staff or self.user.groups.filter(name='admins').exists():
            return True
        else:
            return False
    
    def isClient(self):
        if self.user.groups.filter(name='client').exists():
            return True
        else:
            return False
    
    def isColaborator(self):
        if self.user.groups.filter(name='colaborator').exists():
            return True
        else:
            return False

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=UserModel)
def create_user_extended(sender, instance, created, **kwargs):
    if created:
        if instance.user is None:
            user = User.objects.create_user(instance.email, instance.email, User.objects.make_random_password())
            user.is_active = True
            user.save()
            
            instance.user = user
            instance.save()

#################
## Cliente y archivos cliente
#################
def upload_to_uuid_folder(instance, filename):
    prefix = random.randrange(100000000000,999999999999)
    return "clients/{}/{}_{}".format(instance.uuid, prefix, filename)
class ClientModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    disabled = models.BooleanField(default = False)

    name = models.CharField(max_length = 200)
    code = models.CharField(max_length = 5, default = None)
    main_color = models.CharField(max_length = 7, default = "#43B5E4")

    email = models.EmailField()
    description = models.TextField()
    relevant_fields = models.TextField()
    logo = models.ImageField(upload_to=upload_to_uuid_folder, null = True, blank = True)

    last_task = models.CharField(max_length=255, default='')

    def getLastTask(self):
        results = TaskResult.objects.filter(task_id = self.last_task)
        if len(results) > 0:
            return results[0]
        else:
            return "Sin tareas"

    def getUsers(self):
        return UserModel.objects.filter(client = self)

    def getColaborators(self):
        return Colaborator.objects.filter(client = self)

    def getColaboratorById(self, id):
        try:
            return Colaborator.objects.get(client = self, pk = id)
        except:
            return None

    def getFileById(self, id):
        try:
            return ClientFiles.objects.get(client = self.pk, pk = id)
        except:
            return None

    @staticmethod
    def getClient(pk):
        try:
            return ClientModel.objects.get(uuid = pk)
        except:
            return None

    @staticmethod
    def getClients(disabled = False):
        if disabled:
            return ClientModel.objects.all()
        else:
            return ClientModel.objects.filter(disabled = False)

    def __str__(self):
        return self.name