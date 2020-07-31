# GAZ
How to delete debug.log:  
  * 1 delete from repo  
  * 2 in local do:  
  >  git rm --cache <name>  
  > git commit -am <name>  
  * 3 if not in gitignor - add to gitignor
  
How to fetch new branch from GitHub :
  * git fetch origin  (fetch сливает изменения с гитхаба, но не применяет их. origin - это стандартное название удаленного репозитория)
  * git checkout -b <название ветки> <origin>/<название ветки>

Удаление базы данных:
 * удалить миграции из папки planes/migrations (все содержимое папки migrations)
 * python manage.py makemigrations planes
 * python manage.py migrate
 * python manage.py loaddata initial_data.json

Запуск сервера:
 * python manage.py runserver

