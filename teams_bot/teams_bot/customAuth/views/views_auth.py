import json
import logging

from django.utils import timezone
from rest_framework import generics, status, permissions, exceptions
from rest_framework.response import Response

from customAuth.serializers import serializer_user
from customAuth.models.model_user import User
from lib.drf import permissions as lib_drf_permissions

logger = logging.getLogger(__name__)


class AuthLogin(generics.GenericAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):

        # logger.info('Request for login started')
        # logger.info('REQUEST: email - {}'.format(request.data['email']))
        # try:
        request_serializer = serializer_user.LoginFormSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=request_serializer.validated_data['email']).first()

        if user and user.check_password(request_serializer.validated_data['password']):
            user_serializer = serializer_user.UserBaseSerializer(user)
            result = {'user': user_serializer.data}
            # res = get_response(result)
            # logger.info('Request for login finished : SUCCESS')
            return Response(data=result, status=status.HTTP_200_OK)
        else:
            # logger.info('Request for login finished : ERROR')
            raise exceptions.AuthenticationFailed()
            # return Response("Invalid login credentials", status=status.HTTP_401_UNAUTHORIZED)
    # except Exception as e:
    #     return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
