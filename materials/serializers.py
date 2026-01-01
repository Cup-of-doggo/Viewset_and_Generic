from rest_framework import serializers
from materials.models import Course, Lesson



class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_counter = serializers.SerializerMethodField()
    lesson_info = LessonSerializer(source='lessons', read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_lessons_counter(obj):
        if obj.lessons:
            return obj.lessons.count()
