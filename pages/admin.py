from django.contrib import admin
from .models import Page, Category

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields= ('created', 'updated')

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    readonly_fields= ('created', 'updated')
    list_display = ('title', 'order', 'post_categories')
    search_fields = ('title', 'categories__name')
    class Media:
        css = {
            'all': ('pages/css/custom_ckeditor.css',)
        }

    def post_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all().order_by("name")])
    post_categories.short_description = "Categorías"

admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
