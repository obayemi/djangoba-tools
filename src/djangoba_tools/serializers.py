from rest_framework import serializers
from rest_framework.relations import RelatedField

from .models import QuerySet


class FiltererdRelatedFieldMixin(RelatedField):
    def __init__(self, permission=None, **kwargs):
        super().__init__(**kwargs)
        self.permission = permission or self.generate_permission()

    def generate_permission(self):
        queryset = self.get_queryset()
        if queryset is None:
            return None

        return f"view_{queryset.model._meta.model_name}"

    def get_queryset(self):
        request = self.context.get("request")
        queryset = super().get_queryset()

        if not isinstance(queryset, QuerySet) or queryset is None:
            raise NotImplementedError(
                f"{queryset} needs to implement djangoba_tools.QuerySet"
            )

        if not request:
            return queryset

        return queryset.has_permission(request.user, self.permission)


class FilteredRelatedField(
    FiltererdRelatedFieldMixin,
    serializers.PrimaryKeyRelatedField,
):
    pass


class FilteredSlugRelatedField(
    FiltererdRelatedFieldMixin,
    serializers.SlugRelatedField,
):
    pass


class ModelSerializer(serializers.ModelSerializer):
    serializer_related_field = FilteredRelatedField

    @staticmethod
    def prefetch_related(queryset, request, viewset):
        return queryset
