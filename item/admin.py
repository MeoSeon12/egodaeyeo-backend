from django.contrib import admin
from .models import (
    Category as CategoryModel,
    Item as ItemModel,
    Bookmark as BookmarkModel,
    Inquiry as InquiryModel,
    Review as ReviewModel,
    ItemImage as ItemImageModel,
)


admin.site.register(CategoryModel)
admin.site.register(ItemModel)
admin.site.register(BookmarkModel)
admin.site.register(InquiryModel)
admin.site.register(ReviewModel)
admin.site.register(ItemImageModel)
