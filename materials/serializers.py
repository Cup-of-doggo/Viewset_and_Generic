from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import LessonValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LessonValidator(field='link')]

class CourseSerializer(serializers.ModelSerializer):
    lessons_counter = serializers.SerializerMethodField()
    lesson_info = LessonSerializer(source='lessons', read_only=True, many=True)
    sub_check = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_lessons_counter(obj):
        if obj.lessons:
            return obj.lessons.count()

    @staticmethod
    def is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False