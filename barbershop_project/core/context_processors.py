def navbar(request):
    menu_items = [
        {'title': 'О нас', 'anchor': '#about'},
        {'title': 'Услуги', 'anchor': '#services'},
        {'title': 'Мастера', 'anchor': '#masters'},
        {'title': 'Запись', 'anchor': '#booking'},
    ]
    return {'menu_items': menu_items}