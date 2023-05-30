from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_reviewer', 'is_reader']
    exclude = [
        'password',
		'first_name',
		'last_name',
		'is_staff',
        'user_permissions',
        'is_superuser',
        'groups'
	]
    readonly_fields = [
		'email',
		'username',
		# 'is_active',
        'date_joined',
        'last_login',
        'is_reader'
	]

