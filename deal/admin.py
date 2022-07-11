from django.contrib import admin
from .models import (
    Deal as DealModel,
    DealHistory as DealHistoryModel,
)


admin.site.register(DealModel)
admin.site.register(DealHistoryModel)