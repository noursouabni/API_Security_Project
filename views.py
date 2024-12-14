from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
import logging
logger = logging.getLogger(__name__)
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'is_staff']

    # pour créer un nouveau User
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    # to Update user
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        # Update password ken mawjoud
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance
class IsAdminUserCustom(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
class ProtectedViewJWT(APIView):
    permission_classes = [IsAdminUserCustom]

    def get(self, request):
        return Response({"message": "Seuls les administrateurs peuvent accéder à cette route avec JWT !"})

# View for OAuth2 Authentication
class ProtectedViewOAuth(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAdminUserCustom]

    def get(self, request):
        return Response({"message": "You have access to this protected route with OAuth2!"})

    def get(self, request):
        return Response({"message": f"Hello {request.user}, you are authenticated!"})
class LoginView(APIView):
    permission_classes = []  #  authentication mouch lezma 

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"detail": "Invalid credentials"}, status=401)

# View bch nekhou el Users lkol (GET request)

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] 
# View lel user details (GET request by ID)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserCustom]
    lookup_field = 'id'
    def get_queryset(self):
        logger.info(f"Requesting user with ID: {self.kwargs.get('id')}")
        return super().get_queryset()
    def get(self, request, *args, **kwargs):
        logger.info(f"Authenticated user: {request.user}")
        return super().get(request, *args, **kwargs)

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserCustom]
    lookup_field = 'id'
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "User deleted successfully!"}, status=status.HTTP_200_OK)

# View bch nkaydou user jdid (POST request)
class RegisterUserView(generics.CreateAPIView):
    permission_classes = [IsAdminUserCustom]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
# View lel login w JWT token generation (POST request)
@api_view(['POST'])
def login_user(request):
    from rest_framework_simplejwt.tokens import RefreshToken
    from rest_framework import status

    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.filter(username=username).first()

    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        })

    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def check_admin_status(request):
    # Verifying if the user is authenticated and an admin
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    if request.user.is_staff:
        return Response({"detail": "You are an admin."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "You are not an admin."}, status=status.HTTP_200_OK)

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the API! Please navigate to /admin/ for admin page.")
