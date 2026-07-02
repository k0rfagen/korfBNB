from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Role)
admin.site.register(Listing)
admin.site.register(Booking)

@admin.register(BNBUser)
class BNBUserAdmin(UserAdmin):
    pass