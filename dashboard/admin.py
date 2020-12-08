from django.contrib import admin

# Register your models here.
from dashboard.models import *
# Modelo DigComp
admin.site.register(Areas)
admin.site.register(Competences)
admin.site.register(Linecompetences)
admin.site.register(Examples)
admin.site.register(Groups)
admin.site.register(Proficiencylevels)
admin.site.register(Competenciasusuario)

"""
  Migrations for 'dashboard':
  dashboard/migrations/0001_initial.py
    - Create model Areas
    - Create model Competences
    - Create model Competenciasusuario
    - Create model Examples
    - Create model Groups
    - Create model Linecompetences
    - Create model Proficiencylevels
    
"""