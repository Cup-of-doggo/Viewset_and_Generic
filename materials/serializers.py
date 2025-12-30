from rest_framework import serializers
from materials.models import Course, Lesson



class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'



class CourseSerializer(serializers.ModelSerializer):
    lessons_counter = serializers.SerializerMethodField()
    lesson_info = LessonSerializer(source='lesson_set.all.lesson')

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_lessons_counter(obj):

        return obj.lesson_in_course.count()
