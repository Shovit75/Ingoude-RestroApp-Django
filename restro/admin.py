from django.contrib import admin
from .models import Food, Category, WebUser, Checkout, Chef

# Register your models here.

admin.site.register(Food)
admin.site.register(Category)
admin.site.register(WebUser)
admin.site.register(Checkout)
admin.site.register(Chef)