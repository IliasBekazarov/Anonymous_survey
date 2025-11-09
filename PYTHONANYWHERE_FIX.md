## 🔥 PYTHONANYWHERE БОЮНЧА ТОЛУК ЧЕЧИМ

### Көйгөй: /admin/ жана /result/ иштебейт

Бул көбүнчө WSGI конфигурациясы же static файлдар көйгөйү.

---

## ✅ ТОЛУК ОҢДОО КАДАМДАРЫ:

### 1. GitHub'дан акыркы версияны алыңыз

```bash
cd ~/Anonymous_survey
git pull
```

### 2. Virtual environment текшериңиз

```bash
# Virtual env барбы текшерүү
ls ~/.virtualenvs/

# Эгерде жок болсо, түзүңүз:
mkvirtualenv --python=/usr/bin/python3.10 survey_env

# Активациялоо
workon survey_env

# Проверка
which python
# Натыйжа: /home/opros123/.virtualenvs/survey_env/bin/python
```

### 3. Пакеттерди орнотуу

```bash
cd ~/Anonymous_survey
pip install -r requirements.txt
```

### 4. Database жана static файлдар

```bash
# Миграциялар
python manage.py migrate

# Static файлдарды жыйноо
python manage.py collectstatic --noinput

# Superuser түзүү (эгерде жок болсо)
python manage.py createsuperuser
```

### 5. Settings файлын текшерүү

Bash консолдо:

```bash
cd ~/Anonymous_survey
nano survey_project/settings.py
```

`ALLOWED_HOSTS` сабында төмөнкү болушу керек:

```python
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'opros123.pythonanywhere.com,localhost,127.0.0.1').split(',')
```

`Ctrl+O` → Enter → `Ctrl+X` (сактоо жана чыгуу)

### 6. WSGI файлын ТУУРА конфигурациялоо

**Dashboard → Web → Code → WSGI configuration file**

Файлды ачып, **БАРДЫГЫН ӨЧҮРҮП**, бул кодду коюңуз:

```python
import os
import sys

# ============ МААНИЛҮҮ: opros123 дегенди өзүңүздүн username менен алмаштырыңыз! ============

# Project path
path = '/home/opros123/Anonymous_survey'
if path not in sys.path:
    sys.path.insert(0, path)

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'survey_project.settings'

# Environment variables - PRODUCTION үчүн
os.environ['SECRET_KEY'] = 'your-super-secret-production-key-change-this-12345'
os.environ['DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = 'opros123.pythonanywhere.com,localhost,127.0.0.1'

# Virtual environment activation
activate_this = '/home/opros123/.virtualenvs/survey_env/bin/activate_this.py'
try:
    with open(activate_this) as f:
        code = compile(f.read(), activate_this, 'exec')
        exec(code, dict(__file__=activate_this))
except FileNotFoundError:
    # Эгерде activate_this.py табылбаса, PATH кошуу
    site_packages = '/home/opros123/.virtualenvs/survey_env/lib/python3.10/site-packages'
    if site_packages not in sys.path:
        sys.path.insert(0, site_packages)

# Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**ӨЗГӨРТҮҮЛӨР** (3 жерде):
1. `/home/opros123/` → `/home/СИЗДИН_USERNAME/`
2. `opros123.pythonanywhere.com` → `СИЗДИН_USERNAME.pythonanywhere.com`
3. SECRET_KEY → башка кылыңыз!

### 7. Web App Settings

**Dashboard → Web** бөлүмүндө текшериңиз:

#### A. Source code:
```
/home/opros123/Anonymous_survey
```

#### B. Working directory:
```
/home/opros123/Anonymous_survey
```

#### C. Virtualenv:
```
/home/opros123/.virtualenvs/survey_env
```

#### D. Static files mapping:

**МААНИЛҮҮ!** Эки саптык кошуңуз:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/opros123/Anonymous_survey/staticfiles/` |
| `/static/admin/` | `/home/opros123/.virtualenvs/survey_env/lib/python3.10/site-packages/django/contrib/admin/static/admin/` |

### 8. Python версиясы

Python version: **3.10**

### 9. RELOAD!

Чоң жашыл **Reload** баскычын басыңыз!

---

## 🔍 ТЕКШЕРҮҮ:

### Error логун окуу:

```bash
tail -100 /var/log/opros123.pythonanywhere.com.error.log
```

### Кандай каталар издөө:

1. **ModuleNotFoundError: No module named 'django'**
   - Virtual env туура эмес
   - `workon survey_env && pip install -r requirements.txt`

2. **DisallowedHost at /**
   - ALLOWED_HOSTS туура эмес
   - WSGI файлында ALLOWED_HOSTS текшириңиз

3. **Static files 404**
   - `python manage.py collectstatic --noinput`
   - Static files mapping текшириңиз

4. **OperationalError: no such table**
   - `python manage.py migrate`

---

## 🎯 ИШТЕШИ КЕРЕК УРЛДАР:

Эгерде бардыгы туура болсо:

✅ `https://opros123.pythonanywhere.com/` - Башкы бет (опрос)
✅ `https://opros123.pythonanywhere.com/result/` - Админ панель  
✅ `https://opros123.pythonanywhere.com/admin/` - Django admin
✅ `https://opros123.pythonanywhere.com/api/teachers/` - API

---

## 🆘 ДАГЫ ИШТЕБЕСЕ:

Error log'дун АКЫРКЫ 50 сабын жөнөтүңүз:

```bash
tail -50 /var/log/opros123.pythonanywhere.com.error.log
```

Мен так катаны көрүп, чече алам!
