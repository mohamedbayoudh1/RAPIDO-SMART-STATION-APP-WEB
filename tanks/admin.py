from django.contrib import admin
from .models import Tank, Category
# Register your models here.


class TankAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'category', 'date',)
    search_fields = ('description', 'category', 'date',)

    list_per_page = 5


admin.site.register(Tank, TankAdmin)
admin.site.register(Category)