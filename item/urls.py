from django.urls import path
from .views import ItemListView, DetailView, ReviewView, ContractView


urlpatterns = [
    path('', ItemListView.as_view(),),
    path('details/<int:item_id>', DetailView.as_view()),
    path('reviews/<int:item_id>', ReviewView.as_view()),
    path('contracts/start/<int:item_id>', ContractView.as_view()),
    path('contracts/end/<int:item_id>', ContractView.as_view()),

]