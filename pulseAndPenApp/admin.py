from django.contrib import admin
from pulseAndPenApp.models import User, Contact, Blog, Comment, NewsletterSubscription

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'first_name', 'last_name', 'email', 'password' ]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'message']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'content', 'category', 'thumbnail_url', 'created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'blog', 'user', 'text', 'created_at']

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email']
