from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from .models import Login, User, Contact
from django.utils.timezone import now

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    date_time = serializers.DateTimeField()

    class Meta:
        model = Login
        fields = ['email', 'password', 'date_time']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'email': 'Email is not registered.'})

        if not check_password(password, user.password):
            raise serializers.ValidationError({'password': 'Incorrect password.'})

        if 'date_time' not in data or not data['date_time']:
            data['date_time'] = now()

        return data

    def create(self, validated_data):
        return Login.objects.create(
            email=validated_data['email'],
            date_time=validated_data['date_time']
        )

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'message']

    def validate_phone_number(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value