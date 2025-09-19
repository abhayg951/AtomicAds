from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AlertViewSet, UserAlertsViewSet

router = DefaultRouter()
router.register(r'alerts', AlertViewSet, basename='alert')

user_alerts = UserAlertsViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path('', include(router.urls)),
    # user alert endpoints:
    path('users/<int:user_id>/alerts/', UserAlertsViewSet.as_view({'get':'list'}), name='user-alerts'),
    path('users/<int:user_id>/alerts/<int:pk>/snooze/', UserAlertsViewSet.as_view({'post':'snooze'}), name='user-snooze'),
    path('users/<int:user_id>/alerts/<int:pk>/mark_read/', UserAlertsViewSet.as_view({'post':'mark_read'}), name='user-mark-read'),
    path('users/<int:user_id>/alerts/<int:pk>/mark_unread/', UserAlertsViewSet.as_view({'post':'mark_unread'}), name='user-mark-unread'),
]
