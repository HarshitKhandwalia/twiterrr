from django.contrib import admin
from .models import Tweet

class Tweetadmin(admin.ModelAdmin):
    list_display = ('user','text','created_at',)

admin.site.register(Tweet,Tweetadmin)
# Register your models here.
