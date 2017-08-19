from django import forms
from .models import Item
import json
from .models import *

class RegBeerForm(forms.ModelForm):

    companies = {}
    countries = {}
    names = {}
    list_names = []
    list_companies = []
    list_countries = []
    for beer in Item.objects.all():
        if beer.company in companies:
            companies[beer.company].append(beer.company)
        else:
            companies[beer.company] = [beer.company]

        list_companies.append((beer.company, beer.company))

        if beer.country in countries:
            countries[beer.country].append(beer.country)
        else:
            countries[beer.country] = [beer.name]

        list_countries.append((beer.country, beer.country))

        if beer.name in names:
            names[beer.name].append(beer.name)
        else:
            names[beer.name] = [beer.name]

        list_names.append((beer.name, beer.name))

  
    name_select = forms.ChoiceField(choices=(list_names))
    company_select = forms.ChoiceField(choices=(list_companies))
    country_select = forms.ChoiceField(choices=(list_countries))

    names = json.dumps(names)
    companies = json.dumps(companies)
    countries = json.dumps(countries)

    class Meta:
        model = Item
        fields = ('name_select', 'company_select', 'country_select',)


class ContactForm(forms.Form):
	"""docstring for ContactForm"""
	userName = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name *'}))
	userEmail = forms.EmailField(required=False, label='Your e-mail address', widget=forms.TextInput(attrs={'placeholder': 'Your Email *'}))
	beerName = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Beer Name *'}))
	beerStyle = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Beer Style *'}))
	beerCompany = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Beer Company *'}))
	beerCountry = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Beer Country *'}))
	beerImage = forms.ImageField(required=False)
	beerDetails = forms.CharField(widget=forms.Textarea)

	def clean_details(self):
		beerDetail = self.cleaned_data['beerDetails']
		num_words = len(beerDetail.split())
		if num_words < 4 :
			raise forms.ValidationError("Not enough details for your Beer!")
		return beerDetail

class FilterForm(forms.Form):
    FILTER_CHOICES = (
        ('name', 'Beer Name'),
        ('style', 'Beer Style'),
        ('country', 'Beer Country'),
        ('company', 'Beer Company'),
    )

    filter_by = forms.ChoiceField(choices = FILTER_CHOICES)
    
# class FormQuestionSelect(forms.ModelForm):
#    # itemList = forms.ChoiceField(choices=[(items.id, items.name) for items in Item.objects.all()])

#     class Meta:
#         model = Item
#         fields = ('itemList', )
#         widgets = {
#             'itemList': Select(attrs={'class': 'select'}),
#         }

#     def __init__(self, questionsSet=None, **kwargs):
#         super(FormQuestionSelect, self).__init__(**kwargs)
#         if questionsSet:

            #Tested many code here to filter, None of them worked :(
            #Is that possible to create instanceList there ?         

# class BeerFilter_Check(django_filters.FilterSet):
# 	items = django_filters.ModelMultipleChoiceFilter(queryset=Item.objects.filter(created_date__lte=timezone.now())), widget=forms.CheckboxSelectMultiple)
# 	#name = django_filters.CharFilter(lookup_expr='icontains')
# 	#style = django_filters.CharFilter(lookup_expr='icontains')
# 	class Meta:
# 		model = Item
# 		fields = ['items']