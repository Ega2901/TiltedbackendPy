# file: myapp/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        ref_code = request.data.get('referral_code')
        referrer = None
        if ref_code:
            referrer = User.objects.filter(referral_code=ref_code).first()

        user = User(
            telegram_id=request.data.get('telegram_id'),
            tg_username=request.data.get('tg_username'),
            nickname=request.data.get('nickname'),
            referrer=referrer
        )

        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='by_telegram_id/(?P<telegram_id>[^/.]+)')
    def by_telegram_id(self, request, telegram_id=None):
        user = User.objects.filter(telegram_id=telegram_id).first()
        if user:
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'], url_path='start_farming')
    def start_farming(self, request, pk=None):
        user = self.get_object()
        # Логика начала фермерства
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='claim_rewards')
    def claim_rewards(self, request, pk=None):
        user = self.get_object()
        # Логика получения наград
        return Response(status=status.HTTP_200_OK)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['post'], url_path='complete')
    def complete_task(self, request, pk=None):
        task = self.get_object()
        if not task.completed:
            task.completed = True
            task.save()
            task.user.points += task.points
            task.user.save()
        return Response(status=status.HTTP_200_OK)
