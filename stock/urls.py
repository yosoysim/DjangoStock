#from django.contrib import admin
from django.urls import path, include
from .views import *
#from .views import BookListView, BookDetailView, SearchResultsListView

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('', main_page, name='main'),
    path('', HomePageView.as_view(), name='home'),
    path('stock_list', stock_list_page, name='stocklist'),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('about/', AboutPageView.as_view(), name='about'),

    path('books', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>', BookDetailView.as_view(), name='book_detail'), # int -> uuid : 안 바꿈. 무슨 난수표 같아서..
    path('books/search', SearchResultsListView.as_view(), name='search_results'),

    path('orders', OrdersPageView.as_view(), name='orders'),
]
