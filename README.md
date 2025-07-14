<div align="center">
 
<img src="assets/box.png" alt="GiftShop" width="100"/>

# GiftShop

</div>

## Описание

### Интернет-магазин сувениров "GiftShop"

### Технологии

1. **Django `v5` + Django Templates**: Multi-Page Application
2. **Celery**: Распределенная асинхронная **очередь задач**
3. **RabbitMQ**: Брокер сообщений
4. **Redis**: Хранение задач **Celery** + **Кеш**
5. **Flower**: Мониторинг и управление задачами в **Celery**
6. **Postgresql**: База Данных
7. **TailwindCSS**: CSS-фреймворк, упрощающий стилизацию HTML и **адаптивный дизайн**

### Функционал

**Пользователи**: могут просматривать товары, добавлять их в корзину и совершать покупки, размещая заказы. Доступна регистрация и вход в профиль, активация купонов, просмотр истории заказов, отправка сообщений обратной связи.

**Администраторы**: могут полностью управлять основным функционалом магазина: его содержимым (товары, категории товаров, скидочные купоны), а также заказами пользователей. Могут выгружать заказы в CSV-формате, просматривать сообщения обратной связи.

<details>

<summary>Страницы</summary>

#### Страницы

**shop:**

- [x] Списки товаров
  - [x] Главная страница, со всеми товарами `giftshop.com/`
  - [x] Товары по категориям `giftshop.com/category/kopilki/`
- [x] Просмотр карточки товара `giftshop.com/1/kopilka-xxl-gold/`

**cart** и **coupons:**

- [x] Просмотр корзины `giftshop.com/cart/`
  - [x] Активация купона на скидку `giftshop.com/coupons/apply/`
- [x] Добавление товара в корзину `giftshop.com/cart/add/<id>/`
- [x] Удаление товара из корзины `giftshop.com/cart/remove/<id>/`

**orders:**

- [x] Оформление заказа `giftshop.com/orders/create/`
- [x] Просмотр истории заказов `giftshop.com/orders/`

**account:**

- [x] Вход/выход из профиля `giftshop.com/account` `/login/` | `/logout/`
- [x] Регистрация пользователя `giftshop.com/account/register/`

**info:**

- [x] Информационная страница `giftshop.com/info/`
- [x] Форма обратной связи

</details>

<details>

<summary>Admin-панель</summary>

#### Admin-панель

- Управление товарами и категориями товаров
- Управление купонами на скидку
- Просмотр и управление заказами, выгрузка заказов в CSV
- Просмотр сообщений обратной связи
- Управление пользовательскими профилями

</details>

## Установка

1. Настроить `.env` (в соответствии с `.env.example`)
2. Настроить веб-сервер **Angie**:
   - Конфигурация `angie/angie.conf`
   - Серверы в `angie/http.d/`, например `default.conf`

По умолчанию **Angie** сконфигурирован на прослушивание `:80` порта **со всеми server_name's**.

```bash
# Запуск проекта
docker compose -f docker-compose.prod.yaml up -d

# Добавление Django Superuser: Admin-аккаунт
docker compose run web python manage.py createsuperuser
```

## Галерея

<div class="carousel-container">
    <div class="carousel-images">
        <img class="carousel-image" src="assets/pages/image-1.png" alt="Image 1">
        <img class="carousel-image" src="assets/pages/image-2.png" alt="Image 2">
        <img class="carousel-image" src="assets/pages/image-3.png" alt="Image 3">
        <img class="carousel-image" src="assets/pages/image-1.png" alt="Image 1">
        <img class="carousel-image" src="assets/pages/image-2.png" alt="Image 2">
        <img class="carousel-image" src="assets/pages/image-3.png" alt="Image 3">
        </div>
</div>

<style>
/* Базовые стили для контейнера карусели */
.carousel-container {
    position: relative;
    width: 100%;
    max-width: 600px; /* Регулируйте по необходимости */
    margin: 20px auto;
    overflow: hidden; /* Скрывает выходящие за пределы изображения */
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Контейнер изображений, который будет прокручиваться */
.carousel-images {
    display: flex;
    /* Убедитесь, что ширина контейнера больше, чем у одного изображения, чтобы анимация имела место */
    width: fit-content; /* Позволяет содержимому определять ширину */
    animation: autoScroll 15s linear infinite; /* 15s - длительность, infinite - бесконечно */
}

/* Изображения внутри карусели */
.carousel-image {
    width: 600px; /* Ширина одного изображения, должна совпадать с max-width контейнера */
    height: auto; /* Сохраняет пропорции */
    object-fit: cover;
    border-radius: 8px;
    flex-shrink: 0; /* Важно: предотвращает сжатие изображений */
}

/* Чтобы создать эффект бесконечной прокрутки, дублируем изображения.
   Это не идеальное решение, но работает для CSS-only.
   Например, если у вас 3 изображения, продублируйте их 1-2 раза.
   image1.jpg, image2.jpg, image3.jpg, image1.jpg, image2.jpg
*/
.carousel-images img:nth-child(n) {
    /* Можно добавить небольшие отступы, если нужно */
    margin-right: 0px; /* Adjust as needed */
}

/* Анимация прокрутки */
@keyframes autoScroll {
    0% {
        transform: translateX(0%);
    }
    100% {
        /*
           Расчет: (количество изображений - 1) * 100%
           Если у вас 3 уникальных изображения, и вы их дублируете до 5 штук:
           (5 изображений - 1) * 100% = 400%
           Но для бесшовной цикличной прокрутки, особенно когда изображения дублируются,
           нужно прокрутить ровно на ширину *уникальных* изображений.
           Если у вас 3 уникальных изображения и вы продублировали их,
           чтобы в сумме получилось 6 (img1, img2, img3, img1, img2, img3),
           то прокрутка должна быть на ширину 3 изображений.
           -300% означает прокрутку на ширину 3-х изображений влево.
        */
        transform: translateX(-300%); /* Пример для 3 уникальных изображений */
    }
}

/* Опционально: пауза при наведении (работает, если элемент поддерживает :hover) */
.carousel-container:hover .carousel-images {
    animation-play-state: paused;
}

</style>

