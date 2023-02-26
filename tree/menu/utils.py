from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.conf import settings

from menu.models import Item


def remove_last_slash(url: str) -> str:
    """
    Возвращает URL без финального слеша.
    """
    if url.endswith('/'):
        return url[:-1]

    return url


def get_open_path(request: WSGIRequest) -> str:
    """
    Возвращает абсолютный URL запроса.
    """
    open_path = request.build_absolute_uri()

    return remove_last_slash(open_path)


def get_open_slug(open_path: str, slug_path: dict) -> str | None:
    """
    Возвращает slug элемента в зависимости от переданного URL, либо None при
    отсутствии совпадения.
    """
    return slug_path.get(open_path)


def get_url(item: Item, request: WSGIRequest) -> str:
    """
    Возвращает абсолютный URL из атрибутов элемента в БД.
    """
    if item.url.startswith('http'):
        return remove_last_slash(item.url)

    try:
        named_url = reverse(f'{item.url}')
    except NoReverseMatch:
        return item.url

    return remove_last_slash(request.build_absolute_uri(named_url))


def get_items_from_bd(category: str) -> QuerySet:
    """
    Возвращает все элементы модели Item с требуемой категорией из БД.
    """
    items = Item.objects.filter(category=category).select_related(
        'parent', 'category'
    )
    if not items:
        raise ObjectDoesNotExist(
            f'Меню с категорией {category} отсутствует в БД.'
        )

    return items


def get_items(category: str) -> QuerySet:
    """
    Возвращает все элементы модели Item с требуемой категорией.
    Если queryset присутствует в кеше, запросов к БД не будет.
    """
    key = f'items_{category}'
    items = cache.get(key)
    if items is None:
        items = get_items_from_bd(category)
        cache.set(key, items, settings.DEFAULT_CACHE_TIMEOUT)

    return items


def get_tree(
    items: QuerySet, request: WSGIRequest
) -> tuple[dict, dict, dict, Item]:
    """
    Из полученного queryset возвращает:
    словарь - {slug родителя: список элементов наследников},
    словарь - {slug наследника: элемент родителя},
    словарь - {url элемента: slug элемента},
    корневой элемент меню.
    """
    parent_children = {}
    child_parent = {}
    slug_path = {}

    for item in items:
        child_parent[item.slug] = item.parent
        slug_path[get_url(item, request)] = item.slug
        if item.parent is None:
            root = item
            items = items.exclude(id=root.id)
        elif item.parent.slug in parent_children:
            parent_children[item.parent.slug].append(item)
        else:
            parent_children[item.parent.slug] = [item]

    return parent_children, child_parent, slug_path, root


def get_open_items(parents: dict, open_slug: str, root: Item) -> list:
    """
    Возвращает список из slug элементов, необходимых для отрисовки на странице
    в виде раскрытых пунктов меню.
    """
    slugs = []
    slugs.append(open_slug)

    while True:
        item_slug = slugs[-1]
        parent = parents[item_slug]
        if parent is None:
            break
        slugs.append(parent.slug)

    return slugs
