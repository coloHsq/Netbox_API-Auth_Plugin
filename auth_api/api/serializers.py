from rest_framework import serializers
from rest_framework.exceptions import ParseError


class KeyExchangeSerializer(serializers.Serializer):

    public_key = serializers.CharField()

    def validate(self, attrs):
        public_key = attrs.get('public_key')
        attrs['public_key'] = public_key
        return attrs


class ApiLoginSerializer(serializers.Serializer):
    encrypted_data = serializers.CharField()
    session_id = serializers.CharField()

    def validate(self, attrs):
        if attrs is None:
            raise ParseError(detail='Empty request')
        if not attrs.get('encrypted_data'):
            raise ParseError(detail='Missing credentials')
        if not attrs.get('session_id'):
            raise ParseError(detail='Missing session')
        return attrs
