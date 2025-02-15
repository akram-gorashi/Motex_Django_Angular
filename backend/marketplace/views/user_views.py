from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from marketplace.models import CustomUser
from marketplace.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  #   Require authentication for user management

    @action(detail=False, methods=['GET'])
    def me(self, request):
        """  Get the current authenticated user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
