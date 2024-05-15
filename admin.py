from django.contrib import admin

from .models import teachers

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    fields = ('name', 'image')

admin.site.register(teachers, TeacherAdmin)

# Register your models here.
