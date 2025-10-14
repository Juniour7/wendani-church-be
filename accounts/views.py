from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, ChangePasswordSerializer, ElderCreateSerializer

User = get_user_model()



# --------LOGIN ENPOINT -------
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error" : "Invalid credentials entered"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.check_password(password):
        return Response({"error" " 'Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'role': user.role,
        'full_name': user.full_name,
        'must_change_password': user.must_change_password
    })


# -----GET CURRENT USER INFORMATION----------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# -------CHANGE PASSWORD ENPOINT----------

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user
    old_password = serializer.validated_data['old_password']
    new_password = serializer.validated_data['new_password']

    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.must_change_password = False
    user.save()

    return Response({'message': 'Password changed successfully'})


# -------SUPERUSER CREATES AN ELDER ACCOUNT-----

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_elder_view(request):
    serializer = ElderCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
