from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, LoginViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='login'),
]
