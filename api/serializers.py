from rest_framework import serializers

class ReadFileSerializer(serializers.Serializer):
    setup = serializers.FileField()
    email = serializers.FileField()