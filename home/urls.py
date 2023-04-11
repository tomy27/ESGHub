from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query', views.query, name='query'),
    path('search', views.search, name='search'),
    path('chartdata/<int:id>', views.chartdata, name='chartdata'),
    path('what_is_esg', views.what, name='what'),
]