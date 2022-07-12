from django.contrib import admin
from .models import (
    Contract as ContractModel,
    ContractHistory as ContractHistoryModel,
)


admin.site.register(ContractModel)
admin.site.register(ContractHistoryModel)