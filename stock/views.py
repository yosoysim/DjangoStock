from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.contrib.auth.decorators import login_required
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

def stockListview(request):

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

	args = {"company_lov": my_company, "stockPrice": qs,	}

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

@login_required
def StockIndicatorView(request):

	company_lov = StockList.objects.filter(use_yn='Y', user_id=3).order_by('company_id')
	qs = StockIndicator.objects.all().order_by('-txn_date')

	if request.method == "GET":
		companyId = request.session['company_id'] = request.GET.get('company_id')
		from_date = request.session['from_d'] = request.GET.get('from_d')
		to_date = request.session['to_d'] = request.GET.get('to_d')

		if companyId:
			qs = qs.filter(company_id=companyId)



	#return HttpResponse(from_d)
	if not from_date :

		from_date = '2000-01-01'

	if not to_date:
		to_date = '2099-12-31'

	qs = qs.filter(txn_date__gte=from_date, txn_date__lte=to_date)

	args = {"company_lov": company_lov, "curIndicator": qs,}

	return render(request, 'price/stock_indicator.html', args)


@login_required
def StockIndicatorCalView(request):

	#now = datetime.datetime.now()
	now = timezone.now()

	if request.method == "GET":
		# query = self.request.GET.get("q")
		companyId = request.session['company_id']  = request.GET.get('company_id')
		from_date = request.session['from_d'] = request.GET.get('from_d')
		to_date = request.session['to_d'] = request.GET.get('to_d')
		ma5 = 25

	else:
		companyId = '003490'
		from_date = '2017-01-01'
		to_date = '2099-12-31'
		ma5 = 44

	#return HttpResponse(to_date)

	#from_date = '2020-03-14'

	try:
		if companyId:


			indicator_cal = StockIndicator(txn_date=from_date, company_id=companyId, ma5=ma5, upd_d = now )
			indicator_cal.save()

			#success_url = reverse_lazy('indicator')  # 생성 후 이동할 페이지
			#redirection_page = '/price/stock_indicatorCal_completed/'
			redirection_page = '/price/stock_indicatorCal_completed/'

			qs = StockIndicator.objects.all().order_by('-txn_date')

			my_company = StockList.objects.filter(use_yn='Y', user_id=3).order_by('company_id')

			if companyId:
				qs = qs.filter(company_id=companyId)

			qs = qs.filter(txn_date__gte=from_date, txn_date__lte=to_date)
			args = {"curIndicator": qs,
					"companyList": my_company, }

			return render(request, 'price/stock_indicator.html', args)



		else:
			redirection_page = 'error'
	except:
		redirection_page = 'error'

	return redirect(redirection_page)


@login_required
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


@login_required
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


@login_required
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

class BookDetailView(LoginRequiredMixin,	PermissionRequiredMixin, DetailView):
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


@login_required
def StockTxnView(request):
	args = {}
	return render(request, 'txn/stock_txn.html', args)

@login_required
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

@login_required
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

@login_required
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

@login_required
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


"""
class TxnHistoryView(generic.ListView):
	template_name = 'txn/txn_history.html'
	context_object_name = 'txn_history'

	def get_queryset(self):	

		return StockTxn.objects.order_by('-txn_date')
"""

@login_required
def TxnHistoryView(request) :

	template ="txn/txn_history.html"

	if request.method == "POST":
		company_id = request.POST['company_id']
		date_from = request.POST['date_from']
		date_to = request.POST['date_to']
	else:
		date_from = '2018-01-01'
		date_to = '2099-12-31'
		company_id = ''

	request.session['date_from'] = date_from
	request.session['date_to'] = date_to
	request.session['company_id'] = company_id

	#q = StockTxn.objects.filter(txn_date__gt=date_from, txn_date__lte=date_to).filter(company_id__exact=company_id)
	q = StockTxn.objects.filter(txn_date__gt=date_from, txn_date__lte=date_to, company_id__contains=company_id)

	args = ({"txn_history": q})

	return render(request, template, args)


"""
class TxnMonthlyView(generic.ListView):

	template_name = 'txn/txn_monthly.html'
	context_object_name = 'txn_monthly'

	def get_queryset(self):

		return TxnMonthlySQL.objects.order_by('txn_date')
"""

