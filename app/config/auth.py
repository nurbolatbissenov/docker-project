from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError

from user.models import CustomUser


class CustomAuthToken(TokenAuthentication):

    def __init__(self):
        super().__init__()

    model = CustomUser

    def authenticate_credentials(self, key):
        model = self.get_model()
        tokens = model.objects.select_related('user').filter(key=key)

        if tokens.count() == 0:
            raise ValidationError('ERROR: Invalid User TOKEN')

        user_data = tokens[0].user

        if not user_data.is_active:
            raise ValidationError('ERROR: User is not active, pls, contact with support!')

        return (user_data, tokens)
