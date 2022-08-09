from django.contrib import admin

# Register your models here.
from .models import FIRM, Staff

admin.site.register(FIRM)

admin.site.register(Staff)