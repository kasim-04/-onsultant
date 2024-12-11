from locust import HttpUser, task, between


class ChatUser(HttpUser):
    wait_time = between(1, 2)  # Интервал между запросами

    @task
    def open_chat(self):
        # Открытие чата
        self.client.get("/")

    @task
    def send_message(self):
        # Отправка сообщения в чат
        self.client.post("/send_message/", json={"message": "Посоветуй детскую игрушку для развития ребенка из популярных мультфильмов"})