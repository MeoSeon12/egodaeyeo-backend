from django.contrib import admin
from .models import (
    Feedback as FeedbackModel,
    Report as ReportModel
)

admin.site.register(FeedbackModel)
admin.site.register(ReportModel)