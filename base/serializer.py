from .models import User, ExpenseParticipant, ExpenseGroup

from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset = User.objects.all())])
    password = serializers.CharField(write_only =True,required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password':"Password fields didn't match"})

        return attrs
    

    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data.get('email', None),
            first_name = validated_data.get('first_name',None),
            last_name = validated_data.get('last_name', None)
            )

        user.set_password(validated_data['password'])
        user.save()

        return user
    

class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only =True,required=True)
    
    class Meta:
        model = User
        fields = ('email', 'password')



class ExpenseGroupSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    participants = serializers.ListField()
    class Meta:
        model = ExpenseGroup
        fields = "__all__"