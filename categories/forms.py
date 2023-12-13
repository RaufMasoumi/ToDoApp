from django import forms
from tasklists.mixins import FormTitleValidationMixin
from tasks.forms import get_ordering_choices
from .models import Category

CATEGORY_SEARCH_FIELDS = ['title', ]
CATEGORY_ORDERING_FIELDS = ['title', 'created_at', 'updated_at']


class CategoryModelForm(FormTitleValidationMixin, forms.ModelForm):
    reverse_relation = 'categories'

    class Meta:
        model = Category
        fields = ('title', )


class CategoryOrderingForm(forms.Form):
    ordering_fields = CATEGORY_ORDERING_FIELDS
    ORDERING_CHOICES = get_ordering_choices(ordering_fields)
    ordering = forms.ChoiceField(choices=ORDERING_CHOICES, required=False)
