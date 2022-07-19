from django.urls import path
from .views import ItemListView, DetailView, ItemPostView


urlpatterns = [
    path('', ItemListView.as_view(),),
    path('details/<int:item_id>', DetailView.as_view()),
    path('upload', ItemPostView.as_view()),
]