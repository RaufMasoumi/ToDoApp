from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.filters import SearchFilter, OrderingFilter
from tasks.mixins import AllauthLoginRequiredMixin
from tasks.mixins import ViewSOFMixin
from tasks.forms import SearchForm, TaskOrderingForm, TASK_SEARCH_FIELDS
from tasks.filters import TaskFilterSet
from .models import Category
from .mixins import UserCategoryQuerysetMixin
from .forms import CategoryModelForm, CategoryOrderingForm, CATEGORY_SEARCH_FIELDS
from .filters import CategoryFilterSet
# Create your views here.


class CategoryListView(AllauthLoginRequiredMixin, UserCategoryQuerysetMixin, ViewSOFMixin, ListView):
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'
    search_form = SearchForm
    search_filter_class = SearchFilter
    search_fields = CATEGORY_SEARCH_FIELDS
    ordering_form = CategoryOrderingForm
    ordering_filter_class = OrderingFilter
    ordering_fields = ordering_form.ordering_fields
    filterset_class = CategoryFilterSet


class CategoryDetailView(AllauthLoginRequiredMixin, UserCategoryQuerysetMixin, ViewSOFMixin, DetailView):
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'
    search_form = SearchForm
    search_filter_class = SearchFilter
    search_fields = TASK_SEARCH_FIELDS
    ordering_form = TaskOrderingForm
    ordering_filter_class = OrderingFilter
    ordering_fields = ordering_form.ordering_fields
    filterset_class = TaskFilterSet

    def get_filter_queryset(self):
        return self.get_object().tasks.all()


class CategoryCreateView(AllauthLoginRequiredMixin, CreateView):
    model = Category
    template_name = 'categories/category_create.html'
    form_class = CategoryModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['instance_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(AllauthLoginRequiredMixin, UserCategoryQuerysetMixin, UpdateView):
    template_name = 'categories/category_update.html'
    form_class = CategoryModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class CategoryDeleteView(AllauthLoginRequiredMixin, UserCategoryQuerysetMixin, DeleteView):
    template_name = 'categories/category_delete.html'
    success_url = reverse_lazy('category-list')

