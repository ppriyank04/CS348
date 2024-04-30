from django.urls import path
from . import views

app_name = 'polls'  # Namespace for the app

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('add/', views.add_stock, name='add_stock'),
    path('update/', views.update_stock, name='update_stock'),  # No stock_id in the URL
    path('report/', views.stock_report, name='stock_report'),
    path('sell/', views.sell_stock, name='sell_stock'),
]
