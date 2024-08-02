# file: myapp/serializers.py
from rest_framework import serializers
from .models import User, Task

class UserSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'telegram_id', 'tg_username', 'nickname', 'points', 'referral_code', 'referrer', 'avatar', 'referrals']

    def get_referrals(self, obj):
        return UserSerializer(obj.referrals.all(), many=True).data

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'image', 'completed', 'user', 'task_url', 'points']
