from django.contrib import admin
from .models import *
from django.forms import CheckboxSelectMultiple

# Register your models here.

class ContentStylingAdmin(admin.ModelAdmin):
    model = ContentStyling

    def save_model(self, request, obj, form, change):
        
        if obj.created_by: 
            obj.updated_by_id = request.user.id
        else:
            obj.created_by_id = request.user.id
      
        super().save_model(request, obj, form, change)
    
    list_display = ('font_name','created_By', 'created_at', 'updated_By', 'updated_at')

    def created_By(self,obj):
        if obj.created_by != None:
            return obj.created_by.username

    def updated_By(self,obj):
        if obj.updated_by != None:
            return obj.updated_by.username

admin.site.register(ContentStyling, ContentStylingAdmin)


class ReportTemplateAdmin(admin.ModelAdmin):
    model = ReportTemplate

    def save_model(self, request, obj, form, change):
        
        if obj.created_by: 
            obj.updated_by_id = request.user.id
        else:
            obj.created_by_id = request.user.id
      
        super().save_model(request, obj, form, change)
    
    list_display = ('template_name','created_By', 'created_at', 'updated_By', 'updated_at')

    def created_By(self,obj):
        if obj.created_by != None:
            return obj.created_by.username

    def updated_By(self,obj):
        if obj.updated_by != None:
            return obj.updated_by.username

admin.site.register(ReportTemplate, ReportTemplateAdmin)


class ReportManagementAdmin(admin.ModelAdmin):
    model = ReportManagement

    def save_model(self, request, obj, form, change):
        
        if obj.created_by: 
            obj.updated_by_id = request.user.id
        else:
            obj.created_by_id = request.user.id

        super().save_model(request, obj, form, change)
    
    list_display = ('name','query','created_By', 'created_at', 'updated_By', 'updated_at')

    formfield_overrides = {
            models.ManyToManyField: {'widget': CheckboxSelectMultiple},
        }

    def created_By(self,obj):
        if obj.created_by != None:
            return obj.created_by.username

    def updated_By(self,obj):
        if obj.updated_by != None:
            return obj.updated_by.username
        
admin.site.register(ReportManagement, ReportManagementAdmin)

class ReportFiltersAdmin(admin.ModelAdmin):
    model = ReportFilters

    def save_model(self, request, obj, form, change):
        
        if obj.created_by: 
            obj.updated_by_id = request.user.id
        else:
            obj.created_by_id = request.user.id

        super().save_model(request, obj, form, change)
    

    formfield_overrides = {
            models.ManyToManyField: {'widget': CheckboxSelectMultiple},
        }

    def created_By(self,obj):
        if obj.created_by != None:
            return obj.created_by.username

    def updated_By(self,obj):
        if obj.updated_by != None:
            return obj.updated_by.username


admin.site.register(ReportFilters,ReportFiltersAdmin)
