from django.contrib.auth import get_user_model
from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from .models import User
import re

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = [
            'id',
            'phone',
            'name',
            'is_active',
        ]


class UserRegisterSerializer(serializers.Serializer):

    phone = serializers.CharField(
        max_length=11,
        min_length=10,
        required=True
    )
    name = serializers.CharField(
        max_length=10,
        min_length=2,
        required=True
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_phone(self, phone):
        if not re.compile(r'010\d{7,8}').match(phone) :
            raise serializers.ValidationError(_("The phone number is not valid"))
        return phone

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def save(self, request):
        phone = request['phone']
        name = request['name']
        password = request['password1']

        user = User.objects.create_user(phone, name)

        user.set_password(password)
        user.save()

        return user
