## Комментарии к работе

 - Для рендера нового меню необходимо добавить в файл
   *tree/templates/menu/index.html* тег с требуемым названием. В случае отсутствия таких элементов меню в БД приложение вернет ошибку. На данный момент выводится два меню: main_menu и minor_menu. 
   ![Image
   alt](https://github.com/BystrovN/images/raw/master/uptrader_test/tag.png)
   
 - При рендере одного меню - один запрос к БД. Скрин с двумя меню на странице:
	![Image
   alt](https://github.com/BystrovN/images/raw/master/uptrader_test/4_sql.png)
   
 - Для уменьшения запросов к БД queryset со всеми пунктами меню кешируется по умолчанию на 5 секунд. Время жизни можно изменить в settings.py. Скрин с двумя меню в кеше:
	![Image
   alt](https://github.com/BystrovN/images/raw/master/uptrader_test/2_sql.png)
   
 - Для ознакомления с работой подготовлены тестовые данные. Для загрузка их в базу из каталога *tree/* необходимо выполнить команду:
  ``` python manage.py loaddata dump.json ```

## Запуск

1. После клонирования проекта рекомендуется использовать виртуальное окружение для дальнейшего развертывания.
```
	python3.11 -m venv venv
```

2. Установить зависимости:
```
	pip install -r requirements.txt
```

3. Выполнить миграции:
```
	python manage.py migrate
```
4. Запуск:
```
	python manage.py runserver
```


## Стек

 - Python - 3.11
 - Django - 4.1