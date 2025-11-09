from rest_framework import serializers
from .models import Teacher, Question, Response


class TeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    short_name = serializers.ReadOnlyField()

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'full_name', 'short_name']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'order']
        read_only_fields = ['id']


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'teacher', 'question', 'rating', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class BulkResponseSerializer(serializers.Serializer):
    """Сериализатор для массовой отправки ответов"""
    responses = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )

    def validate_responses(self, value):
        """Валидация массива ответов"""
        for item in value:
            if 'teacher' not in item or 'question' not in item or 'rating' not in item:
                raise serializers.ValidationError(
                    'Каждый ответ должен содержать teacher, question и rating'
                )
            
            rating = item.get('rating')
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise serializers.ValidationError(
                    'Оценка должна быть целым числом от 1 до 5'
                )
        
        return value

    def create(self, validated_data):
        """Создание множества ответов"""
        responses_data = validated_data['responses']
        created_responses = []
        
        for response_data in responses_data:
            response = Response.objects.create(
                teacher_id=response_data['teacher'],
                question_id=response_data['question'],
                rating=response_data['rating']
            )
            created_responses.append(response)
        
        return created_responses
