from django.urls import path

from product import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product_list/', views.ProductList.as_view(), name='product_list'),
    path('export/xls/', views.export_data_xls, name='export_data_xls'),
    path('export/csv/', views.export_data_csv, name='export_data_csv'),

]
