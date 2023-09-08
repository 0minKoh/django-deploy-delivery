from django.contrib import admin

# Register your models here.
from main.models import Main

@admin.register(Main)
class MainModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'ip', 'url')