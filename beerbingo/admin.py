from django.contrib import admin

from .models import User
from .models import Item
from .models import Like
from .models import Flavor

admin.site.register(Item)