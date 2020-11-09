from django.db import models

import random, uuid, string

def get_random_string():
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(32))
    return result_str
class ApiKeys(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default = False)
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

    publicKey = models.TextField(default=get_random_string)
    privateKey = models.TextField(default=get_random_string)

    last_usage = models.DateTimeField(null = True, blank = True)

    @staticmethod
    def Exists(privateKey):
        return ApiKeys.Validate(privateKey)

    @staticmethod
    def Validate(privateKey):
        check = ApiKeys.objects.filter(privateKey = privateKey).exists()
        return check

#class fishinghookModel(models.Model):
#    name = models.CharField(max_length=50)
#    hostname = models.CharField(max_length=100)
#    ip = models.GenericIPAddressField()#
#
#    def __str__(self):
#        return self.name

