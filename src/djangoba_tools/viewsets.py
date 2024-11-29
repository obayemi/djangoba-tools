from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)


class BaseViewSet(viewsets.GenericViewSet):
    def get_queryset(self):
        return self.get_serializer_class().prefetch_related(
            super().get_queryset(), self.request, self
        )


class ReadonlyViewSet(
    BaseViewSet,
    ListModelMixin,
    RetrieveModelMixin,
):
    pass


class ModelViewSet(
    BaseViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    pass
