## 4. Сервис пользователей (Users Service)

### Зона ответственности
- Регистрация новых пользователей (создание учётной записи).
- Аутентификация (проверка логина/пароля, генерация токенов, валидация сессий).
- Хранение данных о пользователях (логин, пароль (хэш), профильная информация, статус, роли/права).

### Границы
- Не обрабатывает посты или комментарии: все операции с контентом (посты/промокоды, комментарии) вынесены в отдельный сервис.
- Не занимается статистикой (лайками, просмотрами), передаёт лишь события (например, при регистрации) или предоставляет информацию о пользователе, когда запрашивается из других сервисов.
- Имеет собственную базу данных (PostgreSQL), где хранит исключительно данные о пользователях.

