from django.urls import path
from .views import ItemView

urlpatterns = [
    #/items
    path('', ItemView.as_view(),),
]
