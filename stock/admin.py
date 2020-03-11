from django.contrib import admin
from stock.models import *

admin.site.register(StockList)

class ReviewInline(admin.TabularInline):
    model = Review

class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline,
    ]
    list_display = ("title", "author", "price",)



admin.site.register(Book, BookAdmin)

