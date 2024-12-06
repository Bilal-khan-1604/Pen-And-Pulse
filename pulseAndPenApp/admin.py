from django.contrib import admin
from pulseAndPenApp.models import User, Login, Contact

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'first_name', 'last_name', 'email', 'password' ]

@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = [ 'email', 'date_time' ]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'message']
