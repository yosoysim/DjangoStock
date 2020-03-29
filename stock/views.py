from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
#import datetime
from django.utils import timezone

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, ListView
from django.views.generic.list import ListView # stockCompany 용도.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.http import JsonResponse
from .forms import *
from .models import *
from django.db.models import Avg
#from django.db import connection # raw sql 사용 위함.

#from django.http import HttpResponse



def main_view(request):
	#return HttpResponse('Hello, Sim')
	return render(request, 'main.html')
	#return redirect('main.html')

def stock_list_view(request):

	stock_list = StockList.objects.all()
	args = {}
	args.update({"stockList": stock_list})
	#args = {"stockList": stock_list}

	return render(request, 'price/stock_list.html', args)


# 아래는 all 조회 또는 조회를 하드코딩 하는 방식임.
"""
def stock_price_view(request):

	#stock_list = StockList.objects.get(user_id=1)
	qs = StockPrice.objects.all()
	args = {}
	args.update({"stockPrice": qs})  # stockPrice : 커서 역할을 함. html에서.

	return render(request, 'price/stock_price.html', args)
"""

def StockPiceView(request):

	qs = StockPrice.objects.all().order_by('-txn_date')
	#my_company = MyCompanyList() #dropdown 용도 from forms.py
	my_company = StockList.objects.filter(use_yn='Y', user_id=3).order_by('company_id')

	company = request.GET.get('q', '')  # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기 <-- 안 되는 듯..

	request.session['company_id'] = company

	if company:
		qs = qs.filter(company_id=company)

	from_d = request.session['from_d'] = request.GET.get('from_d')
	to_d = request.session['to_d'] = request.GET.get('to_d')

	if from_d or to_d :

		if not from_d :
			from_d = '2000-01-01'

		if not to_d:
			to_d = '2099-12-31'

		qs = qs.filter(txn_date__gte=from_d, txn_date__lte=to_d)

	args = {"stockPrice": qs,
			"companyList": my_company, }

	return render(request, 'price/stock_price.html', args)


"""
class SearchFormView():
	form_class = stock_price_view_search
	template_name = 'blog/search.html'

	def form_valid(self,form): # post method로 값이 전달 됬을 경우
 		word = '%s' %self.request.POST['word'] # 검색어
		post_list = Post.objects.filter(
			Q(title__icontains=word) | Q(content__icontains=word) # Q 객체를 사용해서 검색한다.
				# title,context 칼럼에 대소문자를 구분하지 않고 단어가 포함되어있는지 (icontains) 검사 )
		) .distinct() #중복을 제거한다.
		context = {}
		context['object_list'] = post_list # 검색된 결과를 컨텍스트 변수에 담는다.
		context['search_word']= word # 검색어를 컨텍스트 변수에 담는다.
		return context

"""

def StockIndicatorView(request):

	qs = StockIndicator.objects.all().order_by('-txn_date')

	my_company = StockList.objects.filter(use_yn='Y', user_id=3).order_by('company_id')
	company = request.session['company_id']  = request.GET.get('q', '')

	if company:
		qs = qs.filter(company_id=company)

	from_d = request.session['from_d'] = request.GET.get('from_d')
	to_d = request.session['to_d'] = request.GET.get('to_d')

	if from_d or to_d :

		if not from_d :
			from_d = '2000-01-01'

		if not to_d:
			to_d = '2099-12-31'

		qs = qs.filter(txn_date__gte=from_d, txn_date__lte=to_d)

	args = {"curIndicator": qs,
			"companyList": my_company, }

	return render(request, 'price/stock_indicator.html', args)


def StockIndicatorCalView(request):

	#now = datetime.datetime.now()
	now = timezone.now()

	if request.method == "GET":
		companyId = '003490' #request.POST['company_id']
		txnDate ='2020-03-17'
		ma5 = 11

	try:
		if companyId:

			indicator_cal = StockIndicator(txn_date=txnDate, company_id = companyId, ma5=ma5, upd_d = now )
			indicator_cal.save()

			redirection_page = '/price/stock_indicatorCal_completed/'

		else:
			redirection_page = 'error'
	except:
		redirection_page = 'error'

	return redirect(redirection_page)



