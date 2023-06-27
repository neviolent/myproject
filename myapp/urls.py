from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('login_process/', views.login_process, name='login_process'),
    path('registration/', views.registration, name='registration'),
    path('reviews/', views.reviews, name='reviews'),
    path('review_add/', views.review_add, name='review_add'),
    path('review_search', views.review_search, name='review_search'),
    path('logout/', views.logout, name='logout'),
    path('authorized/', views.authorized, name='authorized'),
]