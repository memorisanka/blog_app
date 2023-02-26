from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Article


class HomeViewTestCase(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class ArticleListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.article = Article.objects.create(title='Test Article', content='This is a test article', author=self.user)

    def test_article_list_view(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Test Article')


class ArticleDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.article = Article.objects.create(title='Test Article', content='This is a test article', author=self.user)

    def test_article_detail_view(self):
        response = self.client.get(reverse('article-detail', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article.html')
        self.assertContains(response, 'Test Article')


class ArticleCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_article_create_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('article-create'),
                                    {'title': 'Test Article', 'content': 'This is a test article'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(title='Test Article').exists())


class ArticleUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.article = Article.objects.create(title='Test Article', content='This is a test article', author=self.user)

    def test_article_update_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('article-update', args=[self.article.id]),
                                    {'title': 'Updated Article', 'content': 'This is an updated test article'})
        self.assertEqual(response.status_code, 302)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Article')


class ArticleDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.article = Article.objects.create(title='Test Article', content='This is a test article', author=self.user)

    def test_article_delete_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('article-delete', args=[self.article.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(title='Test Article').exists())
