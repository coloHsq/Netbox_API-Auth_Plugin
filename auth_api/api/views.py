from django.contrib.auth import authenticate
from rest_framework import parsers, renderers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Token
from . import serializers
from . import crypto_manager


class KeyExchangeView(APIView):
    """
        endpoint that accept a public RSA key (POST method), used to encrypt, and then send back, AES key and nonce,
        used in clients to encrypt login credentials.
    """
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = serializers.KeyExchangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        public_key = serializer.validated_data['public_key']
        encrypted_data, session_id = crypto_manager.encrypt(public_key)
        return Response({'encrypted_data': encrypted_data, 'session_id': session_id})


class ApiLoginView(ObtainAuthToken):

    serializer_class = serializers.ApiLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        username, password, expires = crypto_manager.decrypt_credentials(
            serializer.validated_data['encrypted_data'],
            serializer.validated_data['session_id']
        )
        user = authenticate(request=request, username=username, password=password)
        if user is None:
            raise AuthenticationFailed(detail="Wrong username or password")
        # remove all expired tokens
        for token in Token.objects.filter(user=user):
            if token.is_expired:
                token.delete()
        token, created = Token.objects.get_or_create(user=user, expires=expires)
        return Response({'token': token.key})
