elib
====
Это тестовое web-приложение по управлению электронной библиотекой.

http://alx-elib.herokuapp.com/

Установка зависимостей:
```
pip install -r requirements.txt
```

Создание таблиц в БД:
```python
>>> from elib.database import init_db
>>> init_db()
```
или
```
$ sqlite3 sqlite.db < init.sql
```

Наполнение наблиц начальными данными:
```
$ sqlite3 sqlite.db < data.sql
```

Данные для входа:
```
alex:pass
nic:pass2
```