# Connect 이용방법 : 좀 복잡하지만, raw 방식은 반드시 id 컬럼 추가해야 하는 문제 있음.
@login_required
def TxnMonthlyView(request) :

	template ="txn/txn_monthly.html"

	if request.method == "POST":
		date_from = request.POST['date_from']
		date_to = request.POST['date_to']
	else:
		date_from = '2018-01-01'
		date_to = '2099-12-31'
		#return HttpResponse(date_from)

	request.session['date_from'] = date_from
	request.session['date_to'] = date_to

	rows = []
	cursor = connection.cursor()
	# "%%Y%%m" 처럼 %를 두 개 사용해야 함.
	cursor.execute('''SELECT date_format(txn_date, "%%Y%%m") as ym		
							, sum(if(bos = "B", txn_price*txn_qty, 0)) as amt_buy
							, sum(if(bos = "S", txn_price*txn_qty, 0)) as amt_sell
							, sum(txn_fee) as txn_fee
							, max(company_id)
						FROM stock_txn 
						WHERE txn_yn = "Y" 
						AND user_id = 3
						AND txn_date BETWEEN %s AND %s 
						GROUP BY date_format(txn_date, "%%Y%%m")''', [date_from, date_to])

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


@login_required
def TxnPeriodView(request) :

	template ="txn/txn_period.html"

	if request.method == "POST":
		company_id = request.session['company_id'] = request.POST['company_id']
		date_from = request.POST['date_from']
		date_to = request.POST['date_to']
	else:
		date_from = '2018-01-01'
		date_to = '2099-12-31'
		company_id = None
		#return HttpResponse(date_from)

	request.session['date_from'] = date_from
	request.session['date_to'] = date_to

	rows = []
	cursor = connection.cursor()
	# "%%Y%%m" 처럼 %를 두 개 사용해야 함.
	cursor.execute('''SELECT x.company_id 		
							, t.qty
							, t.profit/t.qty as avg_buy_price
							, sum(if(bos = "B", txn_qty, 0)) as qty_buy
							, sum(if(bos = "B", txn_price*txn_qty, 0)) as amt_buy
							, sum(if(bos = "S", txn_qty, 0)) as qty_sell
							, sum(if(bos = "S", txn_price*txn_qty, 0)) as amt_sell
							, sum(x.txn_fee) as txn_fee
							, sum(if(bos = "S", txn_price*txn_qty, 0)) - sum(if(bos = "B", txn_price*txn_qty, 0)) as profit
						FROM stock_txn x 
						LEFT JOIN stock_txn_temp t
						USING (company_id, user_id) 
						WHERE txn_yn = "Y" 
						AND x.user_id = 3
						AND x.company_id like %s
						AND txn_date BETWEEN %s AND %s 
						GROUP BY x.company_id, t.qty, t.profit/t.qty''', ['%' + company_id + '%', date_from, date_to])

	for row in cursor.fetchall():
		d = dict()
		d['company_id'] = row[0]
		d['qty'] = row[1]
		d['avg_price'] = row[2]
		d['qty_buy'] = row[3]
		d['amt_buy'] = row[4]  #' bos'하면 안 됨.
		d['qty_sell'] = row[5]
		d['amt_sell'] = row[6]
		d['txn_fee'] = row[7]
		d['profit'] = row[8]

		rows.append(d)

	args = ({"txn_period": rows})

	return render(request, template, args)


"""
# 장고의 raw()이용 방법
class TxnMonthlyView(generic.ListView):

	template = "txn/txn_monthly.html"

	def get(self, request):

		if request.method == "POST":
			date_from = request.POST['date_from']
			date_to = request.POST['date_to']

			return HttpResponse(date_from)
		
		#q = "select date_format(txn_date, '%Y%m') as ym, sum(if(bos = 'B', txn_price*txn_qty, 0)) as amt_buy, sum(if(bos = 'S', txn_price*txn_qty, 0)) as amt_sell, sum(txn_fee) as txn_fee, max(company_id) from stock_txn GROUP BY date_format(txn_date, '%Y%m')";
		q = "select id, sum(txn_fee) as txn_fee from stock_txn GROUP BY id"; #Raw query must include the primary key 문제 발생하여 반드시 id 추가해야 함. 그러면 내 의도가 안 됨.
		rows = StockTxn.objects.raw(q)
		args = {"txn_monthly": rows}

		return render(request, self.template, args)
"""

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

