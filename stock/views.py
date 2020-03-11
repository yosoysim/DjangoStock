from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from stock.models import StockList, Book
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.db.models import Q


from .forms import CustomUserCreationForm


def main_page(request):
	#return HttpResponse('Hello, Sim')
	return render(request, 'main.html')
	#return redirect('main.html')

def stock_list_page(request):

	#stock_list = StockList.objects.filter(article__id=article).order_by('company_name')
	#stock_list = StockList.objects.get(user_id=1)
	stock_list = StockList.objects.all()

	args = {}
	args.update({"stockList": stock_list})

	return render(request, 'stock_list.html', args)



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