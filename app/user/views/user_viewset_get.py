from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.filters import UserFilters
from user.serializers import CustomUserSerializer, CustomUserGetSerializer

from user.models import CustomUser
from user.permissions import IsOwnerOrReadOnly


class GetViewSet(viewsets.GenericViewSet):
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = UserFilters

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == 'filter':
            serializer_class = CustomUserGetSerializer
        return serializer_class

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.action == 'filter':
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    @action(methods=['get'], detail=False, url_path='filter')
    def get_user(self, request, *args, **kwargs):
        filtered_queryset = self.filter_queryset(self.queryset.all())
        serializer = self.get_serializer(filtered_queryset, many=True)

        return Response(serializer.data)
