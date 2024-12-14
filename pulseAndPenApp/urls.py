from django.urls import path
from pulseAndPenApp import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.LoginView.as_view(), name='sign-in'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('join/', views.join, name='join'),
    path('home/', views.home_view, name='home'),
    path('blogs/<str:type>/', views.blogs, name='blogs'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms-and-conditions'),
    path('publish/', views.publish, name='publish'),
    path('publish/blog/', views.BlogCreateView.as_view(), name='publish-blog'),
    path('blog/complete/<str:title>', views.complete_blog, name='complete-blog'),
    path('blog/comment/', views.CommentView.as_view(), name='blog-comment'),
    path('blog/<str:title>/<int:blog_id>/comments/', views.get_blog_comments, name='blog-comment'),
    path('subscribe/newsletter/', views.NewsletterSubscriptionView.as_view(), name='newsletter-subscription'),
]