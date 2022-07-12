from django.urls import path
from .views import ItemView, DetailView


urlpatterns = [
    path('', ItemView.as_view(),),
    path('details/<int:item_id>', DetailView.as_view()),
]