@login_required
def BacktestAllView(request) :

	template = "backtest/backtest_all.html"

	if request.method == "POST":
		company_id = request.session['company_id'] = request.POST['company_id']
		date_from = request.POST['date_from']
		date_to = request.POST['date_to']
	else:
		date_from = '2018-01-01'
		date_to = '2099-12-31'
		company_id = None
		#return HttpResponse(date_from)

	request.session['date_from'] = date_from
	request.session['date_to'] = date_to

	company_id ='003490'
	date_from = '2018-01-01'
	date_to = '2022-01-01'

	rf_rate = 1
	pick_freq_rise = 60
	target_days = 7

	rows = []
	cursor = connection.cursor()
	# "%%Y%%m" 처럼 %를 두 개 사용해야 함.
	cursor.execute('''SELECT z.company_name, z.company_id, z.dom_yn
						, sum(if(z.hammer1 > 0, 1, 0)) as cnt_hammer1_up
						, sum(if(z.rf = z.hammer1 && z.rf > 0, 1, 0)) as hammer1_up  
						, round(avg(if(z.hammer1 > 0, z.rf2, null)), 1) as hammer1_up_rf  
						, sum(if(z.hammer1 < 0, 1, 0)) as cnt_hammer1_dn   
						, sum(if(z.rf = z.hammer1 && z.rf < 0, 1, 0)) as hammer1_dn  
						, round(avg(if(z.hammer1 < 0, z.rf2, null)), 1) as hammer1_dn_rf 						
						, sum(if(z.hammer2 > 0, 1, 0)) as cnt_hammer2_up
						, sum(if(z.rf = z.hammer2 && z.rf > 0, 1, 0)) as hammer2_up  
						, round(avg(if(z.hammer2 > 0, z.rf2, null)), 1) as hammer2_up_rf  
						, sum(if(z.hammer2 < 0, 1, 0)) as cnt_hammer2_dn   
						, sum(if(z.rf = z.hammer2 && z.rf < 0, 1, 0)) as hammer2_dn  
						, round(avg(if(z.hammer2 < 0, z.rf2, null)), 1) as hammer2_dn_rf  						
					FROM ( 
						SELECT c.company_name, c.company_id, co.dom_yn 
						, a.txn_date 
						, if(round(100*(if(%s > 1, a.price_avg, a.price_close) - x.price_close)/x.price_close, 0) >= %s, 1, if(round(100*(if(%s > 1, a.price_avg, a.price_close) - x.price_close)/x.price_close, 0) <= %s*-1, -1, 0)) as rf 
						, round(100*(if(%s > 1, a.price_avg, a.price_close) - x.price_close)/x.price_close, 2) as rf2 
						, if(x.c_hammer1 > 0, 1, if(x.c_hammer1 < 0, -1, 0)) as hammer1    
						, if(x.c_hammer2 > 0, 1, if(x.c_hammer2 < 0, -1, 0)) as hammer2
		FROM stock_company co, stock_list c 
			, stock_price a 
			, (SELECT p.price_close  
					, (SELECT y.txn_date 
						FROM stock_ymd y 
						WHERE y.txn_date >= DATE_ADD(p.txn_date, INTERVAL %s DAY) LIMIT 1) as txn_date_pre 
					, b.*
				FROM stock_score_log b, stock_price p 
				WHERE p.txn_date = b.txn_date 
					AND p.price_close > 0 
					AND p.company_id = b.company_id 
					AND p.company_id LIKE %s 
					AND p.txn_date BETWEEN %s AND %s
					AND b.user_id  = 3                                      ) x 
		WHERE c.user_id 	= 3 
			AND c.company_id 	LIKE %s     
			AND a.company_id 	= c.company_id   
			AND a.txn_date 		= x.txn_date_pre 
			AND c.company_id 	= x.company_id 
			AND c.company_id 	= co.company_id
			AND c.use_yn 		= 'Y' 
			AND if(%s > 1, a.price_avg, a.price_close)   > 0 
			AND x.price_close > 0                                                   ) z
		  GROUP BY z.company_name, z.company_id, z.dom_yn 
		   HAVING count(z.rf)  > 0 
		  ORDER BY z.dom_yn, z.company_name''', [rf_rate, pick_freq_rise, rf_rate, pick_freq_rise, target_days, target_days, '%' + company_id + '%', date_from, date_to,	'%' + company_id + '%', target_days])

	for row in cursor.fetchall():
		d = dict()
		d['company_name'] = row[0]
		d['company_id'] = row[1]
		d['dom_yn'] 	= row[2]
		d['cnt_hammer1_up'] = row[3]
		d['hammer1_up'] = row[4]
		d['hammer1_up_rf'] = row[5]
		d['cnt_hammer1_dn'] = row[6]
		d['hammer1_dn'] = row[7]
		d['hammer1_dn_rf'] = row[8]

		d['cnt_hammer2_up'] = row[9]
		d['hammer2_up'] = row[10]
		d['hammer2_up_rf'] = row[11]
		d['cnt_hammer2_dn'] = row[12]
		d['hammer2_dn'] = row[13]
		d['hammer2_dn_rf'] = row[14]
		rows.append(d)

	args = ({"backtest": rows})

	return render(request, template, args)



