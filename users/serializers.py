from django.contrib.auth.models import User
from rest_framework import serializers



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    class Meta:
        model = User
        fields = ['username','password','email']

    def create(self,validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data.get('email','')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','is_active','is_staff']
        read_only_fields = ['id','username','email']
