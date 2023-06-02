from django_filters import FilterSet, DateFilter, CharFilter
from .models import Post
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class PostFilter(FilterSet):
    author = CharFilter(
        label="Author's Username",
        field_name='author__user__username',
        lookup_expr="icontains"
    )
    publication_date = DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        label="Published earlier than",
        field_name='publication_date',
        lookup_expr="lt"
    )

    class Meta:
       model = Post
       fields = {
           'title': ['icontains'],
       }