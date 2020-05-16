from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="product"),
    path('customer/', views.customer, name="customer"),
    path('customer/<str:id>', views.customer, name="customer"),
    path('update/<str:id>', views.update, name="update"),
    path('create/', views.create, name="create"),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.register, name='regiter'),
]
