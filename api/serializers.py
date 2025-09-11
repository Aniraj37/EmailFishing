from rest_framework import serializers
from .models import FailureEmail
class ReadFileSerializer(serializers.Serializer):
    setup = serializers.FileField()
    email = serializers.FileField()


class FailureEmailSerializer(serializers.ModelSerializer):
    email_file = serializers.FileField(source="email.email_file", read_only=True)
    setup_file = serializers.FileField(source="email.setup_file", read_only=True )
    email_id = serializers.UUIDField(source="email.id", read_only=True )
    class Meta:
        model = FailureEmail
        fields = [
            "id",
            "email_id",
            "email_file",
            "setup_file",
            "phrase",
            "start_line",
            "segment_lines",
            "matched_segments",
            "total_count",
            "created_at"
        ]


class FailureEmailByIDSerializer(serializers.ModelSerializer):
    email_file = serializers.FileField(source="email.email_file", read_only=True)
    setup_file = serializers.FileField(source="email.setup_file", read_only=True )
    class Meta:
        model = FailureEmail
        fields = [
            "id",
            "email_file",
            "setup_file",
            "phrase",
            "matched_segments",
            "total_count",
            "created_at"
        ]