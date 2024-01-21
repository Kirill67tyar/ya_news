from django.urls import reverse
import pytest
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone

from news.models import News, Comment


@pytest.fixture
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


@pytest.fixture
@pytest.mark.django_db
def many_news():
    today = datetime.today()
    return News.objects.bulk_create(News(
        title=f'Заголовок № {i}',
        text=f'Текст к статье № {i}',
        date=today - timedelta(days=i),
    ) for i in range(1, settings.NEWS_COUNT_ON_HOME_PAGE + 2))


@pytest.fixture
@pytest.mark.django_db
def comments_with_other_dates(news, author):
    now = timezone.now()
    for i in range(1, 3):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст к комментарию № {i}?',
        )
    comment.created = now + timedelta(days=i)
    comment.save()


@pytest.fixture
def detail_url(news):
    return reverse(
        'news:detail',
        kwargs={'pk': news.pk, }
    )


@pytest.fixture
def delete_url(comment):
    return reverse(
        'news:delete',
        kwargs={'pk': comment.pk, }
    )


@pytest.fixture
def update_url(comment):
    return reverse(
        'news:edit',
        kwargs={'pk': comment.pk, }
    )


@pytest.fixture
def form_data():
    return {
        'text': 'Комментарий 1'
    }


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
