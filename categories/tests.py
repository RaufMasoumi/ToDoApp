from django.urls import reverse_lazy
from tasks.test_mixins import GenericViewsTestCase
from .models import Category


class CategoryTests(GenericViewsTestCase):

    def setUp(self):
        super().setUp()
        self.category1 = Category.objects.create(
            user=self.user,
            title='testcategory1'
        )
        self.category2 = Category.objects.create(
            user=self.user,
            title='testcategory2'
        )
        self.content = [self.category1.title, self.category2.title]
        self.detail_content = [self.category1.title, ]
        self.detail_not_contain_content = [self.category2.title, ]
        self.update_content = ['Update', self.category1.title, ]
        self.update_not_contain_content = ['Create', self.category2.title]
        self.delete_content = ['Delete', self.category1.title, ]

    def test_category_model(self):
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.first(), self.category1)
        self.assertEqual(Category.objects.first().title, 'testcategory1')

    def test_category_slug_auto_creation(self):
        self.assertEqual(self.category1.slug, 'testcategory1')

    @GenericViewsTestCase.list_view_test(
        path='category-list', content='content', context_name='categories', object_list_count=2,
        template_name='categories/category_list.html', bad_user_not_contain_content='content'
    )
    def test_category_list_view(self, path, response, content):
        pass

    @GenericViewsTestCase.detail_view_test(
        path='category-detail', lookup_fields=['slug', ], content='detail_content', template_name='categories/category_detail.html',
        object_name='category1', not_contain_content='detail_not_contain_content'
    )
    def test_category_detail_view(self, path, response, content, obj):
        pass

    @GenericViewsTestCase.create_view_test(
        path='category-create', content=['Create', ], template_name='categories/category_create.html', model=Category,
        data={'title': 'newcategory'}, not_contain_content=['Update', ]
    )
    def test_category_create_view(self, path, data, get_response, post_response, created_obj, success_url):
        pass

    @GenericViewsTestCase.update_view_test(
        object_name='category1', path='category-update', lookup_fields=['slug', ], content='update_content',
        template_name='categories/category_update.html',  data={'title': 'updated'}, not_contain_content='update_not_contain_content',
    )
    def test_category_update_view(self, path, data, get_response, post_response, updated_obj, success_url):
        pass

    @GenericViewsTestCase.delete_view_test(
        object_name='category1', path='category-delete', lookup_fields=['slug', ], content='delete_content',
        template_name='categories/category_delete.html', not_contain_content=['Update', 'Create', ],
        success_url=reverse_lazy('category-list')
    )
    def test_category_delete_view(self, path, get_response, post_response, deleted_obj, success_url):
        pass
