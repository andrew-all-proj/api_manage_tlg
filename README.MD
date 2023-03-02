# Развертывание на локальной машине
1. Создаем виртуальное окружение: python3 -m venv venv
2. Активируем venv: source venv/bin/activate
3. Устанавливаем зависимости: pip install -r requirements.txt

4. Создаем локальную БД: flask db upgrade

# Создание пользователя
1. sudo useradd -d /opt/api_managetlg user_managetlg
2. Даем права на папку chown -R user_managetlg:user_managetlg /opt/api_managetlg

# Создание БД
1. Переходим под пользователя sudo su postgres
2. Создаем роль для БД (user_managetlg) createuser --interactive
3. Создаем БД sudo -u postgres createdb db_managetlg
4. Проверка psql 
            \l
5. задать пароль psql
                 \password user_managetlg

6. Дать права на БД 
            psql
            GRANT ALL PRIVILEGES ON DATABASE "db_managetlg" to user_managetlg;

# Миграции
1. Активировать миграции: flask db init
2. Создать миграцию: flask db migrate -m "start"
3. Применить миграции: flask db upgrade

#Загрузка fixture
1.  Ввести в консоль: python .\load_fixtures.py --fixture <name file fixture .json> 
python load_fixtures.py --fixture type_media.json