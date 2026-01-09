from django.contrib import admin
from .models import FormTemplate, FormField, Employee, UserProfile


class FormFieldInline(admin.TabularInline):
    model = FormField
    extra = 1
    ordering = ['order']

@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'field_count']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name', 'description']
    inlines = [FormFieldInline]

    def field_count(self, obj):
        return obj.fields.count()

    field_count.short_description = 'Number of Fields'

@admin.register(FormField)
class FormFieldAdmin(admin.ModelAdmin):
    list_display = ['label', 'field_type', 'form_template', 'required', 'order']
    list_filter = ['field_type', 'required', 'form_template']
    search_fields = ['label', 'form_template__name']
    ordering = ['form_template', 'order']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'form_template', 'created_by', 'created_at']
    list_filter = ['form_template', 'created_at', 'created_by']
    search_fields = ['form_template__name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at']
