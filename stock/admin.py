from django.contrib import admin
from stock.models import *

# 테이블 형태로 변경하여 깔끔하게 보이게.
class StockListAdmin(admin.ModelAdmin):
    list_display = ("user_id", "company_id", "company_name")
admin.site.register(StockList, StockListAdmin)

admin.site.register(StockPrice)

class ReviewInline(admin.TabularInline):
    model = Review

class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline,
    ]
    list_display = ("title", "author", "price",)

admin.site.register(Book, BookAdmin)

