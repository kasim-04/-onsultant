from django.core.management.base import BaseCommand
# from .models import FAQ
# from .utils import generate_ngrams
from main.models import FAQ
from main.utils import generate_ngrams


class Command(BaseCommand):
    help = "Обновляет N-граммы для FAQ"

    def handle(self, *args, **kwargs):
        faqs = FAQ.objects.all()
        for faq in faqs:
            faq.ngrams = {
                'unigrams': generate_ngrams(faq.question, 1),
                'bigrams': generate_ngrams(faq.question, 2),
                'trigrams': generate_ngrams(faq.question, 3),
            }
            faq.save()
        self.stdout.write(self.style.SUCCESS("N-граммы для FAQ успешно обновлены"))

