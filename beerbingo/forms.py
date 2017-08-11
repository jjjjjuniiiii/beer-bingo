from django import forms
from .models import Item

# class searchObj(forms.ModelForm):
# 	"""docstring for searchObj"""
# 	class Meta:
#         model = Item 
#         fields = ('name', 'style',)
		
class ContactForm(forms.Form):
	"""docstring for ContactForm"""
	#userName = forms.CharField(max_length=100)
	userEmail = forms.EmailField(required=False, label='Your e-mail address')
	beerName = forms.CharField(max_length=100)
	beerStyle = forms.CharField()
	beerCompany = forms.CharField()
	beerCountry = forms.CharField()
	beerImage = forms.ImageField(required=False)
	beerDetails = forms.CharField(widget=forms.Textarea)

	def clean_details(self):
		beerDetail = self.cleaned_data['beerDetails']
		num_words = len(beerDetail.split())
		if num_words < 4 :
			raise forms.ValidationError("Not enough details for your Beer!")
		return beerDetail