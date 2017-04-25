from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Messeges)
admin.site.register(Revocation_list)
admin.site.register(revocation_requests)