from rest_framework import filters


class PermissionFilterBackend(filters.BaseFilterBackend):
    permission = {}

    def get_permission_action(self, view):
        match view.action:
            case "retrieve":
                return "view"
            case "list":
                return "view"
            case "partial_update":
                return "change"
            case "udate":
                return "change"
            case "destroy":
                return "delete"
            case action:
                return action

    def get_permission(self, request, queryset, view):
        action = self.get_permission_action(view)
        return (
            self.permission.get(action) or f"{action}_{queryset.model._meta.model_name}"
        )

    def filter_queryset(self, request, queryset, view):
        # if not isinstance(queryset.model, SensinovModel):
        # return queryset

        permission = self.get_permission(request, queryset, view)
        return queryset.has_permission(request.user, permission)
