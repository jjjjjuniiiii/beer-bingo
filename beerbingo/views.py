from django.shortcuts import render
from django.utils import timezone
from .models import Item
from .crawl_and_save_in_csv import main
from django.shortcuts import redirect
# Create your views here.#
#def index(request):
	#beers = Beer.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#	return render(request, 'beerbingo/index.html', {'beers': beers})

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

def crawl_view(request):
	# main = crawl_and_save_in_csv(request.Post)
	# mains = main.objects.all()
	# return HttpResponse(mains)
	main()