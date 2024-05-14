from django.contrib import admin
# import your models here
from .models import Project, Link, Language

# Register your models here
admin.site.register(Project)
admin.site.register(Link)
admin.site.register(Language)