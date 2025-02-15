from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

#   Fix Register View to Use CustomUser
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()  #   Use CustomUser queryset
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully!"
        }, status=status.HTTP_201_CREATED)
