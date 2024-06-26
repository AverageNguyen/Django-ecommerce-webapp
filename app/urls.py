from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.loginPage, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logoutPage, name = 'logout'),
    path('cart/',views.cart, name = 'cart'),
    path('checkout/',views.checkout, name = 'checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('search/', views.search, name = 'search'),
    path('category/', views.category, name = 'category'),
    path('detail/', views.detail, name = 'detail'),
    path('process_order/', views.processOrder, name = 'process_order'),
    path('shop/', views.shop, name = 'shop'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    
]