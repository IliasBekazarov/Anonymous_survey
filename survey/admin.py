from django.contrib import admin
from .models import Teacher, Question, Response


from django.contrib import admin
from .models import Teacher, Question, Response, SurveySession


@admin.register(SurveySession)
class SurveySessionAdmin(admin.ModelAdmin):
    list_display = ['session_id_short', 'ip_address', 'has_completed', 'started_at', 'completed_at', 'response_count']
    list_filter = ['has_completed', 'started_at', 'completed_at']
    search_fields = ['session_id', 'ip_address']
    readonly_fields = ['session_id', 'ip_address', 'user_agent', 'browser_fingerprint', 'started_at', 'completed_at']
    ordering = ['-started_at']
    
    def session_id_short(self, obj):
        return f"{obj.session_id[:20]}..."
    session_id_short.short_description = 'Session ID'
    
    def response_count(self, obj):
        return obj.responses.count()
    response_count.short_description = 'Количество ответов'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'created_at']
    search_fields = ['first_name', 'last_name']
    ordering = ['last_name', 'first_name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['order', 'text', 'created_at']
    list_display_links = ['text']
    list_editable = ['order']
    ordering = ['order']


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'question', 'rating', 'session', 'timestamp']
    list_filter = ['teacher', 'rating', 'timestamp', 'session__has_completed']
    search_fields = ['teacher__first_name', 'teacher__last_name', 'session__ip_address']
    readonly_fields = ['session', 'timestamp']
    ordering = ['-timestamp']
