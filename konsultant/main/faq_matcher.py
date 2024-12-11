import re
from .models import Toy, FAQ
from .text_processing import generate_ngrams
from django.shortcuts import reverse
from collections import Counter


def extract_weight_from_input(user_input):
    """
    Извлекает вес (число) из пользовательского запроса.
    Пример: "Подгузники для детей 13 килограмм" -> 13
    """
    match = re.search(r'(\d+)\s*к[и|и]?лограмм', user_input, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None  # Если вес не найден


def extract_range_from_description(description):
    """
    Извлекает диапазон веса из описания товара.
    Пример: "Подгузники для детей от 11-16 кг" -> (11, 16)
    """
    match = re.search(r'от\s*(\d+)-(\d+)\s*кг', description, re.IGNORECASE)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None  # Если диапазон не найден


def is_within_weight_range(weight, range_min, range_max):
    """
    Проверяет, попадает ли вес в диапазон.
    """
    return range_min <= weight <= range_max


def calculate_similarity(user_ngrams, candidate_ngrams):
    """Взвешенная функция расчета схожести"""
    weights = {'unigrams': 0.2, 'bigrams': 0.5, 'trigrams': 1.0}  # Вес триграмм выше
    similarity = 0

    for ngram_type, weight in weights.items():
        user_ngram_count = Counter(user_ngrams.get(ngram_type, []))
        candidate_ngram_count = Counter(candidate_ngrams.get(ngram_type, []))
        common = user_ngram_count & candidate_ngram_count
        similarity += sum(common.values()) * weight

    return similarity


def find_best_match(user_input):
    """
    Основная функция для поиска ответа на запрос.
    """

    # Генерируем n-граммы пользователя
    user_ngrams = {
        'unigrams': generate_ngrams(user_input, 1),
        'bigrams': generate_ngrams(user_input, 2),
        'trigrams': generate_ngrams(user_input, 3),
    }
    print(f"User ngrams: {user_ngrams}")

    faqs = FAQ.objects.all()
    best_match = None
    highest_similarity = 0

    # Обработка текстового совпадения
    for faq in faqs:
        similarity = calculate_similarity(user_ngrams, faq.ngrams)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = faq

    if highest_similarity > 0.2:  # Порог схожести
        return best_match.answer

    if "оператор" in user_input.lower():
        return "Для того, чтоб связаться с оператором, наберите по номеру телефона +7 (999) 123-45-67 или же отправьте ваш вопрос нам на почту: support@detmir.ru"

    if "подгузники" in user_input.lower():
        return "У нас есть подгузники Lovular, Pampers active baby, Pampers premium care"

    if "игрушки" in user_input.lower():
        return "У нас есть игрушки: Синий трактор, дракон и музыкальный сортер"

    if "смеси" in user_input.lower():
        return "У нас есть смесь PediaSure и смесь NAN"

    if "смесь" in user_input.lower():
        return "У нас есть смесь PediaSure и смесь NAN"

    if "памперсы" in user_input.lower():
        return "У нас есть подгузники Lovular, Pampers active baby, Pampers premium care"
    # Если ничего не найдено
    return "Для более точного ответа, пожалуйста, уточните свой вопрос!"


def find_best_match_with_link(user_input):
    """
    Функция для поиска ответа с ссылкой на товар.
    """
    from .faq_matcher import find_best_match

    answer = find_best_match(user_input)
    try:
        toy = Toy.objects.get(name=answer)
        toy_url = reverse('product_detail', args=[toy.id])
        return f"{toy.name}: {toy.description}. <a href='{toy_url}'>Посмотреть товар</a>"
    except Toy.DoesNotExist:
        return answer
