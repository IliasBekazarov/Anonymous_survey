from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class SurveySession(models.Model):
    """Модель для отслеживания уникальных сессий студентов"""
    session_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Уникальный идентификатор сессии',
        help_text='Комбинация IP + browser fingerprint'
    )
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес')
    user_agent = models.TextField(verbose_name='User Agent', blank=True)
    browser_fingerprint = models.CharField(
        max_length=255,
        verbose_name='Browser fingerprint',
        blank=True
    )
    has_completed = models.BooleanField(
        default=False,
        verbose_name='Опрос завершен'
    )
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Начало прохождения'
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время завершения'
    )

    class Meta:
        verbose_name = 'Сессия студента'
        verbose_name_plural = 'Сессии студентов'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['has_completed']),
        ]

    def __str__(self):
        status = "завершен" if self.has_completed else "в процессе"
        return f"Сессия {self.session_id[:20]}... ({status})"

    def complete(self):
        """Отметить сессию как завершенную"""
        self.has_completed = True
        self.completed_at = timezone.now()
        self.save()


class Teacher(models.Model):
    """Модель преподавателя"""
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def short_name(self):
        """Фамилия + первая буква имени"""
        return f"{self.last_name} {self.first_name[0]}."


class Question(models.Model):
    """Модель вопроса"""
    text = models.TextField(verbose_name='Текст вопроса')
    order = models.IntegerField(
        default=0,
        verbose_name='Порядок',
        help_text='Порядок отображения вопроса'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['order']

    def __str__(self):
        return f"Вопрос {self.order}: {self.text[:50]}"


class Response(models.Model):
    """Модель ответа студента"""
    session = models.ForeignKey(
        'SurveySession',
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Сессия',
        null=True,
        blank=True
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Преподаватель'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Вопрос'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['teacher', 'question']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.teacher} - {self.question.text[:30]} - {self.rating}"
