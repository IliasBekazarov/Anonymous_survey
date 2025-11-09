# PythonAnywhere deployment инструкциялары

## 1. PythonAnywhere'де аккаунт түзүңүз
https://www.pythonanywhere.com/ - Beginner аккаунт (бекер)

## 2. Bash console ачыңыз
Dashboard -> Consoles -> Bash

## 3. GitHub'дан кодду клондоңуз
```bash
git clone https://github.com/IliasBekazarov/Anonymous_survey.git
cd Anonymous_survey
```

## 4. Virtual environment түзүңүз
```bash
mkvirtualenv --python=/usr/bin/python3.10 survey_env
pip install -r requirements.txt
```

## 5. Settings файлын production үчүн даярдаңыз

`survey_project/settings.py` файлында төмөнкүлөрдү өзгөртүңүз:

```python
DEBUG = False
ALLOWED_HOSTS = ['<сиздин-username>.pythonanywhere.com', 'localhost', '127.0.0.1']
```

## 6. Static файлдарды жыйноо
```bash
python manage.py collectstatic
```

## 7. Маалымат базасын миграциялоо
```bash
python manage.py migrate
```

## 8. Superuser түзүңүз
```bash
python manage.py createsuperuser
```

## 9. Баштапкы маалыматтарды жүктөө (опционалдуу)
```bash
python manage.py load_initial_data
```

## 10. Web app конфигурациялоо

Dashboard -> Web -> Add a new web app:
- Manual configuration
- Python 3.10

### WSGI файлы конфигурациясы
`/var/www/<username>_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/<username>/Anonymous_survey'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'survey_project.settings'

# Activate your virtual env
activate_this = '/home/<username>/.virtualenvs/survey_env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Static files mapping
Web tab -> Static files:
- URL: `/static/`
- Directory: `/home/<username>/Anonymous_survey/staticfiles/`

### Virtual environment
Virtualenv: `/home/<username>/.virtualenvs/survey_env`

## 11. Reload сайтты
Web tab -> Reload button

## 12. Сайтты текшерүү
`<username>.pythonanywhere.com`

---

## Кошумча settings

`.env` файл (production):
```env
SECRET_KEY=your-super-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=<username>.pythonanywhere.com,localhost,127.0.0.1
```

## Маалымат базасын резервдөө
```bash
python manage.py dumpdata > backup.json
```

## Маалыматтарды калыбына келтирүү
```bash
python manage.py loaddata backup.json
```

## Logs текшерүү
PythonAnywhere Dashboard -> Files -> /var/log/<username>.pythonanywhere.com.error.log

---

## Маанилүү эскертүүлөр:

1. ⚠️ Free аккаунт чектөөлөрү:
   - Бир гана web app
   - Күндүз 100,000 хит
   - 512MB RAM

2. 🔒 Коопсуздук:
   - DEBUG = False өзгөртүңүз
   - SECRET_KEY өзгөртүңүз
   - ALLOWED_HOSTS туура толтуруңуз

3. 📊 База маалыматтары:
   - SQLite free аккаунтта иштейт
   - Production үчүн PostgreSQL сунушталат (paid)

4. 🔄 Жаңыртуулар:
   ```bash
   cd Anonymous_survey
   git pull
   python manage.py migrate
   python manage.py collectstatic --noinput
   # Reload web app
   ```
