#from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views # generic view 용.
#from .views import BookListView, BookDetailView, SearchResultsListView

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('', main_page, name='main'),
    path('', HomePageView.as_view(), name='home'),
    #path('price/', MenuPriceView, name='menu_price'),
    path('price/indicator', StockIndicatorView, name='indicator'),
    path('price/indicator_cal', StockIndicatorCalView, name='indicatorCal'),
    path('price/indicator_edit', StockIndicatorEditView, name='indicatorEdit'),
    path('price/indicator_all_recal', StockIndicatorAllCalView, name='indicatorAllReCal'),
    path('price/stock_indicatorCal_completed/', IndicatorCalCompletedView, name='indicalorCalcompleted'),
    path('price/stock_list', stock_list_view, name='stocklist'),
    path('price/stock_price', StockPiceView, name='stockprice'),
    #path('price/stock_price/search', stock_price_view_search.as_view(), name='stockprice_search'),

    path('txn/stock_txn', StockTxnView, name='stocktxn'),
    path('txn/stock_txn_res', StockTxnInputView, name='stocktxninput'), #path('user_register_res/', user_register_result, name='registerres'),
    path('txn/txn_input_completed/', TxnInputCompleted, name='txninputcompleted'),
    #path('txn/txn_cash', views.TxnCashView.as_view(), name='txnCash'),
    path('txn/txn_cash', TxnCashView, name='txnCash'),
    path('txn/txn_cash/add/', TxnCashInputView, name='txnCashAdd'),
    path('txn/txn_history', views.TxnHistoryView.as_view(), name='txnHistory'),
    #path('txn/txn_monthly', views.TxnMonthlyView.as_view(), name='txnMonthly'),
    path('txn/txn_monthly', TxnMonthlyView, name='txnMonthly'),

    path('setup/stock_change_history', views.StockChangeHistoryView.as_view(), name='stockChangeHistory'),

    #path('setup/stock_company_list', StockCompanyListView.as_view(), name='stockCompany'), 실패
    path('setup/stock_company/', views.StockCompanyView.as_view(), name='stockCompany'), #clsss로 할 경우
    path('setup/stock_company/add/', StockCompanyCreateView.as_view(), name='addCompany'),
    path('setup/stock_company/update/<int:pk>/', StockCompanyUpdateView.as_view(), name='updateCompany'),
    path('setup/stock_company/delete/<int:pk>/', StockCompanyDeleteView.as_view(), name='deleteCompany'),
    path('setup/stock_company/detail/<int:pk>/', StockCompanyDetailView.as_view(), name='detailCompany'),

    path('setup/stock_item_master', item_in_category, name='item_all'),
    path('setup/stock_item_master/<slug:category_slug>/', item_in_category, name='item_in_category'),
    #path('setup/stock_item_master/<int:id>/', item_in_category, name='item_in_category'),
    path('setup/stock_item_master_detail/<int:id>/<item_slug>/', item_detail, name='item_detail'),
    #path('setup/stock_item_master_detail/<int:id>/', item_detail, name='item_detail'),

    #path('setup/stock_company/', StockCompanyView, name='stockCompany'),  function으로 할 경우

    path('signup/', SignupPageView.as_view(), name='signup'),
    path('about/', AboutPageView.as_view(), name='about'),

    path('books', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>', BookDetailView.as_view(), name='book_detail'), # int -> uuid : 안 바꿈. 무슨 난수표 같아서..
    path('books/search', SearchResultsListView.as_view(), name='search_results'),

    path('orders', OrdersPageView.as_view(), name='orders'),

    path('error', ErrorView, name='error'),

]