def StockIndicatorEditView(request):

	now = timezone.now()

	#return HttpResponse(str(request.method)) # JS를 통하면 무조건 GET으로 변한다.
	if request.method == "GET":
		#editId = request.POST.get('edit_id')
		#editId = request.GET['key_id'] # 이것은 MultiValueDictKeyError 발생
		editId = request.GET.get('key_id')
		#return HttpResponse(str(editId))

	try:
		if editId:

			qs = StockIndicator.objects.get(id=editId)
			ma5_edit = 455

			qs.ma5 = ma5_edit
			qs.upd_d = now
			qs.save()

			redirection_page = '/price/stock_indicatorCal_completed/'  # redirect 할 경우는 이처럼  '/price/ ~~
			#redirection_page = 'price/stock_indicatorCal_completed.html' # render할 경우는 그냥 'price/~~

		else:
			redirection_page = 'error'
			#redirection_page = 'error.html'
	except:
		redirection_page = 'error'  ######### redirect 시에는 앞/뒤에 모두 '/'이 없어야 함.
		#redirection_page = 'error.html'


	return redirect(redirection_page)
	#return render(request, redirection_page)



def StockIndicatorAllCalView(request):

	now = timezone.now()


	if request.method == "GET":

		txnDate = request.GET.get('txn_date')
		editId = request.GET.get('key_id')

		#return HttpResponse(str(txnDate))  OK

	#try:
		if txnDate:

			#return HttpResponse(str(txnDate))

			#qs = StockIndicator.objects.get(txn_date='2020-03-17') ok. 17일 데이터가 단 한개만 있기 때문에 운 좋게 걸린 것임.
			qs = StockIndicator.objects.filter(txn_date__exact = txnDate)
			#qs = StockIndicator.objects.get(txn_date = txnDate)  #ok
			#qs = StockIndicator.objects.get(company_id = '003490')   #오류. get은 단 1개만 추출함!!
			#qs = StockIndicator.objects.filter(company_id='003490').first()  ok
			#qs = qs.filter(txn_date__exact = txnDate)

			for c1 in qs:

				c1.ma5 = 0
				c1.ma10 = 0
				c1.upd_d = now
				c1.save()

				#. 여기 개발 차례임. 종목을 발췌하여 평균 구하기.

				#q2 = StockPrice.objects.filter(txn_date__gt = txnDate).filter(c1.company_id__exact = "003490")
				#q2 = StockPrice.objects.filter(txn_date__gt = '2018-01-01').filter(txn_date__lte='2020-03-15')
				q2 = StockPrice.objects.filter(txn_date__gt='2019-02-01').filter(txn_date__lte='2020-03-15')
				get_average = q2.aggregate(Avg('price_close'))


				return HttpResponse(str(get_average))
				#c1.company_id

			#return HttpResponse(str(qs.ma5)) # 아!!! 이놈이 문제 였구나..




			redirection_page = '/price/stock_indicatorCal_completed/'  # redirect 할 경우는 이처럼  '/price/ ~~
			#redirection_page = 'price/stock_indicatorCal_completed.html' # render할 경우는 그냥 'price/~~

		else:
			redirection_page = 'error'

	#except:
	#	redirection_page = 'error'


	return redirect(redirection_page)



def IndicatorCalCompletedView(request):
	return render(request,  'price/stock_indicatorCal_completed.html')

class HomePageView(TemplateView):
    template_name = 'home.html'

class SignupPageView(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/signup.html' #registeration

class AboutPageView(TemplateView):
    template_name = 'about.html'

class BookListView(LoginRequiredMixin, ListView):
	model = Book
	context_object_name = 'book_list'
	template_name = 'books/book_list.html'
	login_url = 'account_login'

class BookDetailView(
	LoginRequiredMixin,
	PermissionRequiredMixin,
	DetailView):
	model = Book
	context_object_name = 'book' # html 파일에서 object_list를 명시적으로 표현하기 위해.
	template_name = 'books/book_detail.html'
	login_url = 'account_login'
	permission_required = 'books.special_status'


class OrdersPageView(TemplateView):
    template_name = 'orders/purchase.html'


class SearchResultsListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )


def StockTxnView(request):
	args = {}
	return render(request, 'txn/stock_txn.html', args)

