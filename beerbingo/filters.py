from .models import Item
import django_filters
from django.contrib.admin.filters import AllValuesFieldListFilter
from django import forms
#from multiSelectField import multiSelectField

class BeerFilter(django_filters.FilterSet):
	# groups = django_filters.ModelMultipleChoiceFilter(queryset=Item.objects.all(),
 #        widget=forms.CheckboxSelectMultiple)
	name = django_filters.CharFilter(lookup_expr='icontains')
	style = django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = Item
		fields = ['name', 'style', 'company', 'country','rate',]

# class BeerFilterIndex(SimpleListFilter):
# 	# items = django_filters.ModelMultipleChoiceFilter(queryset=Item.objects.all().values('name','style','country','company'), widget=forms.CheckboxSelectMultiple)
# 	# #name = django_filters.CharFilter(lookup_expr='icontains')
# 	# #style = django_filters.CharFilter(lookup_expr='icontains')
# 	# class Meta:
# 	# 	model = Item
# 	# 	fields = ['items',]
# 	 category = _('Itemid')
	 
#      parameter_name ='name'

#      contlist = list(Item.objects.all())

#       def lookups(self, request, model_admin):
#          lst = []
#          for id in self.contlist:
#              lst.append((id.name,id.name))
#          return tuple(lst)

#      def queryset(self, request, queryset):
#          if self.value() is None:
#              return queryset
#          return queryset.filter(name__exact=self.value())

# class DropdownFilter(AllValuesFieldListFilter):
#      template = 'admin/dropdown_filter.html' 
