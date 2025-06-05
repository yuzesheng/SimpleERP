from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserRegisterSerializer, UserSerializer
from utils.email_utils import send_password_change_code

# Create your views here.
#注册
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_email_exists(request):
    email = request.query_params.get('email')
    exists = User.objects.filter(email = email).exists()
    return  Response({'exists':exists})


@api_view(['POST'])
@permission_classes([AllowAny])
def send_change_password_email_code(request):
    email  = request.data.get('email')
    if not email:
        return Response({'error':'邮箱不能为空'},status=400)
    try:
        send_password_change_code(email)
        return Response({'message':'验证码已发送到邮箱，请注意查收'})
    except ValueError as e:
        return  Response({'error':str(e)},status=429)

#登陆用户修改密码
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_logged_in(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if not user.check_password(old_password):
        return Response({'detail':'旧密码错误'},status=400)
    user.set_password(new_password)
    user.save()
    return Response({'detail':'密码修改成功,请重新登录'},status=200)

#未登录用户修改密码
@api_view(['POST'])
@permission_classes([AllowAny])
def change_password_via_email(request):
    email = request.data.get('email')
    code = request.data.get('code')
    new_password = request.data.get('new_password')
    if not all([email,code,new_password]):
        return Response({'error':'请填写完整信息'},status=400)

    conn = get_redis_connection('default')
    saved_code = conn.get(f'pwd_change:{email}')
    if saved_code is None or saved_code.decode()!= code:
        return Response({'error':'验证码错误或已过期'},status = 400)

    try:
        user = User.objects.get(email = email)
    except User.DoesNotExist:
        return Response({'error':'用户不存在'},status=404)

    user.set_password(new_password)
    user.save()
    conn.delete(f'pwd_change:{email}') #删除验证码
    return  Response({'message':'密码修改成功，请登录'})

class UserAdminViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    #获取用户列表
    def list(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

    #启用/禁用用户
    @action(detail=True,methods=['post'])
    def toggle_active(self,request,pk=None):
        try:
            user = User.objects.get(pk = pk)
        except User.DoesNotExist:
            return Response({'error':'用户不存在'},status=404)
        if user.is_superuser:
            return Response({'error':'超级管理员不能被禁用'},status=400)
        user.is_active = not user.is_active
        user.save()
        status_str = '启用' if user.is_active else '禁用'
        return Response({'message':f'{user.username}已{status_str}'},status=200)









