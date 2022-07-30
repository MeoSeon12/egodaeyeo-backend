from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatView.as_view(),),
    path('<int:room_id>', views.ChatRoomView.as_view(),),
    path('rooms/<int:item_id>', views.ChatView.as_view(),),
    path('alerts/<int:user_id>', views.ChatAlertView.as_view(),),
]