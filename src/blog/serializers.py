from rest_framework import serializers


class SingleArticleSerializer(serializers.Serializer):
    title = serializers.CharField(allow_blank=False, allow_null=False, required=True, max_length=128)
    cover = serializers.CharField(allow_blank=False, allow_null=False, required=True, max_length=256)
    content = serializers.CharField(allow_blank=False, allow_null=False, required=True, max_length=2048)
    created_at = serializers.DateTimeField(required=True, allow_null=False)

class SubmitArticleSerializer(serializers.Serializer):
    title = serializers.CharField(allow_blank=False, allow_null=False, required=True, max_length=128)
    cover = serializers.FileField(required=True, allow_null=False, allow_empty_file=False)
    content = serializers.CharField(allow_blank=False, allow_null=False, required=True, max_length=2048)
    category_id = serializers.IntegerField(allow_null=False, required=True)
    auther_id = serializers.IntegerField(allow_null=False, required=True)
    promote = serializers.BooleanField(required=True, allow_null=False)

class UpdateArticleCoverSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=True, allow_null=False)
    cover = serializers.FileField(required=True, allow_null=False, allow_empty_file=False)

class DeleteArticleSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=True, allow_null=False)
