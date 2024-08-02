from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import User, GlobalTask, UserTaskStatus, Referral
from .serializers import UserTaskStatusSerializer, ReferralSerializer, GlobalTaskSerializer, UserSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserDetail(APIView):
    def get(self, request, telegram_id):
        try:
            user = User.objects.get(telegram_id=telegram_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=404)


class RegisterUser(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        tg_username = request.data.get('tg_username')
        nickname = request.data.get('nickname')
        referral_code = request.data.get('referral_code')
        avatar = request.data.get('avatar')

        # Проверка существования пользователя
        if User.objects.filter(telegram_id=telegram_id).exists():
            return JsonResponse({"error": "User already exists"}, status=400)

        # Создание нового пользователя
        user = User.objects.create(
            telegram_id=telegram_id,
            nickname=nickname
        )

        if avatar:
            user.avatar = avatar

        user.save()

        # Начисление бонусов за реферальный код
        if referral_code:
            try:
                referrer = User.objects.get(referral_code=referral_code)
                # Добавляем обоих пользователей в список друзей
                user.friends.add(referrer)
                referrer.friends.add(user)
                # Начисляем очки обоим пользователям
                referrer.points += 10
                user.points += 10
                referrer.save()
                user.save()
            except User.DoesNotExist:
                pass

        # Генерация JWT токенов
        refresh = RefreshToken.for_user(user)

        # Возвращаем данные о пользователе и токены
        return JsonResponse({
            "user": UserSerializer(user).data,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        })


class UserTasks(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        try:
            user = User.objects.get(id=user_id)

            # Создаем записи в UserTaskStatus, если они отсутствуют
            for global_task in GlobalTask.objects.all():
                UserTaskStatus.objects.get_or_create(user=user, task=global_task)

            # Получаем все UserTaskStatus для пользователя
            user_tasks = UserTaskStatus.objects.filter(user=user)
            serializer = UserTaskStatusSerializer(user_tasks, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class CompleteTask(APIView):
    def post(self, request, task_id):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            task_status = UserTaskStatus.objects.get(user=user, task_id=task_id)
            if not task_status.completed:
                task_status.completed = True
                task_status.save()

                # Начисляем очки за выполненную задачу
                user.points += task_status.task.points
                user.save()

                return Response({"status": "task completed", "points": user.points}, status=status.HTTP_200_OK)
            return Response({"error": "Task already completed"}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, UserTaskStatus.DoesNotExist):
            return Response({"error": "Task or User not found"}, status=status.HTTP_404_NOT_FOUND)


class StartFarming(APIView):
    def patch(self, request, telegram_id):
        try:
            user = User.objects.get(telegram_id=telegram_id)
            user.start_farming = True
            user.save()
            return Response({'status': 'farming started'})
        except User.DoesNotExist:
            return Response(status=404)

class ClaimRewards(APIView):
    def patch(self, request, telegram_id):
        try:
            user = User.objects.get(telegram_id=telegram_id)
            user.points += 100  # Пример начисления очков
            user.save()
            return Response({'status': 'points claimed', 'points': user.points})
        except User.DoesNotExist:
            return Response(status=404)

class CreateGlobalTask(APIView):
    def post(self, request):
        serializer = GlobalTaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(GlobalTaskSerializer(task).data, status=201)
        return Response(serializer.errors, status=400)