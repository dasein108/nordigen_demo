from django.contrib import admin

from .models import UserAccount, UserRequisition

admin.site.register(UserAccount)
admin.site.register(UserRequisition)
# Register your models here.
