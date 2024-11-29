from django.db import models


class PermissionedModelMixin:
    @classmethod
    def filter_permission(cls, queryset, user, permission):
        raise NotImplementedError(f"{cls} needs to implement `filter_permission`")


class QuerySet(models.QuerySet):
    def has_permission(self, user, permission):
        if not issubclass(self.model, PermissionedModelMixin):
            raise NotImplementedError(
                f"{self.model} needs to implement {PermissionedModelMixin}"
            )
        return self.model.filter_permission(self, user, permission)


class Model(models.Model, PermissionedModelMixin):
    objects = QuerySet.as_manager()

    class Meta:
        abstract = True


def PermissionMixinBuilder(
    filter_func=lambda queryset, user, permission: queryset,
    bypass_supseruser=False,
):
    class PermissionMixin(PermissionedModelMixin):
        @classmethod
        def filter_permission(cls, queryset, user, permission):
            if not bypass_supseruser and user.is_superuser:
                return queryset
            return filter_func(cls, queryset, user, permission)

    return PermissionMixin


SuperUserOnlyPermissionMixin = PermissionMixinBuilder(
    filter_func=lambda queryset, user, permission: queryset.none()
)
