from django import template

from menu import utils

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, category):
    """
    Рендерит меню из элементов категории, переданной в качестве аргумента.
    """
    request = context.request

    items = utils.get_items(category)
    open_path = utils.get_open_path(request)

    # По заданию для отрисовки меню требуется не более одного запроса к БД.
    # Для выполнения условия формируем вспомогательные словари в функции ниже.
    parent_tree, child_parent, slug_path, root = utils.get_tree(items, request)
    open_slug = utils.get_open_slug(open_path, slug_path)
    root.url = utils.get_url(root, request)

    context = {
        'items': [root],
        'parent_tree': parent_tree,
    }

    # Если для запрошенного URL отсутствует пункт меню в БД, то на странице
    # отрендерится только корень, наследники будут свернуты. При обратной
    # ситуации ниже формируется список с раскрытыми пунктами меню.
    if open_slug is not None:
        open_items = utils.get_open_items(child_parent, open_slug, root)
        context['open_items'] = open_items

    return context


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_children(context, slug, parent_tree, open_items):
    items = parent_tree.get(slug)

    if items is not None:
        for item in items:
            item.url = utils.get_url(item, context.request)

    context = {
        'items': items,
        'parent_tree': parent_tree,
        'open_items': open_items,
    }

    return context
