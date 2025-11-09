from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Count, Max
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response as DRFResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
import csv
from datetime import datetime
import json

from .models import Teacher, Question, Response, SurveySession
from .serializers import (
    TeacherSerializer,
    QuestionSerializer,
    ResponseSerializer,
    BulkResponseSerializer
)
from .utils import get_client_ip, get_user_agent, generate_session_id


# ============= СТРАНИЦЫ =============

@ensure_csrf_cookie
def index(request):
    """Главная страница с опросом"""
    return render(request, 'survey/index.html')


@ensure_csrf_cookie
def admin_panel_view(request):
    """Страница админ-панели"""
    return render(request, 'survey/admin_panel.html')


# ============= API ДЛЯ ОПРОСА =============

@api_view(['GET'])
def check_session_status(request):
    """Проверка, прошел ли уже студент опрос"""
    # Получаем данные из запроса
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    browser_fingerprint = request.GET.get('fingerprint', '')
    
    # Генерируем session_id
    session_id = generate_session_id(ip_address, user_agent, browser_fingerprint)
    
    # Проверяем, есть ли уже завершенная сессия
    try:
        session = SurveySession.objects.get(session_id=session_id)
        if session.has_completed:
            return DRFResponse({
                'can_take_survey': False,
                'message': 'Сіз мурунтан эле тесттен өттүңүз',
                'completed_at': session.completed_at
            })
        else:
            return DRFResponse({
                'can_take_survey': True,
                'session_id': session_id,
                'message': 'Тестти улантууга болот'
            })
    except SurveySession.DoesNotExist:
        # Создаем новую сессию
        session = SurveySession.objects.create(
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            browser_fingerprint=browser_fingerprint
        )
        return DRFResponse({
            'can_take_survey': True,
            'session_id': session_id,
            'message': 'Жаңы сессия башталды'
        })


@api_view(['GET'])
def teachers_list(request):
    """Список всех преподавателей"""
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return DRFResponse(serializer.data)


@api_view(['GET'])
def questions_list(request):
    """Список всех вопросов"""
    questions = Question.objects.all().order_by('order')
    serializer = QuestionSerializer(questions, many=True)
    return DRFResponse(serializer.data)