class StockChangeHistoryView(LoginRequiredMixin, generic.ListView):
	template_name = 'setup/stock_change_history.html'
	context_object_name = 'change_history'

	def get_queryset(self):
		return StockChangeHis.objects.order_by('-txn_date')


def ErrorView(request):
	return render(request, 'error.html')

# 실패 : 이것은 stock/stockcompany_list.html 를 쫒아간다..대충 알겠다. 나는 폴더를 별도로 만들고 앱을 여러개 만들었으니 안 먹힌다.
#class StockCompanyListView(ListView):
#	model = StockCompany


class StockCompanyView(LoginRequiredMixin, generic.ListView):
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


class StockCompanyCreateView(LoginRequiredMixin, CreateView):
	model = StockCompany
	fields = ['company_id', 'company_name', 'pod', 'dom_yn', 'baedang', 'is_active']
	success_url = reverse_lazy('stockCompany')  # 글쓰기를 완료했을 때 이동할 페이지
	template_name = 'setup/stock_company_create.html'


class StockCompanyUpdateView(LoginRequiredMixin, UpdateView):
	model = StockCompany
	fields = ['company_id', 'company_name', 'pod', 'dom_yn', 'baedang', 'is_active']
	success_url = reverse_lazy('stockCompany')  # 글쓰기를 완료했을 때 이동할 페이지
	template_name = 'setup/stock_company_update.html'

class StockCompanyDetailView(LoginRequiredMixin, DetailView):
	model = StockCompany
	template_name = 'setup/stock_company_detail.html'  # 이걸 명시하지 않아서 지금까지 개고생...


class StockCompanyDeleteView(LoginRequiredMixin, DeleteView):
	model = StockCompany
	success_url = reverse_lazy('stockCompany')  # 글쓰기를 완료했을 때 이동할 페이지
	template_name = 'setup/stock_company_delete.html'

# score master 

class ScoreMasterView(LoginRequiredMixin, generic.ListView):
	model = StockScoreMaster
	template_name = 'setup/score_master.html'
	context_object_name = 'scoreMaster'

	paginate_by = 6

	# 아래는 굳이 추가 안 해도 됨.(정렬 때문에 추가함)
	def get_queryset(self):
		return StockScoreMaster.objects.order_by('seq_id')


class ScoreMasterCreateView(LoginRequiredMixin, CreateView):
	model = StockScoreMaster
	fields = ['company_id', 'company_name', 'pod', 'dom_yn', 'baedang', 'is_active']
	success_url = reverse_lazy('scoreMaster')  # 생성 후 이동할 페이지
	template_name = 'setup/score_master_create.html'


class ScoreMasterUpdateView(LoginRequiredMixin, UpdateView):
	model = StockScoreMaster
	fields = ['item', 'item_desc', 'def_field', 'plus', 'minus', 'criteria1']
	success_url = reverse_lazy('scoreMaster')  # 갱신 후 이동할 페이지
	template_name = 'setup/score_master_update.html'

class ScoreMasterDetailView(LoginRequiredMixin, DetailView):
	model = StockScoreMaster
	#context_object_name = 'scoreDetail'
	template_name = 'setup/score_master_detail.html'  # 이걸 명시하지 않아서 지금까지 개고생...

class ScoreMasterDeleteView(LoginRequiredMixin, DeleteView):
	model = StockScoreMaster
	success_url = reverse_lazy('scoreMaster')  # 글쓰기를 완료했을 때 이동할 페이지
	template_name = 'setup/score_master_delete.html'

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

@login_required
def item_detail(request, id, item_slug=None):
    item = get_object_or_404(StockScoreMaster, id=id, slug=StockScoreMaster)
    #add_to_cart = AddProductForm(initial={'quantity':1})
    return render(request, 'setup/stock_item_master_detail.html', {'item': item})
