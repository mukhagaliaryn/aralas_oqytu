from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django_summernote.admin import SummernoteModelAdmin

from accounts.models import User, Content


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name', )
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('avatar', 'email', 'username', 'first_name', 'last_name', 'user_type', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'first_name', 'password1', 'password2', )}
        ),
    )


class ContentAdmin(SummernoteModelAdmin):
    list_display = ('title', 'order', )


admin.site.register(User, UserAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.unregister(Group)
