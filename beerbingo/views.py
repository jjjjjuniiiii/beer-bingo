import sqlite3
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
from .forms import RegBeerForm
from .models import Item
from .models import *
from .crawl_and_insert import main
from .filters import BeerFilter
#from .filters import BeerFilter_Check
import simplejson
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.#
def index(request):
   beers = Item.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
   beers_item = Item.objects.all()
   item_list=[];
   for item in beers_item:
      item_list.append(item.name)
   return render(request, 'beerbingo/index.html',{'item_list':item_list})

# def index(request):
# 	beers = Item.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
# 	return render(request, 'beerbingo/index.html', {})
	
def about(request):
	return render(request, 'beerbingo/about.html',{})

def beer_listing(request):
	beers = Item.objects.all()
	item_list=[];
	for item in beers:
		item_list.append(item.name)
	return render(request, 'beerbingo/beer-listing.html',{'item_list':item_list})

def beer_details(request):
	beers = Item.objects.all()
	item_list=[];
	for item in beers:
		item_list.append(item.name)
	return render(request, 'beerbingo/base_search.html',{'item_list':item_list})

def contact(request):
	return render(request, 'beerbingo/contact.html',{})

def write(request):
	return render(request, 'beerbingo/write.html',{})

def login(request):
	return render(request, 'beerbingo/login.html',{})

def crawl_view(request):
	main()
	return render(request, 'beerbingo/auto.html',{})

#list-search/
def search_beer(request):
	beers = Item.objects.all()
	item_list=[];
	for item in beers:
		item_list.append(item.name)

	errors = []
	if request.method == 'GET':	
		search_item = request.GET.get('beer_name')

		if not search_item:
			errors.append('wrong!')
		else :
			searchObj_name = Item.objects.filter(name__icontains=search_item)
			return render_to_response('beerbingo/beer-details.html', {'searchObj' : searchObj_name, 'query' : search_item,'item_list':item_list})	
	return render_to_response('beerbingo/index.html', {'errors' : errors})

def search(request):
	beers = Item.objects.all()
	item_list=[];
	for item in beers:
		item_list.append(item.name)

	errors = []
	if 'search-item' in request.GET :
		search_item = request.GET['search-item']
		if not search_item:
			errors.append('Enter a search Beer!')
		elif len(search_item) > 40 : 
			errors.append('Please enter at most 40 characters.')
		else : 
			searchObj_name = Item.objects.filter(name__icontains=search_item)
			return render_to_response('beerbingo/beer-details.html', {'searchObj' : searchObj_name, 
			'query' : search_item,'item_list':item_list})	

	return render_to_response('beerbingo/index.html', {'errors' : errors})

def search_filtering(request):
	beer_list = Item.objects.all()
	beers_list = Item.objects.all().order_by("name")
	query = request.GET.get("q")
	item_name = [];
	item_style = [];
	item_company = [];
	item_country = [];
	item_rate = [];
	#자동완성
	for item in beer_list:
		item_name.append(item.name)
		item_style.append(item.style)
		item_company.append(item.company)
		item_country.append(item.country)
		item_rate.append(item.rate)
	beer_filter = BeerFilter(request.GET, queryset = beer_list)

	# #페이지네이션
	# paginator = Paginator(item_name, 15) # Show 15 contacts per page
	# page = request.GET.get('page')
	# try:
	# 	beers = paginator.page(page)
	# except PageNotAnInteger:
	# 	# If page is not an integer, deliver first page.
	# 	beers = paginator.page(1)

	# except EmptyPage:
	# 	beers = paginator.page(paginator.num_pages)

	return render(request, "beerbingo/search_form.html", 
		{'filter': beer_filter, 'item_name': item_name, 'item_style':item_style, 'item_company':item_company, 'item_country': item_country, 'item_rate': item_rate,})
    
def photo_album(request):

    item_list = Item.objects.all()
    query = request.GET.get("q")

    if query:
        queryset_list = queryset_list.filter(
            Q(name__icontains=query) |
            Q(style__icontains=query) |
            Q(country__icontains=query) |
            Q(company__icontains=query)

        ).distinct()


    paginator = Paginator(item_list, 20)
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.

        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {

        "object_list": queryset,
        "name": "List",
        "page_request_var": page_request_var,
    }

    return render(request, "beerbingo/home.html", context)



    #자동완성
def auto_complete(request):

   beers = Item.objects.all()
   item_list=[];
   for item in beers:
      item_list.append(item.name)
   json = simplejson.dumps(item_list)
   return HttpResponse(json, content_type='application/javascript')

def to_json(objs, status=200):
	json_str = json.dumps(objs, ensure_ascii=False)
	return HttpResponse(json_str, status = status, content_type='application/json; charset=utf-8')
	
def auto(request):
   beers = Item.objects.all()
   beer_list={}
   for item in beers:
      beer_list[item]=[]
      beer_list[item].append(item.name)
      beer_list[item].append(item.style)
      beer_list[item].append(item.company)
      beer_list[item].append(item.country)
   
   return beer_list

if __name__ == '__auto__':
    auto()

class HomeView(View):
    # @staticmethod
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        chosen_filter = self.request.GET.get('category-filter')
        if chosen_filter:
            items = items.filter(category__category=chosen_filter)
        return render(request, "beerbingo/index.html", {"items": items, 'selected': chosen_filter, 'categories': Item.objects.all().order_by('name')})

def regbeer(request):
    if request.method == 'POST':
        beer_form = RegBeerForm(data=request.POST)

        if beer_form.is_valid():
            bdata = beer_form.cleaned_data.get
            beer_selected = Item.objects.filter(name=bdata('name_select'))
            reg1 = Item(beer_id=beer_selected[0].id, company=bdata('company_select'), country=bdata('country_select'))
            reg1.save()
        else:
            print ('Invalid')

    else:
        beer_form = RegBeerForm()
    return render(request, 'beerbingo/auto.html', {'beer_form': beer_form})

@csrf_exempt
def contact(request):
	errors = []
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid() : 
			cd = form.cleaned_data
			beerName = form.cleaned_data['beerName']
			send_mail(
				#cd['userName'],		
				cd['beerName'],
				cd['beerStyle'],
				cd.get('userEmail','noreply@example.com'),
				['hotty226@naver.com'],					
				cd['beerCompany'],			
				cd['beerCountry'],
				cd['beerDetails'],
				cd['beerImage'],
			)
			insertDB(beerName)
			return HttpResponseRedirect('/contact/thanks/')
			
	else:
		form = ContactForm(
			initial={'beerDetails' : '맥주의 매력을 어필하세요!'}
			)
	return render_to_response('beerbingo/contact.html',{'form' : form})

def insertDB(namee):
    print("insertDB..new Beer..\n")
    item = Item(name = namee)
    item.save()

def contact_email(request):
	return render(request, 'beerbingo/contact-email.html',{})
	
