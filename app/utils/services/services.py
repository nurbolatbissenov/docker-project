from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token


def auth_custom_user(email: str, password: str):
    data = {
        'username': email,
        'password': password
    }
    serializer = AuthTokenSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('user')
    user_token = Token.objects.get(user=user)
    return user, user_token.key


def delete_tokens(user: Token, token: str, all: bool):
    try:
        if all:
            Token.objects.filter(user=user).delete()
        else:
            Token.objects.filter(user=user, key=token).delete()
    except:
        raise ValidationError("ERROR: User's tokens not found!")
