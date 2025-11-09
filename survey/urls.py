from django.urls import path
from . import views

urlpatterns = [
    # Страницы
    path('', views.index, name='index'),
    path('result/', views.admin_panel_view, name='admin_panel'),
    
    # API для опроса
    path('api/session/check/', views.check_session_status, name='check_session'),
    path('api/teachers/', views.teachers_list, name='teachers_list'),
    path('api/questions/', views.questions_list, name='questions_list'),
    path('api/responses/', views.submit_responses, name='submit_responses'),
    path('api/responses/count/', views.total_responses_count, name='total_responses_count'),
    
    # API для статистики
    path('api/statistics/ratings/', views.teacher_ratings, name='teacher_ratings'),
    path('api/statistics/detailed/', views.detailed_statistics, name='detailed_statistics'),
    
    # API для управления вопросами
    path('api/questions/create/', views.create_question, name='create_question'),
    path('api/questions/<int:question_id>/', views.update_question, name='update_question'),
    path('api/questions/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    
    # Аутентификация
    path('api/auth/login/', views.login_view, name='login'),
    path('api/auth/logout/', views.logout_view, name='logout'),
    path('api/auth/status/', views.auth_status, name='auth_status'),
    
    # Экспорт
    path('api/export/csv/', views.export_csv, name='export_csv'),
]
