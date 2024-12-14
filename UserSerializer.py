from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'is_staff']

    # Create new user
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        # Hash the password
        user.set_password(validated_data['password']) 
        user.save()
        return user

    # Update user
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        # Update password ken mawjoud
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance
