import uuid
from collections import defaultdict

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from .models import Toy, Cart, CartItem

from django.http import JsonResponse

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect
from .models import Purchase, CartItem

from .models import FAQ
from .faq_matcher import find_best_match
from collections import defaultdict
def index(request):
    # new_toy = Toy(name='Синий трактор', description='Плюшевая игрушка для детей из мультфильма "Синий трактор"', cost=700, image = '/main/img/игрушка 1.jpeg')
    # new_toy.save()
    #
    # new_toy = Toy(name='Дракон', description='Детская игрушка из пластика для развлечения', cost=500, image='/main/img/игрушка 2.jpeg')
    # new_toy.save()
    #
    # new_toy = Toy(name='Музыкальный сортер', description='Детская игрушка из мульфильма для развития ребенка', cost=1500, image='/main/img/игрушка 3.jpeg')
    # new_toy.save()
    #
    # #
    # new_toy = Toy(name='Подгузники Lovular', description='Подгузник для детей от 4-8 киллограмм',
    #               cost=1200, image='/main/img/подгузник4-8кг.jpeg')
    # new_toy.save()
    #
    # new_toy = Toy(name='Pampers active baby', description='Подгузники для детей от 11-16 киллограмм', cost=1500,
    #               image='/main/img/подгузник11-16кг.jpeg')
    # new_toy.save()
    #
    # new_toy = Toy(name='Pampers premium care', description='Подгузники для детей от 2-5 киллограмм',
    #               cost=1100, image='/main/img/подгузники2-5кг.jpeg')
    # new_toy.save()
    #
    # #
    # new_toy = Toy(name='Смесь PediaSure ', description='Смесь PediaSure Малоежка ваниль 850г с 12 месяцев',
    #               cost=1700, image='/main/img/Смесь PediaSure Малоежка ваниль 850г с 12месяцев.webp')
    # new_toy.save()
    #
    # # new_toy = Toy(name='Pampers active baby', description='Подгузники для детей от 11-16 киллограмм', cost=1600,
    # #               image='/main/img/подгузник11-16кг.jpeg')
    # new_toy.save()
    #
    # new_toy = Toy(name='Смесь NAN', description='Смесь NAN 2 Optipro 1050г с 6месяцев',
    #               cost=1309, image='/main/img/Смесь NAN 2 Optipro 1050г с 6месяцев.webp')
    # new_toy.save()

    #

    for faq in FAQ.objects.all():
        print(f"Вопрос: {faq.question}, Ответ: {faq.answer}, N-граммы: {faq.ngrams}")
    # all_toy = Toy.objects.all()
    # print(all_toy)

    # Toy.objects.get(id=2).delete()
    # Toy.objects.all().delete()

    # for i in all_toy:
    #     print(f'Название: {i.name}, Описание: {i.description}, Стоимость: {i.cost}, Картинка {i.image}')

    return render(request, 'main/main.html')

def kontakt(request):
    return render(request, 'main/kontakt.html')

def about(request):
    return render(request, 'main/about.html')

def products(request):
    all_toy = Toy.objects.all()  # Получаем все игрушки из БД
    context = {'all_toy': all_toy}  # Создаем словарь с данными для передачи в шаблон
    return render(request, 'main/products.html', context)

def profile(request):
    return render(request, 'main/profile.html')  # Создайте шаблон home.html

def login(request):
    return render(request, 'main/login.html')  # Создайте шаблон home.html

def registr(request):
    return render(request, 'main/registr.html')  # Создайте шаблон home.html

@login_required
def add_to_cart(request, toy_id):
    toy = get_object_or_404(Toy, id=toy_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, toy=toy)
    if not item_created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('products')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = sum(item.toy.cost * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'main/cart.html', context)


@login_required
def remove_from_cart(request, toy_id):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, toy_id=toy_id, cart=cart)
        item.delete()
    return redirect('cart')  # Замените 'cart' на URL вашей страницы корзины

# Создание API на стороне Django
def search_toys_by_description(request):
    query = request.GET.get('query', '').lower()
    if not query:
        return JsonResponse([])

    # Разбиваем запрос на слова
    query_words = query.split()

    # Создаем фильтр для поиска по всем словам в описании
    filters = Q()
    for word in query_words:
        filters |= Q(description__icontains=word)

    # Ищем товары, соответствующие запросу
    matching_toys = Toy.objects.filter(filters).distinct().values('name', 'description')
    return JsonResponse(list(matching_toys), safe=False)


def chatbot_response(request):
    if request.method == "POST":
        user_input = request.POST.get("message", "")
        bot_response = find_best_match(user_input)
        return JsonResponse({"response": bot_response})
    return JsonResponse({"error": "Invalid request"}, status=400)

def product_detail(request, pk):
    toy = get_object_or_404(Toy, pk=pk)
    return render(request, 'main/product_detail.html', {'toy': toy})


def shopping_cart(request):
    # Страница, отображающая товары после оплаты
    cart_items = request.session.get('cart_items', [])
    cart_total = request.session.get('cart_total', 0)
    return render(request, 'main/shopping_cart.html', {'cart_items': cart_items, 'cart_total': cart_total})


@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        # Получаем товары из сессии или корзины
        cart_items = request.session.get('cart_items', [])

        # Добавляем товары в Покупки
        for item in cart_items:
            toy_id = item.get('toy_id')
            quantity = item.get('quantity')

            # Создаем запись покупки
            Purchase.objects.create(toy_id=toy_id, quantity=quantity, user=request.user)

        # Очищаем корзину
        request.session['cart_items'] = []
        request.session['cart_total'] = 0

        # Перенаправляем на страницу "Спасибо за покупку"
        return redirect('success_page')

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('cart')  # Вернуться на страницу корзины, если корзина отсутствует

    cart_items = cart.items.all()

    if not cart_items.exists():
        return redirect('cart')  # Если корзина пуста, перенаправляем пользователя обратно

    # Создаем уникальный идентификатор заказа
    order_id = uuid.uuid4()
    print(f"Создание заказа {order_id} для пользователя {request.user.username}")

    for item in cart_items:
        print(f"Добавление товара {item.toy.name}, количество {item.quantity}")
        Purchase.objects.create(
            user=request.user,
            toy=item.toy,
            quantity=item.quantity,
            order_id=order_id
        )

    # Очищаем корзину
    cart_items.delete()

    return redirect('purchase_history')


@login_required
def purchase_history(request):
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchase_date')

    if not purchases.exists():
        return render(request, 'main/purchase_history.html', {'purchases': None})

    # Группируем покупки по идентификатору заказа
    grouped_purchases = defaultdict(list)
    for purchase in purchases:
        grouped_purchases[str(purchase.order_id)].append(purchase)

    # Преобразуем в обычный словарь, чтобы избежать проблем с .items в шаблоне
    grouped_purchases = dict(grouped_purchases)

    # Рассчитываем общую сумму для каждого заказа
    order_summaries = {}
    for order_id, items in grouped_purchases.items():
        total_sum = sum(item.quantity * item.toy.cost for item in items)
        order_summaries[order_id] = total_sum

    return render(request, 'main/purchase_history.html', {'purchases': grouped_purchases, 'order_summaries': order_summaries})