def StockTxnInputView(request):

	if request.method == "POST":
		companyId = request.POST['company_id']
		txnQty = request.POST['txn_qty']
		txnPrice = request.POST['txn_price']
		bos = request.POST['bos']
		txnYn = request.POST['txn_yn']
		txnFee = int(request.POST['txn_fee'])
		txnDate = request.POST['txn_date']
		bosReason = request.POST['bos_reason']
		bosReasonDetail = request.POST['bos_reason_detail']
		txn_seq = 1

	try:
		if txn_seq:

			txn = StockTxn(txn_seq=txn_seq, user_id=3, bos=bos, txn_date=txnDate, txn_time=txnDate,
						company_id = companyId, txn_yn = txnYn,  txn_qty = txnQty, txn_price = txnPrice, txn_fee = txnFee,
						bos_reason = bosReason,  bos_reason_detail = bosReasonDetail	)
			txn.save()
			"""
			reset_yn = models.CharField(max_length=1, blank=True, null=True)
			close_yn = models.CharField(max_length=1, blank=True, null=True)
			cash_inout = models.IntegerField(blank=True, null=True)
			cash_balance = models.IntegerField(blank=True, null=True)
			asis_price = models.IntegerField(blank=True, null=True)
			target_period = models.IntegerField(blank=True, null=True)
			target_price = models.IntegerField(blank=True, null=True)
			target_date = models.DateField(blank=True, null=True)  
			result_review = models.CharField(max_length=250, blank=True, null=True)
			upd_d = models.DateTimeField(blank=True, null=True)
			"""

			redirection_page = '/txn/txn_input_completed/'

		else:
			redirection_page = '/stock/error/'
	except:
		redirection_page = '/stock/error/'

	#return render(request, 'txn/txn_input_completed.html')
	return redirect(redirection_page)

def TxnInputCompleted(request):
	return render(request,  'txn/txn_input_completed.html')


"""
class TxnCashView(generic.ListView):
	#model = StockTxn
	#queryset = StockTxn.objects.all()
	#queryset = StockTxn.objects.filter(txn_seq=61)
	#queryset = StockTxn.objects.get(txn_seq=61) 단일 api는 모두 에러남.
	#queryset = qs.latest('-txn_seq')
	template_name = 'txn/txn_cash.html'
	context_object_name = 'cash_asis'
	
	def get_queryset(self):
		#return StockTxn.objects.last()

		#queryset = StockTxn.objects.latest('-txn_seq')
		#queryset = StockTxn.objects.filter(txn_seq=61)

		return self.queryset
		#return StockTxn.objects.latest('-txn_seq')
		#return model.objects.order_by('-txn_date')
"""


def TxnCashView(request):

	qs = StockTxn.objects.order_by("-txn_seq")[:1]
	args = {"cash_asis": qs }

	return render(request, 'txn/txn_cash.html', args)

"""
class TxnCashView(CreateView):
	model = StockCompany
	fields = ['company_id', 'company_name', 'pod', 'dom_yn', 'baedang', 'is_active']
	success_url = reverse_lazy('stockCompany')  # 글쓰기를 완료했을 때 이동할 페이지
	template_name = 'setup/stock_company_create.html'
"""

def TxnCashInputView(request):

	now = timezone.now()

	if request.method == "POST":
		balance = request.POST['cash_balance']
		cashIn = request.POST['cash_in']
		cashOut = request.POST['cash_out']

		if not cashIn:
			cashIn = 0

		#if cashOut is None:
		if not cashOut:
			cashOut = 0

		cashNet = int(balance) + int(cashIn) - int(cashOut) # 장고는 string임.

		txn_seq = int(request.POST['txn_seq'])

	try:
		if cashNet  > 0 :

			q = StockTxn(cash_balance=cashNet, bos = 'C', txn_yn='Y', upd_d = now, txn_seq=txn_seq+1, company_id='' )
			q.save()

			redirection_page = '/txn/txn_cash'

		else:
			redirection_page = '/stock/error/'
	except:
		redirection_page = '/stock/error/'

	return redirect(redirection_page)



class TxnHistoryView(generic.ListView):
	template_name = 'txn/txn_history.html'
	context_object_name = 'txn_history'

	def get_queryset(self):
		return StockTxn.objects.order_by('-txn_date')

"""
class TxnMonthlyView(generic.ListView):

	template_name = 'txn/txn_monthly.html'
	context_object_name = 'txn_monthly'

	def get_queryset(self):

		return TxnMonthlySQL.objects.order_by('txn_date')
"""

"""
class TxnMonthlyView(generic.ListView):
	template_name = 'txn/txn_monthly.html'

	def get(self, request):
		query = 'select company_id, bos, txn_qty, txn_price, txn_fee, txn_date from stock_txn'
		cursor = connection.cursor()
		row = cursor.execute(query)
		rows = row.fetchall()
		data = list()
		for i in rows:
			d = dict()
			d['company_id'] = i[0]
			d['bos'] = i[1]
			d['txn_qty'] = i[2]
			d['txn_price'] = i[3]
			d['txn_fee'] = i[4]
			data.append(d)		
		return render(request, self.template_name, {'txn_monthly': data})
"""

