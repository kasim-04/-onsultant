from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    return value * arg

@register.filter
def sum_total(order_items):
    return sum(item.quantity * item.toy.cost for item in order_items)

@register.filter
def get_item(dictionary, key):
    """Извлекает элемент из словаря по ключу."""
    return dictionary.get(str(key))  # Преобразуем ключ в строку, чтобы избежать проблем с типами данных
