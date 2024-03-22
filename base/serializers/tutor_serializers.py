from rest_framework import serializers
from base.models import TutorProfile,TutorVerifictions, classSchedule,Assignment,Class,Subject,ClassMessage

class TutorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorProfile
        fields = '__all__'


class TutorVerifictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorVerifictions
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class classScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = classSchedule
        fields = '__all__'


class  ClassMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMessage
        fields = '__all__'