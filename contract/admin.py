from django.contrib import admin
from .models import (
    Contract as ContractModel,
    Review as ReviewModel,
)


admin.site.register(ContractModel)
admin.site.register(ReviewModel)