from rest_framework import serializers

from test_app.models import Url


class UrlSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(read_only=True)
    short_url = serializers.CharField(read_only=True)

    class Meta:
        model = Url
        fields = ["id", "default_url", "short_url", "user_id", "views"]


class UrlListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ["id", "short_url"]
