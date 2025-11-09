from django.core.management.base import BaseCommand
from survey.models import Teacher, Question


class Command(BaseCommand):
    help = 'Загрузка начальных данных: преподавателей и вопросов'

    def handle(self, *args, **kwargs):
        self.stdout.write('Загрузка начальных данных...')

        # Список из 23 преподавателей
        teachers_data = [
            ('Анна', 'Иванова'),
            ('Борис', 'Петров'),
            ('Виктор', 'Сидоров'),
            ('Галина', 'Смирнова'),
            ('Дмитрий', 'Козлов'),
            ('Елена', 'Новикова'),
            ('Жанна', 'Морозова'),
            ('Игорь', 'Волков'),
            ('Ирина', 'Соколова'),
            ('Кирилл', 'Лебедев'),
            ('Лариса', 'Козлова'),
            ('Михаил', 'Новиков'),
            ('Наталья', 'Федорова'),
            ('Олег', 'Михайлов'),
            ('Павел', 'Александров'),
            ('Раиса', 'Кузнецова'),
            ('Сергей', 'Попов'),
            ('Татьяна', 'Васильева'),
            ('Ульяна', 'Петрова'),
            ('Федор', 'Семенов'),
            ('Эльвира', 'Романова'),
            ('Юрий', 'Григорьев'),
            ('Яков', 'Степанов'),
        ]

        # Создание преподавателей
        created_teachers = 0
        for first_name, last_name in teachers_data:
            teacher, created = Teacher.objects.get_or_create(
                first_name=first_name,
                last_name=last_name
            )
            if created:
                created_teachers += 1
                self.stdout.write(f'  Создан преподаватель: {teacher}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Преподаватели: создано {created_teachers}, '
                f'всего {Teacher.objects.count()}'
            )
        )

        # Список из 15 вопросов
        questions_data = [
            'Преподаватель доступно объясняет материал',
            'Преподаватель использует современные методы обучения',
            'Преподаватель проявляет уважение к студентам',
            'Преподаватель справедливо оценивает знания',
            'Преподаватель заинтересован в успехе студентов',
            'Занятия проходят организованно и по расписанию',
            'Преподаватель компетентен в своей области',
            'Преподаватель отвечает на вопросы студентов',
            'Преподаватель поддерживает дисциплину на занятиях',
            'Преподаватель мотивирует к изучению предмета',
            'Преподаватель использует практические примеры',
            'Преподаватель дает полезные домашние задания',
            'Преподаватель доступен для консультаций',
            'Преподаватель использует интерактивные методы',
            'Общая оценка преподавателя',
        ]

        # Создание вопросов
        created_questions = 0
        for order, text in enumerate(questions_data, start=1):
            question, created = Question.objects.get_or_create(
                order=order,
                defaults={'text': text}
            )
            if created:
                created_questions += 1
                self.stdout.write(f'  Создан вопрос {order}: {text[:50]}...')

        self.stdout.write(
            self.style.SUCCESS(
                f'Вопросы: создано {created_questions}, '
                f'всего {Question.objects.count()}'
            )
        )

        self.stdout.write(self.style.SUCCESS('Загрузка данных завершена!'))
