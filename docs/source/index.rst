Любимые места
=============

Сервис для сохранения информации о любимых местах.

Зависимости
===========

Установите требуемое ПО:

1. |link_docker|

.. |link_docker| raw:: html

   <a href="https://www.docker.com" target="_blank">Docker Desktop</a>

2. |link_git|

.. |link_git| raw:: html

   <a href="https://github.com/git-guides/install-git" target="_blank">Git</a>

3. |link_pycharm|

.. |link_pycharm| raw:: html

    <a href="https://www.jetbrains.com/ru-ru/pycharm/download" target="_blank">PyCharm</a> (опционально).



Установка
=========

Склонируйте репозиторий на свой ПК:

    .. code-block:: console

        git clone https://github.com/mnv/python-course-favorite-places.git

1. Скопируйте файл настроек `.env.sample`, создав файл `.env`:

    .. code-block:: console

        cp .env.sample .env

    Этот файл содержит переменные окружения, значения которых будут общими для всего приложения.
    Файл-образец (`.env.sample`) содержит набор переменных со значениями по умолчанию,
    поэтому он может быть настроен в зависимости от окружения.

2. Соберите Docker-контейнер с помощью Docker Compose:

    .. code-block:: console

        docker compose build

    Эта команда должна быть запущена из корневого каталога, в котором расположен `Dockerfile`.
    Вам также необходимо собрать контейнер заново, если вы обновили `requirements.txt`.

3. Для корректной работы приложения настройте базу данных.
   Примените миграции для создания таблиц в базе данных:

    .. code-block:: console

        docker compose run favorite-places-app alembic upgrade head

4. Теперь можно запустить проект внутри контейнера:

    .. code-block:: console

        docker compose up

   Когда контейнеры подняты, сервер запускается по адресу [http://0.0.0.0:8010/docs](http://0.0.0.0:8010/docs). Вы можете отрыть его в браузере.

Использование
=============



Работа с базой данных
---------------------
При первом запуске выполните команду:

    .. code-block:: console

        docker compose exec favorite-places-app alembic init -t async migrations


Для создания новых миграций, которые будут обновлять таблицы базы данных в соответствии с обновленными моделями, выполните эту команду:

    .. code-block:: console

        docker compose run favorite-places-app alembic revision --autogenerate  -m "your description"

Для применения созданных миграций выполните команду:

    .. code-block:: console

        docker compose run favorite-places-app alembic upgrade head



Автоматизация
=============

Проект содержит специальный файл (`Makefile`) для автоматизации выполнения команд:

1. Сборка Docker-контейнера:

    .. code-block:: console

        make build

2. Генерация доументации:

    .. code-block:: console

        make docs-html

3. Запуск форматирования кода:

    .. code-block:: console

        make format

4. Запуск статического анализа кода (выявление ошибок типов и форматирования кода):

    .. code-block:: console

        make lint

5. Запуск автоматических тестов:

    .. code-block:: console

        make test

    Отчет о покрытии тестами будет расположен по адресу `src/htmlcov/index.html`.
    Таким образом, вы можете оценить качество покрытия автоматизированных тестов.

6. Запуск всех функций поддержки качества кода (форматирование, линтеры, автотесты):

    .. code-block:: console

        make all



Тестирование
============

Для запуска автоматических тестов выполните команду:

    .. code-block:: console

        docker compose run app pytest --cov=/src --cov-report html:htmlcov --cov-report term --cov-config=/src/tests/.coveragerc -vv

Также существует аналогичная `make`-команда:

    .. code-block:: console

        make test

Отчет о тестировании находится в файле `src/htmlcov/index.html`.

Документация
============

Клиенты
=======
Базовый
--------
.. automodule:: clients.base.base
    :members:

Гео
---
.. automodule:: clients.geo
    :members:

Схемы
-------
.. automodule:: clients.shemas
    :members:

Интеграции
============
Базы данных
--------
.. automodule:: integrations.db.session
    :members:
События
------
.. automodule:: integrations.events.producer
    :members:
.. automodule:: integrations.events.schemas
    :members:

Модели
======
.. automodule:: models.mixins
    :members:
.. automodule:: models.places
    :members:

Репозитории
============
.. automodule:: repositories.base_repository
    :members:
.. automodule:: repositories.places_repository
    :members:

Схемы
=======
.. automodule:: schemas.base
    :members:
.. automodule:: schemas.places
    :members:
.. automodule:: schemas.routes
    :members:

Сервисы
=======
.. automodule:: services.places_service
    :members:


Транспорт
=========
.. automodule:: transport.handlers.places
    :members:
