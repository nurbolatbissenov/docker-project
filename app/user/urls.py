from rest_framework.routers import DefaultRouter

from user.views import AuthViewSet, GetViewSet

router = DefaultRouter()

router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'auth', GetViewSet, basename='auth')


urlpatterns = [] + router.urls