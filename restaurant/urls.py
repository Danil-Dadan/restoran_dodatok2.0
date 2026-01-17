from django.urls import path
from . import views
from .views import register, home
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('order/checkout/', views.checkout, name='checkout'),
    path('order/success/', views.order_success, name='reservation_success'),
    path('reservation/', views.make_reservation, name='reservation'),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='main/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

