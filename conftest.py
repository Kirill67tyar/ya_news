import pytest

from news.models import News, Comment


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):
    """фикстура создания автора заметки."""
    return django_user_model.objects.create(username='Кама Пуля')


@pytest.fixture
def author_client(client, author):  # Вызываем фикстуру автора и клиента.
    """фикстура логина автора заметки."""
    client.force_login(author)
    return client


@pytest.fixture
@pytest.mark.django_db
def news():
    """фикстура создания заметки."""
    return News.objects.create(
        title='Заголовок к статье № 1',
        text='Текст к статье № 1',
    )


@pytest.fixture
def comment(author, news):
    """фикстура создания заметки."""
    return Comment.objects.create(
        text='Коммент к статье № 1',
        author=author,
        news=news,
    )


@pytest.fixture
def id_for_url(news):
    return (news.pk,)

# @pytest.fixture
# # # Фикстура запрашивает другую фикстуру создания заметки.
# def slug_for_args(note: Note) -> tuple[str]:
#     return (note.slug,)


# @pytest.fixture
# # фикстура для формы создания заметки
# def form_data():
#     return {
#         'title': 'Новый заголовок',
#         'text': 'Новый текст',
#         'slug': 'new-slug',
#     }
