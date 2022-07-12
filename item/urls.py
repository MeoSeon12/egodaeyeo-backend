from django.urls import path
from . import views

urlpatterns = [
    path('detail/', views.DetailView.as_view())
]