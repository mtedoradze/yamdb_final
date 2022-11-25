from django.http import JsonResponse
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.permissions import AdminPermission, UserPermission

from .models import User
from .serializers import (CreateUserSerializer, CustomTokenObtainSerializer,
                          UserAdminCreateSerializer, UserSelfUpdateSerializer)


class SignUpView(APIView):
    """Создание нового пользователя"""

    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Получение токена по username и confirmation_code."""

    serializer_class = CustomTokenObtainSerializer
    permission_classes = [permissions.AllowAny]


class UserInfoViewSet(viewsets.ModelViewSet):
    """
    Создание администратором нового пользователя, получение
    пользователя по username.
    """

    queryset = User.objects.all()
    serializer_class = UserAdminCreateSerializer
    permission_classes = [AdminPermission, ]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username',)
    ordering = ('username', )

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            permission_classes=[UserPermission])
    def get_user(self, request):
        """Получение своей страницы по эндпоинту users/me."""

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            if request.user.role == User.USER:
                serializer = UserSelfUpdateSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
