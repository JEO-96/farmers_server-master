from rest_framework import viewsets, permissions, generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .models import User
from .serializers import UserSerializer, UserRegisterSerializer


class UserRegisterView(CreateAPIView):

    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserRegisterSerializer(data=data)

        if serializer.is_valid(raise_exception=True):

            user = serializer.save(request.data)

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)

            token = jwt_encode_handler(payload)

            res = {'phone': data['phone'], 'name': data['name'], 'token': token}
            return Response(res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(generics.RetrieveAPIView):

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
