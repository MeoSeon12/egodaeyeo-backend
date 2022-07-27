from django.urls import path
from .views import ContractView

urlpatterns = [
    path('start/<int:item_id>', ContractView.as_view()),
    path('end/<int:item_id>', ContractView.as_view()),
]