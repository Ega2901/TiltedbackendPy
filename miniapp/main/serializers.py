from rest_framework import serializers
from .models import User, GlobalTask, UserTaskStatus,  Referral

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'telegram_id', 'username', 'nickname', 'points', 'avatar', 'referral_code']

class GlobalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalTask
        fields = ['id', 'task_name', 'task_description', 'task_image', 'points', 'task_url']

class UserTaskStatusSerializer(serializers.ModelSerializer):
    task = GlobalTaskSerializer()

    class Meta:
        model = UserTaskStatus
        fields = ['id', 'task', 'completed']

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['id', 'user', 'referred_user']
