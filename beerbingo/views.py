from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils import timezone
from .models import Item
from .crawl_and_save_in_csv import main
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from beerbingo.forms import ContactForm
import sqlite3
from .models import Item

# Create your views here.#

def index(request):
	beers = Item.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
	return render(request, 'beerbingo/index.html', {})
	
def about(request):
	return render(request, 'beerbingo/about.html',{})

def beer_listing(request):
	return render(request, 'beerbingo/beer-listing.html',{})

def beer_details(request):
	return render(request, 'beerbingo/beer-details.html',{})

def contact(request):
	return render(request, 'beerbingo/contact.html',{})

def write(request):
	return render(request, 'beerbingo/write.html',{})

def login(request):
	return render(request, 'beerbingo/login.html',{})

def crawl_view(request):
	# main = crawl_and_save_in_csv(request.Post)
	# mains = main.objects.all()
	# return HttpResponse(mains)
	main

def search_beer(request):
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
			'query' : search_item})	

	return render_to_response('beerbingo/index.html', {'errors' : errors})
		#return HttpResponse('Please submit a search beer!')

# @csrf_exempt
# def contact(request):
# 	errors = []
# 	if request.method == 'POST':
# 		if not request.POST.get('contact-name',''):
# 			errors.append('Enter your name!')
# 		if not request.POST.get('contact-beer-name',''):
# 			errors.append('Enter your beer name!')
# 		if request.POST.get('contact-email') and '@' not in request.POST['contact-email'] : 
# 			errors.append('Enter a valid e-mail address.')
# 		if not errors : 
# 			send_mail(
# 				request.POST['contact-name'],
# 				request.POST.get('contact-email','noreply@example.com'),
			
# 				request.POST['contact-beer-name'],
# 				['siteowner@example.com'],
# 				)
# 			return HttpResponseRedirect('/contact/thanks/')

# 	return render_to_response('beerbingo/contact.html', {
# 		'errors' : errors,
# 		'contact_name' : request.POST.get('contact-name',''),
# 		'contact_beer_name' : request.POST.get('contact-beer-name',''),
# 		'contact_email' : request.POST.get('contact-email',''),
# 		})

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
	
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.User
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'beerbingo/post_edit.html', {'form': form})

# def post_detail(request):
# 	return render(request, 'beerbingo/post_detail.html',{})

# def post_list(request):
# 	return render(request, 'beerbingo/post_list.html',{})