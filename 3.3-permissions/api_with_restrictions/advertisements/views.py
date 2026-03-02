from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, FavoriteAdvertisement
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.exclude(status='DRAFT')
        elif not self.request.user.is_staff:
            queryset = queryset.filter(
                models.Q(status='OPEN') |
                models.Q(status='CLOSED') |
                models.Q(status='DRAFT', creator=self.request.user)
            )
        return queryset

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        elif self.action in ["toggle_favorite"]:
            return [IsAuthenticated()]
        return []

    def get_throttles(self):
        """Настройка лимитов запросов."""
        if self.request.user.is_authenticated:
            self.throttle_classes = [UserRateThrottle]
        else:
            self.throttle_classes = [AnonRateThrottle]
        return super().get_throttles()

    def perform_create(self, serializer):
        """Создание объявления с проверкой лимита открытых объявлений."""
        user = self.request.user
        open_ads_count = Advertisement.objects.filter(creator=user, status='OPEN').count()
        if open_ads_count >= 10:
            raise serializers.ValidationError(
                "У вас уже 10 открытых объявлений. Закройте некоторые перед созданием новых.")
        serializer.save(creator=user)

    def destroy(self, request, *args, **kwargs):
        """Удаление объявления с проверкой прав."""
        instance = self.get_object()
        if instance.creator != request.user and not request.user.is_staff:
            return Response(
                {"detail": "Вы не можете удалить это объявление."},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'])
    def toggle_favorite(self, request, pk=None):
        ad = self.get_object()
        user = request.user

        if ad.creator == user:
            return Response(
                {"detail": "Вы не можете добавить свое объявление в избранное."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'POST':
            FavoriteAdvertisement.objects.get_or_create(user=user, advertisement=ad)
            return Response({"status": "added to favorites"}, status=status.HTTP_201_CREATED)
        else:
            FavoriteAdvertisement.objects.filter(user=user, advertisement=ad).delete()
            return Response({"status": "removed from favorites"}, status=status.HTTP_204_NO_CONTENT)
