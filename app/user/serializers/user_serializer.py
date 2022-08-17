from rest_framework import serializers
from user.models import CustomUser
from django.core.mail import send_mail

from user.tasks import custom_send_mail


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'email', 'username', 'user_role'

        def create(self, validated_data):
            user = CustomUser.objects.create_user(validated_data['email', 'username', 'user_role', 'password'], None)
            return user


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'email', 'username', 'password'

    def verify_email(self):
        if self.validated_data.get('email'):
            custom_send_mail(self.validated_data.get('email'))

    # def custom_send_mail(self):
    #     send_mail(
    #         'Assalamu aleykum',
    #         'Here is the message.',
    #         'from@example.com',
    #         #[email]
    #         #['a.jigitekov@gmail.com']
    #         ['nurbolatbissenov@gmail.com'],
    #     )



class CustomUserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
