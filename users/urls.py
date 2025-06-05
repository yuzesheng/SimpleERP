from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import RegisterView, CurrentUserView, check_email_exists, send_change_password_email_code, \
    change_password_via_email, change_password_logged_in, UserAdminViewSet

router = DefaultRouter()
router.register('admin',UserAdminViewSet,basename='user-admin')
urlpatterns = [
    path('register/',RegisterView.as_view(),name = 'register'),
    path('login/',TokenObtainPairView.as_view(),name = 'token_obtain_pair'),#登录
    path('token/refresh/',TokenRefreshView.as_view(),name = 'token_refresh'),#刷新
    path('me/',CurrentUserView.as_view(),name = 'current_user'),#获取当前用户信息
    path('check_email/', check_email_exists),
    path('send_reset_code/',send_change_password_email_code),
    path('reset_password_unauthenticated/', change_password_via_email),
    path('reset_password_authenticated/', change_password_logged_in),
    path('',include(router.urls))
]