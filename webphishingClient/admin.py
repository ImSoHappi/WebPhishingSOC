from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Colaborator)
admin.site.register(ClientFiles)

admin.site.register(Exercise)
admin.site.register(Campaign)
admin.site.register(ColaboratorCampaign)