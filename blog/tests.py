from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from .models import Post


class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.post = Post.objects.create(
            title='A good title',
            body='Nice body content',
            author=self.user,
        )

    def test_string_representation(self): # Тест проверяет, что строковое представление содержимое поста верны
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self): # Тест проверяет работу метода get_absolute_url в модели
        self.assertEquals(self.post.get_absolute_url(), '/post/1/')

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Nice body content')

    def test_post_list_view(self):  # Тест проверяет, что
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200) # сайт возвращает код 200,
        self.assertContains(response, 'Nice body content') # содержит наш текст,
        self.assertTemplateUsed(response, 'home.html') # использует правильный шаблон

    def test_post_detail_view(self): # Тест проверяет, что
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)  # наша страница возвращат код 200
        self.assertEqual(no_response.status_code, 404) # неправильная страница возвращает код 404
        self.assertContains(response, 'A good title') # содержит соответствующий текст,
        self.assertTemplateUsed(response, 'post_detail.html') # использует соответствующий шаблон

    def test_post_create_view(self): # Тест проверяет создание представления
        response = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New text',
            'author': self.user,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')

    def test_post_update_view(self): # Тест проверяет обновление поста в блоге
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated title',
            'body': 'Updated text',
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self): # Тест проверяет удаление поста в блоге
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)