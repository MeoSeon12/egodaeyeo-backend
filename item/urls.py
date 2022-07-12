from django.urls import path
from .views import ItemView

urlpatterns = [
    path('', ItemView.as_view(),),
    path('detail/', views.DetailView.as_view()),
]