# djangoba tools

Django + oba = :heart:

tools and patterns by and for me that I use in mostly every django project,
very not production ready.

> PLEASE DO NOT USE

## Features

### Model / PermissionMixinBuilder

`Model` now require to add a `filter_permission` classmethod, or `PermissionMixinBuilder` can allow to declare it outside of the model
the `filter_permission` is made to be used automatically by the `PermissionFilterBackend` FilterBackend and the `FilteredRelatedFieldMixin`

> those two are equivalent

```py
# with method
class Ressource(Model):
    account = ForeignKey(Account)

    @classmethod
    def filter_permission(cls, queryset, user, permission):
        if user.is_superuser:
            return queryset
        return queryset.filter(
          account__in=Account.objects.filter(
            membership__user=user, membership__role__permission=permission
          )
        )


# With builder
def filter_permission(cls, queryset, user, permission):
    return queryset.filter(
      account__in=Account.objects.filter(
        membership__user=user, membership__role__permission=permission
      )
    )

class Ressource(PermissionMixinBuilder(filter_func=filter_permission), Model):
    Account = ForeignKey(Account)
```

Note that the builder automatically allows superuser without additional check, unless built with `bypass_superuser=False`

### PermissionFilterBackend

When applied to a viewset as filter backend (can be applied as a default filter backend), will ensure that the results from a viewset are always filtered to reflect the policies defined in the `djangoba_tools.models.Model`'s `filter_permission` method, construct the permission name from the viewset's action

### ModelSerializer

Serves two purposes:

> prefetch_related

Adds a `prefetch_related` method to the serializer, used automaticallly in `djangoba_tools.views.ModelViewSet`
helps to put a prefetch hook right where we define the way we'll use the model

Can also be nested if using nested serializers,

```py
class RootSerializer(ModelSerializer):
    nested = NestedSerializer()
    class Meta:
        model = RootModel
        fields = [
          'nested'
        ]

    @staticmethod
    def prefetch_related(self, queryset, request, viewset):
        return queryset.prefetch_related(
          'nested', NestedSerializer.prefetch_related(
            NestedModel.objects.all(), request, viewset
          )
        )
```

> FilteredRelatedFieldMixin

by defautl, `ModelSerializer` filters accessible related models with the `djangoba_tools.models.Model`'s permission management

### ViewSets `ModelViewSet` (derived from `BaseViewSet`)

> only works with `djangoba_tools.serializers.ModelSerializer`

Viewsets now override `get_queryset` to call the serializer's `prefetch_related` newly defined method
