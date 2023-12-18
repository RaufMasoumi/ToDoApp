from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.filters import SearchFilter, OrderingFilter
from tasks.mixins import AllauthLoginRequiredMixin, ViewSOFMixin
from tasks.forms import SearchForm, TaskOrderingForm, TASK_SEARCH_FIELDS, TaskModelForm
from tasks.filters import TaskFilterSet
from tasks.views import TaskUpdateView
from .models import Category
from .mixins import UserCategoryQuerysetMixin, DynamicCategoryTaskQuerysetMixin
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


class CategoryTaskCreateView(AllauthLoginRequiredMixin, DynamicCategoryTaskQuerysetMixin, CreateView):
    template_name = 'categories/category_task_create.html'
    form_class = TaskModelForm

    def get_success_url(self):
        return self.get_category().get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        task = self.object = form.save()
        task.categories.add(self.get_category())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class CategoryTaskUpdateView(TaskUpdateView):
    def get_success_url(self):
        try:
            category = self.request.user.categories.get(slug=self.kwargs.get('category', None))
        except Category.DoesNotExist:
            success_url = super().get_success_url()
        else:
            success_url = category.get_absolute_url()
        return success_url


class CategoryTaskDeleteView(AllauthLoginRequiredMixin, DynamicCategoryTaskQuerysetMixin, DeleteView):
    template_name = 'categories/category_task_delete.html'

    def get_success_url(self):
        return self.get_category().get_absolute_url()

    def form_valid(self, form=None):
        self.get_object().categories.remove(self.get_category())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context
