# import pytest
# from http import HTTPStatus

# from django.urls import reverse


# OK = HTTPStatus.OK


# # @pytest.mark.parametrize(
# #     argnames=('view_name', 'args',),
# #     argvalues=(
# #         ('news:home', None,),
# #         ('news:home', None,),
# #     ),
# # )
# # def test_route(client, view_name, args):
# # response = client.get(reverse(view_name, args=args))
# # assert response.status_code == OK

# # @pytest.mark.parametrize(
# #     argnames=('n', 'args'),
# #     argvalues=(
# #         (pytest.lazy_fixture('news_title'), None, ),
# #         (pytest.lazy_fixture('news_title'), 1, ),
# #     )
# # )
# # def test_news_title(n, args):
# #     print(n)
# #     assert True


# # def test_trial(news):
# #     print(news)
# #     assert True


# # def test_trial_a(author):
# #     print(author)
# #     assert True

# """
# test_routes — тесты доступности конкретных эндпоинтов, 
# проверка редиректов, кодов ответа, которые возвращают страницы, 
# тестирование доступа для авторизованных или анонимных пользователей.

# План тестирования:
#  1) Главная страница доступна анонимному пользователю.                           [Done!]
#  2) Страница отдельной новости доступна анонимному пользователю.                 [Done!]
#  3) Страницы удаления и редактирования комментария доступны автору комментария.  [Done!]
#  4) При попытке перейти на страницу редактирования или удаления комментария 
#     анонимный пользователь перенаправляется на страницу авторизации.
#  5) Авторизованный пользователь не может зайти на страницу редактирования        [Done!]
#     или удаления чужих комментариев (возвращается ошибка 404).
#  6) Страницы регистрации пользователей, входа в учётную запись и выхода из неё   [Done!]
#     доступны анонимным пользователям.
# """
# import os
# import json
# from http import HTTPStatus
# from pprint import pprint as pp

# from django.urls import reverse
# from django.test import Client, TestCase
# from django.contrib.auth import get_user_model

# from news.models import Comment, News


# User = get_user_model()


# class TestRoutes(TestCase):

#     STATUS_OK = HTTPStatus.OK

#     @classmethod
#     def setUpTestData(cls):
#         with open('news/tests/fixtures/fixtures_for_tests.json', encoding='utf-8') as f_json:
#             fixture_data = json.load(f_json)
#         cls.many_news = cls.insert_data(News, fixture_data['news_data'])
#         cls.news = News.objects.create(
#             title='Вековая мудрость выдающегося мыслителя',
#             text='Да, сегодня я пьян, но завтра протрезвею. А кто-то навсегда останется педиком.'
#         )
#         cls.author = User.objects.create(username='Кама Пуля')
#         cls.reader = User.objects.create(username='Мага Лезгин')
#         # cls.auth_client = Client()
#         # cls.auth_client.force_login(cls.user)
#         cls.comment = Comment.objects.create(
#             news=cls.news,
#             author=cls.author,
#             text='some comment',
#         )

#     @staticmethod
#     def insert_data(klass, data):
#         model_instance_list = list(map(lambda item: klass(**item), data))
#         return klass.objects.bulk_create(model_instance_list)

#     def test_page_availability(self):
#         """Тест главной страницы"""
#         # arrange
#         urls = [
#             ('news:home', None,),
#             ('news:detail', (self.news.pk,),),
#             ('users:login', None,),
#             ('users:logout', None,),
#             ('users:signup', None,),
#         ]
#         for name, args in urls:
#             with self.subTest(name=name):
#                 # act
#                 response = self.client.get(reverse(name, args=args))
#                 # assert
#                 self.assertEqual(
#                     response.status_code,
#                     self.STATUS_OK,
#                     # HTTPStatus.FORBIDDEN,
#                     msg=f'Получили статус код {response.status_code}, Ожидаемый статус код 200'
#                 )

#     def test_availability_for_comment_edit_and_delete(self):
#         """Тест страницы удаления и редактирования комментария доступны автору комментария"""
#         user_status = (
#             # Здесь author и reader - экземпляры User которые мы создали в setUpTestData
#             (self.author, self.STATUS_OK,),
#             (self.reader, HTTPStatus.NOT_FOUND,),
#             # неправильные данные для примера провала теста
#             # (self.author, HTTPStatus.NOT_FOUND,),  # предполагаемый баг во view
#             # (self.reader, self.STATUS_OK,),  # предполагаемый баг во view
#         )
#         for user, status_code in user_status:
#             # авторизация клиента и дальше запрос делаем через self.client
#             # пароль при авторищации через force_login не нужен,
#             # я так понимаю, эта функция просто создаёт сессионный ключ
#             # для http-клиента, и делает этим клиентом разных юзеров
#             self.client.force_login(user)
#             for view_name in ('news:delete', 'news:edit',):
#                 with self.subTest(user=user, view_name=view_name):
#                     url = reverse(view_name, args=(self.comment.pk,))
#                     # делаем запрос через http-клиент от django.test
#                     # обрати внимание, что клиент мы не переопределяем
#                     response = self.client.get(url)
#                     self.assertEqual(response.status_code, status_code)

#     def test_redirect_for_anonymous_client(self):
#         """
#         При попытке перейти на страницу редактирования или удаления комментария 
#         анонимный пользователь перенаправляется на страницу авторизации.
#         """
#         # arrange
#         login_url = reverse('users:login')
#         for view_name in ('news:delete', 'news:edit'):
#             url = reverse(view_name, args=(self.comment.pk,))
#             redirect_url = f'{login_url}?next={url}'
#             with self.subTest(view_name=view_name):
#                 # act
#                 # проверяем неавторизованного пользователя
#                 response = self.client.get(url)
#                 # assert
#                 # должен сделать редирект на expected_url,
#                 # т.е. статус код у response должен быть 302
#                 self.assertRedirects(
#                     response=response,
#                     expected_url=redirect_url,
#                     # expected_url=url,
#                 )
