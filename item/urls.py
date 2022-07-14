from django.urls import path
from .views import ItemListView, DetailView


urlpatterns = [
    path('', ItemListView.as_view(),),
    path('details/<int:item_id>', DetailView.as_view()),
]