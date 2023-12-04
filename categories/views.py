from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from tasks.mixins import AllauthLoginRequiredMixin
from .models import Category
from .mixins import UserCategoryQuerysetMixin
# Create your views here.


class CategoryListView(AllauthLoginRequiredMixin, UserCategoryQuerysetMixin, ListView):
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(AllauthLoginRequiredMixin, UserCategoryQuerysetMixin, DetailView):
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'


class CategoryCreateView(AllauthLoginRequiredMixin, CreateView):
    model = Category
    template_name = 'categories/category_create.html'
    fields = ['title', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(AllauthLoginRequiredMixin, UserCategoryQuerysetMixin, UpdateView):
    template_name = 'categories/category_update.html'
    fields = ['title', ]


class CategoryDeleteView(AllauthLoginRequiredMixin, UserCategoryQuerysetMixin, DeleteView):
    template_name = 'categories/category_delete.html'
    success_url = reverse_lazy('category-list')

