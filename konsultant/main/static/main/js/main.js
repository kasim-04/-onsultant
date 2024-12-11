function openChat() {
    const chatMessages = document.getElementById("chatMessages");

    // Открыть окно чата
    document.getElementById("chatWindow").style.display = "block";

    // Добавить приветственное сообщение от бота, если окно пустое
    if (chatMessages.children.length === 0) {
        const botMessage = document.createElement("div");
        botMessage.classList.add("bot-message");
        botMessage.innerHTML = "<p>Здравствуйте! Чем могу помочь?</p>";
        chatMessages.appendChild(botMessage);
    }
}

function closeChat() {
    document.getElementById("chatWindow").style.display = "none";
}

function sendMessage() {
    const userInput = document.getElementById("userInput");
    const chatMessages = document.getElementById("chatMessages");

    if (userInput.value.trim() !== "") {
        // Добавляем сообщение от пользователя
        const userMessage = document.createElement("div");
        userMessage.classList.add("user-message");
        userMessage.innerHTML = `<p>${userInput.value}</p>`;  // Исправлено
        chatMessages.appendChild(userMessage);

        // Ответ бота на основе анализа сообщения пользователя
        const botReply = generateBotResponse(userInput.value);
        const botMessage = document.createElement("div");
        botMessage.classList.add("bot-message");
        botMessage.innerHTML = `<p>${botReply}</p>`;  // Исправлено
        chatMessages.appendChild(botMessage);

        // Очистка поля ввода и прокрутка вниз
        userInput.value = "";
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

//function generateBotResponse(userText) {
//    if (userText.toLowerCase().includes("игрушки до")) {
//        const priceMatch = userText.match(/\d+/);
//        if (priceMatch) {
//            const price = parseInt(priceMatch[0], 10);
//            return `Секунду, ищу игрушки до ${price} рублей...`;
//        }
//    }
//    return "Я здесь, чтобы помочь!";
//}



//Бот печатает
//function sendMessage() {
//    // Показать индикатор "Бот печатает..."
//    const typingIndicator = document.createElement("div");
//    typingIndicator.classList.add("bot-message");
//    typingIndicator.innerHTML = "<p>Бот печатает...</p>";
//    chatMessages.appendChild(typingIndicator);
//
//    // Задержка для имитации ответа бота
//    setTimeout(() => {
//        typingIndicator.remove();
//        const botReply = generateBotResponse(userInput.value);
//        // (остальной код остается)
//    }, 1000);
//}


//Обработка данных по описанию
async function searchToys(userQuery) {
    console.log(`Отправка запроса: /api/search/?query=${encodeURIComponent(userQuery)}`); // Новый лог
    try {
        const response = await fetch(`/api/search/?query=${encodeURIComponent(userQuery)}`);
        if (!response.ok) {
            return "Произошла ошибка при поиске. Пожалуйста, попробуйте снова.";
        }
        const toys = await response.json();
        console.log("Получены данные:", toys); // Новый лог
        if (toys.length > 0) {
            return toys.map(toy => `${toy.name}: ${toy.description}`).join('<br>');
        } else {
            return "К сожалению, ничего не найдено.";
        }
    } catch (error) {
        console.error("Ошибка при поиске:", error);
        return "Произошла ошибка при обработке вашего запроса.";
    }
}




async function sendMessage() {
    const userInput = document.getElementById("userInput");
    const chatMessages = document.getElementById("chatMessages");

    if (userInput.value.trim() !== "") {
        // Добавляем сообщение от пользователя
        const userMessage = document.createElement("div");
        userMessage.classList.add("user-message");
        userMessage.innerHTML = `<p>${userInput.value}</p>`;
        chatMessages.appendChild(userMessage);

        // Получаем ответ бота (ожидаем его)
        const botReply = await generateBotResponse(userInput.value); // Ожидание ответа
        const botMessage = document.createElement("div");
        botMessage.classList.add("bot-message");
        botMessage.innerHTML = `<p>${botReply}</p>`;
        chatMessages.appendChild(botMessage);

        // Очистка поля ввода и прокрутка вниз
        userInput.value = "";
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

async function generateBotResponse(userText) {
    console.log("Введённый текст:", userText);

    // Проверяем, хочет ли пользователь увидеть товары
    const keywords = ["покажи", "найди", "выведи", "товар", "товары"];
    const lowerCaseText = userText.toLowerCase();

    // Если в тексте есть ключевые слова, запускаем поиск
    if (keywords.some(keyword => lowerCaseText.includes(keyword))) {
        const searchResult = await searchToys(userText);
        console.log("Результат поиска:", searchResult);

        // Если результат есть, возвращаем его
        if (searchResult && searchResult.length > 0) {
            return `Найдено:\n${searchResult}`;
        } else {
            return "К сожалению, ничего не найдено.";
        }
    }

    // Если ключевых слов нет, стандартный ответ
    return "Я здесь, чтобы помочь!";
}

//МЛ
async function sendMessage() {
    const userInput = document.getElementById("userInput");
    const chatMessages = document.getElementById("chatMessages");

    if (userInput.value.trim() !== "") {
        // Добавляем сообщение пользователя в чат
        const userMessage = document.createElement("div");
        userMessage.classList.add("user-message");
        userMessage.innerHTML = `<p>${userInput.value}</p>`;
        chatMessages.appendChild(userMessage);

        // Отправляем запрос на сервер
        try {
            const response = await fetch(`/api/ml_search/?query=${encodeURIComponent(userInput.value)}`);
            const data = await response.json();

            // Добавляем ответ бота
            const botMessage = document.createElement("div");
            botMessage.classList.add("bot-message");

            if (data.error) {
                botMessage.innerHTML = `<p>${data.error}</p>`;
            } else {
                botMessage.innerHTML = `<p>Лучший товар: ${data.match} (Сходство: ${(data.similarity * 100).toFixed(2)}%)</p>`;
            }

            chatMessages.appendChild(botMessage);
        } catch (error) {
            const botMessage = document.createElement("div");
            botMessage.classList.add("bot-message");
            botMessage.innerHTML = `<p>Произошла ошибка. Попробуйте снова.</p>`;
            chatMessages.appendChild(botMessage);
        }

        // Прокрутка вниз и очистка поля ввода
        userInput.value = "";
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

//новая

function sendMessage() {
    const userInput = document.getElementById("userInput");
    const chatMessages = document.getElementById("chatMessages");

    if (userInput.value.trim() !== "") {
        // Добавляем сообщение от пользователя
        const userMessage = document.createElement("div");
        userMessage.classList.add("user-message");
        userMessage.innerHTML = `<p>${userInput.value}</p>`;
        chatMessages.appendChild(userMessage);

        // Отправляем запрос на сервер
        fetch("/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken() // Получаем CSRF токен
            },
            body: `message=${encodeURIComponent(userInput.value)}`
        })
        .then(response => response.json())
        .then(data => {
            const botMessage = document.createElement("div");
            botMessage.classList.add("bot-message");
            botMessage.innerHTML = `<p>${data.response}</p>`;
            chatMessages.appendChild(botMessage);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });

        userInput.value = "";
    }
}

// Функция для получения CSRF токена
function getCSRFToken() {
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
        const [name, value] = cookie.split("=");
        if (name === "csrftoken") {
            return value;
        }
    }
    return "";
}