def TxnMonthlyView(request) :

	template ="txn/txn_monthly.html"
	rows = []
	cursor = connection.cursor()
	cursor.execute('''SELECT date_format(txn_date, '%Y%m') as ym		
		, sum(if(bos = 'B', txn_price*txn_qty, 0)) as amt_buy
		, sum(if(bos = 'S', txn_price*txn_qty, 0)) as amt_sell
		, sum(txn_fee) as txn_fee
		, max(company_id)
		FROM stock_txn 
		WHERE txn_yn = "Y" 
		AND user_id = 3
		GROUP BY date_format(txn_date, '%Y%m')''')

	for row in cursor.fetchall():
		d = dict()
		d['ym'] = row[0]
		d['amt_buy'] = row[1]  #' bos'하면 안 됨.
		d['amt_sell'] = row[2]
		d['txn_fee'] = row[3]
		d['company_id'] = row[4]

		rows.append(d)

	args = ({"txn_monthly": rows})

	return render(request, template, args)


"""
#from django.db import connection
def TxnMonthlyView(self):

    with connection.cursor() as cursor:
		
		#cursor.execute("SELECT * FROM stock_txn WHERE txn_yn = %s", [self.txn_yn])
		#cursor.execute("SELECT * FROM stock_txn")
        #row = cursor.fetchone()
		result = cursor.fetchall()

    return result


	#template_name = 'txn/txn_monthly.html'
	#context_object_name = 'txn_monthly'
"""

class StockChangeHistoryView(generic.ListView):
	template_name = 'setup/stock_change_history.html'
	context_object_name = 'change_history'

	def get_queryset(self):
		return StockChangeHis.objects.order_by('-txn_date')


def ErrorView(request):
	return render(request, 'error.html')

# 실패 : 이것은 stock/stockcompany_list.html 를 쫒아간다..대충 알겠다. 나는 폴더를 별도로 만들고 앱을 여러개 만들었으니 안 먹힌다.
#class StockCompanyListView(ListView):
#	model = StockCompany


class StockCompanyView(generic.ListView):
	model = StockCompany
	template_name = 'setup/stock_company.html'
	context_object_name = 'stock_company'

	paginate_by = 6

	# 아래는 굳이 추가 안 해도 됨.(정렬 때문에 추가함)
	def get_queryset(self):
		return StockCompany.objects.order_by('company_name')

""" function으로 할 경우
def StockCompanyView(request):
	qs = StockCompany.objects.order_by('company_name')
	#args = {}
	#args.update = ({'stock_company': qs })
	args = ({'stock_company': qs})
	return render(request, 'setup/stock_company.html', args)
"""


class StockCompanyCreateView(CreateView):
	model = StockCompany
	fields = ['company_id', 'company_name', 'pod', 'dom_yn', 'baedang', 'is_active']
	success_url = reverse_lazy('stockCompany')  # 글쓰기를 완료했을 때 이동할 페이지
	template_name = 'setup/stock_company_create.html'


class StockCompanyUpdateView(UpdateView):
	model = StockCompany
	fields = ['company_id', 'company_name', 'pod', 'dom_yn', 'baedang', 'is_active']
	success_url = reverse_lazy('stockCompany')  # 글쓰기를 완료했을 때 이동할 페이지
	template_name = 'setup/stock_company_update.html'

class StockCompanyDetailView(DetailView):
	model = StockCompany
	template_name = 'setup/stock_company_detail.html'  # 이걸 명시하지 않아서 지금까지 개고생...


class StockCompanyDeleteView(DeleteView):
	model = StockCompany
	success_url = reverse_lazy('stockCompany')  # 글쓰기를 완료했을 때 이동할 페이지
	template_name = 'setup/stock_company_delete.html'


def item_in_category(request, category_slug=None):
	current_category = None
	categories = Category.objects.all()
	items = StockScoreMaster.objects.filter(use_yn='Y')


	if category_slug:
	    current_category = get_object_or_404(Category, slug=category_slug)
	    items = items.filter(category=current_category)

	return render(request, 'setup/stock_item_master.html',
			  {'current_category': current_category, 'categories': categories, 'items': items})


"""
def item_in_category(request):
	current_category = None
	categories = Category.objects.all()
	#items = StockScoreMaster.objects.filter(use_yn='Y')
	items = StockScoreMaster.objects.all()

	args = {"categories": categories, "items": items}

	return render(request, 'setup/stock_item_master.html', args)
"""

def item_detail(request, id, item_slug=None):
    item = get_object_or_404(StockScoreMaster, id=id, slug=StockScoreMaster)
    #add_to_cart = AddProductForm(initial={'quantity':1})
    return render(request, 'setup/stock_item_master_detail.html', {'item': item})
