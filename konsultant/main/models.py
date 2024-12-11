from django.contrib.auth.models import User
from django.db import models
from .text_processing import generate_ngrams
import uuid

class Toy(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=250, blank=False)
    cost = models.IntegerField(default=0)
    image = models.ImageField(upload_to='main/img/', blank=True, null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Корзина пользователя {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}  (x{self.toy.name})"


class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    ngrams = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        # Генерация N-грамм для вопроса перед сохранением
        self.ngrams = {
            'unigrams': generate_ngrams(self.question, 1),
            'bigrams': generate_ngrams(self.question, 2),
            'trigrams': generate_ngrams(self.question, 3),
        }
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Заказ {self.order_id}: {self.toy.name} x{self.quantity} для {self.user.username}"
