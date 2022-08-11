from django.urls import path
from .views import FeedbackView, ReportView

urlpatterns = [
     path('', FeedbackView.as_view()),
     path('report/<int:item_id>/', ReportView.as_view()),
]