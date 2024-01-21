# """
# Залогиненный пользователь может создать заметку, а анонимный — не может.
# Невозможно создать две заметки с одинаковым slug.
# Если при создании заметки не заполнен slug, то он формируется автоматически, с помощью функции pytils.translit.slugify.
# Пользователь может редактировать и удалять свои заметки, но не может редактировать или удалять чужие.
# """
# import pytest
# from http import HTTPStatus
# from pytils.translit import slugify
# from pytest_django.asserts import assertRedirects, assertFormError

# from django.urls import reverse

# from notes.models import Note
# from notes.forms import WARNING


# def test_user_can_create_note(author, author_client, form_data):
#     """
#     Проверка, что зарегистрированный пользователь может создать заметку,
#     его средиректит на страницу 'success'
#     и все поля заметки что он создаст - правильные
#     """
#     # arrange
#     success_url = reverse('notes:success')
#     create_note_url = reverse('notes:add')
#     # action
#     response = author_client.post(create_note_url, data=form_data)
#     note = Note.objects.get()
#     # assertion
#     assertRedirects(response, success_url)  # успешный редирект
#     assert Note.objects.count() == 1  # должен создаться 1 объект
#     # все поля объекта правильные
#     assert note.title == form_data['title']  # + 'asds'
#     assert note.text == form_data['text']
#     assert note.slug == form_data['slug']
#     assert note.author == author


# # ? ----- декоратор @pytest.mark.django_db -----


# # Добавляем маркер, который обеспечит доступ к базе данных т.к. фикстуры к db мы сдесь не используем
# @pytest.mark.django_db
# def test_anonymous_user_cant_create_note(client, form_data):
#     """
#     Проверка, что анонимный пользователь не может создать заметку,
#     его средиректит на страницу логина
#     """
#     # arrange
#     login_url = reverse('users:login')
#     create_note_url = reverse('notes:add')
#     expected_url = f'{login_url}?next={create_note_url}'
#     # action
#     response = client.post(create_note_url, data=form_data)
#     # assertion
#     assertRedirects(response, expected_url)
#     assert Note.objects.count() == 0  # заметка не создалась

# # ? ----- проверка формы с помощью assertFormError -----


# def test_not_unique_slug(author_client, note, form_data):
#     """Тест на то, что нельзя создать одинаковый слаг"""
#     # arrange
#     create_note_url = reverse('notes:add')
#     form_data['slug'] = note.slug
#     # action
#     response = author_client.post(create_note_url, data=form_data)
#     # assertion
#     assertFormError(
#         response=response,
#         form='form',
#         field='slug',
#         errors=note.slug + WARNING
#     )
#     assert Note.objects.count() == 1


# def test_empty_slug(author_client, form_data):
#     """Тест на то, что слаг может создаться автоматически и он правильный"""
#     # arrange
#     create_note_url = reverse('notes:add')
#     expected_url = reverse('notes:success')
#     # form_data.pop('slug')
#     del form_data['slug']
#     # action
#     response = author_client.post(create_note_url, form_data)
#     note = Note.objects.get()
#     expexted_slug = slugify(note.title)
#     # assertion
#     assertRedirects(response, expected_url)
#     assert Note.objects.count() == 1
#     assert note.slug == expexted_slug


# def test_author_can_edit_note(author_client, form_data, note):
#     """Тест успешного обновления заметки её автором."""
#     # arrange
#     edit_url = reverse('notes:success')
#     update_note_url = reverse('notes:edit', args=(note.slug,))
#     # action
#     response = author_client.post(update_note_url, data=form_data)
#     note.refresh_from_db()  # callable object - запомни это
#     # assertion
#     assertRedirects(response, edit_url)
#     assert note.title == form_data['title']
#     assert note.text == form_data['text']
#     assert note.slug == form_data['slug']


# def test_other_user_cant_edit_note(admin_client, form_data, note):
#     """Тест невозможности обновления заметки не её автором."""
#     # arrange
#     edit_url = reverse('notes:edit', args=(note.slug,))
#     # action
#     response = admin_client.post(edit_url, data=form_data)
#     note_from_db = Note.objects.get(pk=note.pk)
#     # assertion
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert note.title == note_from_db.title
#     assert note.text == note_from_db.text
#     assert note.slug == note_from_db.slug


# def test_author_can_delete_note(author_client, note,):
#     """Тест, что автор может удалить свою заметку."""
#     # arrange
#     expected_url = reverse('notes:success')
#     delete_url = reverse('notes:delete', args=(note.slug,))
#     # action
#     response = author_client.post(delete_url)
#     # assertion
#     assertRedirects(response, expected_url)
#     assert Note.objects.count() == 0


# def test_other_user_cant_delete_note(admin_client, note,):
#     """Тест, что не автор заметки не может её удалить."""
#     # arrange
#     delete_url = reverse('notes:delete', args=(note.slug,))
#     # action
#     response = admin_client.post(delete_url)
#     # asserion
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert Note.objects.count() == 1