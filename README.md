# Тестовое задание Welltory

### Инструкции по запуску приложения:

##### В инструкции предпологаеться что у вас уже установлен docker и docker-compose

- Билдим приложение с помощью команды `docker-compose build`
- Запускаем его используя команду `docker-compose up -d`
- Для миграции БД используем команду `docker exec -it <id контейнера> python manage.py migrate`
- Создаем суперпользователя (для дальнейшей работы с API) с с помощью команды `docker exec -it <id контейнера> python manage.py createsuperuser`
- Сервер будет работать по ссылке http://localhost:8080/

### Инструкция по API:
- POST /login - для авторизации пользователей. После успешной авторизации сервер вернет токен пользователя
- GET /logout - Требует аутентификации по токену!
- POST /calculate - вычесление корреляции по заданным данным. Требует аутентификации по токену!
- GET /correlation?x_data_type=str&y_data_type=str&user_id=int - Вывод вычисленной корреляции по запрашивемым данным

### Примечание:
- Сделал задание на Django, так как он является моим основным фреймворком.
- В качетве базы данных использовал PostgreSQL. Так как он широко используется на Django проектах и у меня имеется больше опыта работы именно с этой СУБД.