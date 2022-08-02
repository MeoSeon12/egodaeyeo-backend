from django.urls import path
from .views import ContractView

urlpatterns = [
    path('<int:item_id>', ContractView.as_view()),
]