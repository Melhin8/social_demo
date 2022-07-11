from django.db.utils import IntegrityError
from rest_framework import serializers


class AutofillAuthorMixin:
    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError('You can like post only once!')
