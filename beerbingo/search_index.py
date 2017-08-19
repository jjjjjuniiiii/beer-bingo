import datetime
from haystack import indexes
from haystack.query import EmptySearchQuerySet
from .models import Item
from .models import *


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    
    text = indexes.CharField(document=True, use_template=True)
    author1 = indexes.EdgeNgramField(model_attr='name')
    author2 = indexes.EdgeNgramField(model_attr='sytle')
    author3 = indexes.EdgeNgramField(model_attr='country')
    author4 = indexes.EdgeNgramField(model_attr='company')
    author5 = indexes.EdgeNgramField(model_attr='img_url')

    def get_model(self):
        return Item

        def index_queryset(self, using=None):
            """Used when the entire index for model is updated."""
            return self.get_model().objects.all()