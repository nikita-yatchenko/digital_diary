from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualization, name='visualization'),
    path('notes/', views.notes, name='notes'),
    path('positives/', views.positives, name='positives'),
    path('negatives/', views.negatives, name='negatives'),
    path('neutrals/', views.neutrals, name='neutrals'),
]
