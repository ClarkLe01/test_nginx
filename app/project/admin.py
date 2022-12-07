from django.contrib import admin
from .models import *
from .forms import ProjectForm

class CollaboratorInline(admin.TabularInline):
    model = Project.collaborators.through


class LangCodeInline(admin.TabularInline):
    model = Project.langcode_tags.through


class ProjectsAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ['name', 'description', 'start_date', 'end_date', 'status', 'cost', 'base',
                    'created_by']
    list_filter = ['created_by__email', 'status', 'base']
    search_fields = ['name', 'created_by__email', ]
    inlines = [
        CollaboratorInline,
        LangCodeInline
    ]
    exclude = ('members', 'langcode_tags')


# class ProjectsWithCostAdmin(admin.ModelAdmin):
#     list_display = ['project__name', 'project__description', 'project__start_date',
#                     'project__end_date', 'project__status', 'value', 'base',
#                     'project__created_by']


# Register your models here.
admin.site.register(Project, ProjectsAdmin)
admin.site.register(File)
