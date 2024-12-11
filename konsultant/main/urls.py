from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registr/', views.registr, name='registr'),

    path('cart/remove/<int:toy_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/<int:toy_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    #   новый
    path('chatbot/', views.chatbot_response, name='chatbot_response'),
    path('checkout/', views.checkout, name='checkout'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
]