@api_view(['POST'])
def submit_responses(request):
    """Отправка ответов на опрос"""
    # Получаем данные из запроса
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    browser_fingerprint = request.data.get('fingerprint', '')
    
    # Генерируем session_id
    session_id = generate_session_id(ip_address, user_agent, browser_fingerprint)
    
    # Проверяем сессию
    try:
        session = SurveySession.objects.get(session_id=session_id)
        
        # Если уже прошел опрос, запрещаем
        if session.has_completed:
            return DRFResponse(
                {'error': 'Сіз мурунтан эле тесттен өттүңүз. Кайталап өтүүгө болбойт!'},
                status=status.HTTP_403_FORBIDDEN
            )
    except SurveySession.DoesNotExist:
        # Создаем новую сессию если не существует
        session = SurveySession.objects.create(
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            browser_fingerprint=browser_fingerprint
        )
    
    # Сохраняем ответы
    responses_data = request.data.get('responses', [])
    
    if not responses_data:
        return DRFResponse(
            {'error': 'Жок дегенде бир мугалимди баалаңыз'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Добавляем session к каждому ответу
    for response_item in responses_data:
        response_item['session_id'] = session.id
    
    serializer = BulkResponseSerializer(data={'responses': responses_data})
    
    if serializer.is_valid():
        # Сохраняем ответы с привязкой к сессии
        saved_responses = []
        for response_data in responses_data:
            response_obj = Response.objects.create(
                session=session,
                teacher_id=response_data['teacher'],
                question_id=response_data['question'],
                rating=response_data['rating']
            )
            saved_responses.append(response_obj)
        
        # Отмечаем сессию как завершенную
        session.complete()
        
        return DRFResponse(
            {
                'message': 'Жооптор ийгиликтүү сакталды! Рахмат!',
                'count': len(saved_responses)
            },
            status=status.HTTP_201_CREATED
        )
    
    return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def total_responses_count(request):
    """Общее количество ответов"""
    count = Response.objects.count()
    return DRFResponse({'total': count})


# ============= API ДЛЯ СТАТИСТИКИ =============

@api_view(['GET'])
def teacher_ratings(request):
    """Рейтинг преподавателей с расчетом среднего балла"""
    teachers = Teacher.objects.all()
    results = []
    
    for teacher in teachers:
        responses = Response.objects.filter(teacher=teacher)
        total_responses = responses.count()
        
        if total_responses > 0:
            avg_rating = responses.aggregate(Avg('rating'))['rating__avg']
            avg_rating = round(avg_rating, 2)
        else:
            avg_rating = 0
        
        results.append({
            'id': teacher.id,
            'name': teacher.full_name,
            'short_name': teacher.short_name,
            'average_rating': avg_rating,
            'total_responses': total_responses
        })
    
    # Сортировка по среднему баллу
    results.sort(key=lambda x: x['average_rating'], reverse=True)
    
    return DRFResponse(results)


@api_view(['GET'])
def detailed_statistics(request):
    """Детальная статистика для таблицы результатов"""
    teachers = Teacher.objects.all()
    questions = Question.objects.all().order_by('order')
    
    results = []
    
    for teacher in teachers:
        teacher_data = {
            'id': teacher.id,
            'name': teacher.full_name,
            'short_name': teacher.short_name,
            'questions': {}
        }
        
        total_sum = 0
        total_count = 0
        
        for question in questions:
            responses = Response.objects.filter(teacher=teacher, question=question)
            count = responses.count()
            
            if count > 0:
                avg = responses.aggregate(Avg('rating'))['rating__avg']
                avg = round(avg, 2)
                total_sum += avg * count
                total_count += count
            else:
                avg = 0
            
            teacher_data['questions'][f'q{question.order}'] = {
                'average': avg,
                'count': count
            }
        
        # Общий средний балл и количество ответов
        if total_count > 0:
            teacher_data['overall_average'] = round(total_sum / total_count, 2)
        else:
            teacher_data['overall_average'] = 0
        
        teacher_data['total_responses'] = total_count
        
        results.append(teacher_data)
    
    return DRFResponse({
        'teachers': results,
        'questions': QuestionSerializer(questions, many=True).data
    })


# ============= API ДЛЯ УПРАВЛЕНИЯ ВОПРОСАМИ =============

@api_view(['POST'])
def create_question(request):
    """Создание нового вопроса (только для админа)"""
    if not request.user.is_authenticated:
        return DRFResponse(
            {'error': 'Требуется аутентификация'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Получаем максимальный order
    max_order = Question.objects.aggregate(Max('order'))['order__max'] or 0
    
    data = request.data.copy()
    data['order'] = max_order + 1
    
    serializer = QuestionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return DRFResponse(serializer.data, status=status.HTTP_201_CREATED)
    
    return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_question(request, question_id):
    """Удаление вопроса (только для админа)"""
    if not request.user.is_authenticated:
        return DRFResponse(
            {'error': 'Требуется аутентификация'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        question = Question.objects.get(id=question_id)
        question.delete()
        return DRFResponse({'message': 'Вопрос удален'}, status=status.HTTP_204_NO_CONTENT)
    except Question.DoesNotExist:
        return DRFResponse(
            {'error': 'Вопрос не найден'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PATCH'])
def update_question(request, question_id):
    """Обновление вопроса (только для админа)"""
    if not request.user.is_authenticated:
        return DRFResponse(
            {'error': 'Требуется аутентификация'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        question = Question.objects.get(id=question_id)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return DRFResponse(serializer.data)
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Question.DoesNotExist:
        return DRFResponse(
            {'error': 'Вопрос не найден'},
            status=status.HTTP_404_NOT_FOUND
        )


# ============= АУТЕНТИФИКАЦИЯ =============

@api_view(['POST'])
@csrf_exempt
def login_view(request):
    """Вход в админ-панель"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return DRFResponse({
            'message': 'Успешный вход',
            'user': {
                'username': user.username,
                'is_staff': user.is_staff
            }
        })
    else:
        return DRFResponse(
            {'error': 'Неверные логин или пароль'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
def logout_view(request):
    """Выход из админ-панели"""
    logout(request)
    return DRFResponse({'message': 'Выход выполнен'})


@api_view(['GET'])
def auth_status(request):
    """Проверка статуса аутентификации"""
    if request.user.is_authenticated:
        return DRFResponse({
            'authenticated': True,
            'user': {
                'username': request.user.username,
                'is_staff': request.user.is_staff
            }
        })
    else:
        return DRFResponse({'authenticated': False})


# ============= ЭКСПОРТ В CSV =============

@api_view(['GET'])
def export_csv(request):
    """Экспорт статистики в CSV"""
    # Создаем HTTP ответ с типом CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="результаты_опроса_{datetime.now().strftime("%Y-%m-%d")}.csv"'
    
    # Добавляем UTF-8 BOM для корректного отображения кириллицы в Excel
    response.write('\ufeff')
    
    # Создаем writer с разделителем точка с запятой
    writer = csv.writer(response, delimiter=';')
    
    # Получаем данные
    teachers = Teacher.objects.all().order_by('last_name', 'first_name')
    questions = Question.objects.all().order_by('order')
    
    # Заголовок
    header = ['Преподаватель']
    header.extend([f'В{q.order}' for q in questions])
    header.extend(['Средний балл', 'Всего ответов'])
    writer.writerow(header)
    
    # Данные по каждому преподавателю
    for teacher in teachers:
        row = [teacher.full_name]
        
        total_sum = 0
        total_count = 0
        
        for question in questions:
            responses = Response.objects.filter(teacher=teacher, question=question)
            count = responses.count()
            
            if count > 0:
                avg = responses.aggregate(Avg('rating'))['rating__avg']
                avg = round(avg, 2)
                row.append(f'{avg} ({count})')
                total_sum += avg * count
                total_count += count
            else:
                row.append('-')
        
        # Средний балл и количество ответов
        if total_count > 0:
            overall_avg = round(total_sum / total_count, 2)
            row.append(str(overall_avg))
        else:
            row.append('-')
        
        row.append(str(total_count))
        
        writer.writerow(row)
    
    return response
