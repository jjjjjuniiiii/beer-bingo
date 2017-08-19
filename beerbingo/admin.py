from django.contrib import admin
#from .filters import DropdownFilter

from .models import User
from .models import Item
from .models import Like
from .models import Flavor

admin.site.register(Item)
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Flavor)

class Media:
    js = ['/path/to/question_set_change.js',]

# class SearchAdmin (admin.ModelAdmin):
#     list_filter = (BeerFilterIndex,DropdownFilter)