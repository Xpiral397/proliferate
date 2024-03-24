from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from base.models import Profile


class UserSerializer(serializers.ModelSerializer):
    #name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id',"_id",'username','first_name','last_name', 'email',"isAdmin",]


    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self,obj):
        return obj.is_staff



class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['username','email',"isAdmin",'first_name','last_name', 'token']

    def get_token(self, obj):
        token =RefreshToken.for_user(obj)
        return str(token.access_token)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']




