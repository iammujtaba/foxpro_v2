from django.urls import path
from . import views

urlpatterns = [
    path('add-hsn/', views.add_hsn, name='add_hsn'),
    path('add-item/', views.add_item, name='add_item'),
    path('current-stock/', views.current_stock, name='current_stock'),
]
