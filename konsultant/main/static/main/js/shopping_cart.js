<script>
document.getElementById('checkout-btn').addEventListener('click', function() {
    fetch("{% url 'checkout_cart' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: JSON.stringify({
            cart_items: {{ cart_items|safe }},
            cart_total: {{ cart_total }},
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = "{% url 'shopping_cart' %}"; // Переход на страницу shopping_cart
        } else {
            alert('Ошибка при оформлении заказа');
        }
    });
});
</script>