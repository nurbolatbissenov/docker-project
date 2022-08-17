from django.contrib.auth import logout
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated

from user.models import CustomUser
from user.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from user.serializers import (CustomUserRegisterSerializer,
                              CustomUserSerializer,
                              LoginSerializer)

from utils.services import auth_custom_user, delete_tokens


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == 'login':
            serializer_class = LoginSerializer
        elif self.action == 'register':
            serializer_class = CustomUserRegisterSerializer
        return serializer_class

    def get_permissions(self):
        permissions_classes = self.permission_classes

        if self.action == 'loguot':
            permissions_classes = [AllowAny]

        return [permission() for permission in permissions_classes]

    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, token = auth_custom_user(
            serializer.validated_data.get('email'),
            serializer.validated_data.get('password'),
        )
        response = dict()
        response['user_data'] = CustomUserSerializer(instance=user).data
        response['token'] = token
        return Response(data=response, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='logout')
    def logout(self, request, *args, **kwargs):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split()[1]
            delete_tokens(request.user, token, False)
        except:
            raise ValidationError('ERROR: User not found! Try with another token!')
        logout(request)

        return Response(
            data={'details': 'OK, user token deleted!'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        #serializer = CustomUserRegisterSerializer(data=request.data)
        #serializer.custom_send_mail()
        serializer.is_valid(raise_exception=True)
        serializer.verify_email()
        data = {}
        if serializer.is_valid(raise_exception=True):
            account = serializer.save()
            token = Token.objects.get(user=account).key
            data['response'] = "successfully registered a new user"
            data['email'] = account.email
            data['username'] = account.username
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)
