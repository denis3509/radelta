ДЛя запуска нужен .env. Пример .env файла в .env.sample, можно взять его.

Перед запуском необходимо применить миграции

`docker compose run django python manage.py migrate`

После можно запускать 

`docker compose up`

Запустить задачу вычисления стоимости доставки:

`docker compose run python manage.py updatecosts` 


Swagger: 

`{hostname}/api/schema/docs/`