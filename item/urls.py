from django.urls import path
from .views import ItemListView, DetailView, ReviewView, ItemPostView, ItemUpdateView


urlpatterns = [
    path('', ItemListView.as_view(),),
    path('details/<int:item_id>', DetailView.as_view()),
    path('upload', ItemPostView.as_view()),
    path('update/<int:item_id>', ItemUpdateView.as_view()),
    path('reupload/<int:item_id>', ItemPostView.as_view()),
    path('reviews/<int:item_id>', ReviewView.as_view()),
]