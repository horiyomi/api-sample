from django.contrib.auth import get_user_model
from api.apps.accounts.models import Invitation
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for custom user model.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        User = get_user_model()
        model = User
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'full_name',
            'is_verified',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        User = get_user_model()

        # Add username to the objects before creation
        validated_data['username'] = validated_data['email']
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # Ensure that the email and password never get updated this way
        validated_data.pop('email', None)
        validated_data.pop('password', None)
        return super().update(instance, validated_data)

    def get_full_name(self, obj):
        return obj.get_full_name()



class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["id", "first_name", "last_name", "email", "is_active", "invited_by"]
        depth = 1
        extra_kwargs = {
            "id": {"read_only": True},
            "invited_by": {"read_only": True},
            "is_active": {"read_only": True }
        }

    

class AcceptInviteSerializer(serializers.Serializer):
    """ Accept inites serializer """
    password = serializers.CharField()