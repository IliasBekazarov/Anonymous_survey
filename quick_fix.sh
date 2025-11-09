#!/bin/bash
# Quick Fix script for PythonAnywhere deployment issues

echo "🔧 Anonymous Survey - Quick Fix Script"
echo "======================================="
echo ""

# Check if in correct directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py табылган жок. Anonymous_survey директориясына өтүңүз:"
    echo "   cd ~/Anonymous_survey"
    exit 1
fi

# Activate virtual environment
echo "📦 Virtual environment активациялоо..."
source ~/.virtualenvs/survey_env/bin/activate

# Install/Update packages
echo "📥 Пакеттерди орнотуу/жаңылоо..."
pip install -r requirements.txt --quiet

# Run migrations
echo "🗄️  Database миграциялары..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Static файлдарды жыйноо..."
python manage.py collectstatic --noinput

# Check for errors
echo "✅ Django check иштетүү..."
python manage.py check --deploy

echo ""
echo "✅ Бүткөн! Эми төмөнкүлөрдү текшериңиз:"
echo "   1. Web tab → WSGI configuration файлын текшериңиз"
echo "   2. Web tab → Virtualenv: ~/.virtualenvs/survey_env"
echo "   3. Web tab → Static files: /static/ → ~/Anonymous_survey/staticfiles/"
echo "   4. Web tab → RELOAD баскычын басыңыз!"
echo ""
echo "📋 Logs текшерүү:"
echo "   tail -50 /var/log/\$USER.pythonanywhere.com.error.log"
