from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Favourite)
admin.site.register(Category)