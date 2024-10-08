from django.contrib import admin
from .models import VisaBanner, Country, VisaType, VisaPackage, RequiredDocuments

class RequiredDocumentsInline(admin.TabularInline):
    model = RequiredDocuments

@admin.register(VisaPackage)
class VisaPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'visa_type', 'is_featured', 'is_active', 'created_at', 'updated_at')
    list_filter = ('country', 'visa_type', 'is_featured', 'is_active')
    search_fields = ('title', 'overview')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('total_fee',)
    inlines = [RequiredDocumentsInline]  # Add inline for RequiredDocuments
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'country', 'visa_type')
        }),
        ('Content', {
            'fields': ('overview',)
        }),
        ('Fees & Processing Time', {
            'fields': ('visa_fee', 'processing_fee', 'total_fee', 'our_processing_time', 'visa_processing_time','valid_for','number_of_entries','max_stay')
        }),
        ('Image & Status', {
            'fields': ('image', 'is_featured', 'is_active')
        })
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('total_fee',)  # Total fee should be read-only when editing
        return self.readonly_fields

@admin.register(VisaBanner)
class VisaBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image','title','is_active')

admin.site.register(VisaType)
