from base.models import StudentProfile
from rest_framework import serializers




class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'
