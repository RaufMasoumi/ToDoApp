from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    old_fieldsets = UserAdmin.fieldsets
    old_fieldsets[1][1]['fields'] += ('slug', )
    fieldsets = old_fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('slug', )}), )
    prepopulated_fields = {'slug': ['username']}


admin.site.register(CustomUser, CustomUserAdmin)
