from django.urls import path
from . import views

urlpatterns = [
    # Аутентификация
    path('login/', views.login_view, name='login'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Пользователи
    path('users/', views.users_list, name='users_list'),
    
    # VIP-клиенты
    path('clients/', views.vip_clients_list, name='vip_clients_list'),
    path('clients/add/', views.vip_client_add, name='vip_client_add'),
    path('clients/<int:pk>/', views.vip_client_detail, name='vip_client_detail'),
    path('clients/<int:pk>/edit/', views.vip_client_edit, name='vip_client_edit'),
    path('clients/<int:pk>/delete/', views.vip_client_delete, name='vip_client_delete'),
    
    # Взаимодействия
    path('clients/<int:client_pk>/interaction/add/', views.interaction_add, name='interaction_add'),
    
    # Организации
    path('organizations/', views.organizations_list, name='organizations_list'),
]


