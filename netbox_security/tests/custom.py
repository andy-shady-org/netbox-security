import importlib
import inspect

from utilities.testing.api import APITestCase as NetBoxAPITestCase
from utilities.testing.views import ModelViewTestCase as NetBoxModelViewTestCase
from django.urls import reverse
from django.utils.module_loading import import_string
from netbox.api.exceptions import GraphQLTypeNotFound
import strawberry_django
from strawberry.types.base import StrawberryList, StrawberryOptional
from strawberry.types.union import StrawberryUnion
from strawberry.types.lazy_type import LazyType
from ipam.graphql.types import IPAddressFamilyType


def get_graphql_type_for_model(model):
    app_label, model_name = model._meta.label.split(".")
    class_name = f"{app_label}.graphql.types.NetBoxSecurity{model_name}Type"
    try:
        return import_string(class_name)
    except ImportError:
        raise GraphQLTypeNotFound(
            f"Could not find GraphQL type for {app_label}.{model_name}"
        )


class NetBoxSecurityGraphQLMixin:
    def _get_graphql_base_name(self):
        base_name = self.model._meta.verbose_name.lower().replace(" ", "")
        return getattr(self, "graphql_base_name", f"netbox_security_{base_name}")

    def _build_query_with_filter(self, name, filter_string):
        """
        Called by either _build_query or _build_filtered_query - construct the actual
        query given a name and filter string
        """
        type_class = get_graphql_type_for_model(self.model)

        # Compile list of fields to include
        fields_string = ""

        file_fields = (
            strawberry_django.fields.types.DjangoFileType,
            strawberry_django.fields.types.DjangoImageType,
        )
        for field in type_class.__strawberry_definition__.fields:
            if field.type in file_fields or (
                type(field.type) is StrawberryOptional
                and field.type.of_type in file_fields
            ):
                # image / file fields nullable or not...
                fields_string += f"{field.name} {{ name }}\n"
            elif (
                type(field.type) is StrawberryList
                and type(field.type.of_type) is LazyType
            ):
                # List of related objects (queryset)
                fields_string += f"{field.name} {{ id }}\n"
            elif (
                type(field.type) is StrawberryList
                and type(field.type.of_type) is StrawberryUnion
            ):
                # this would require a fragment query
                continue
            elif type(field.type) is StrawberryUnion:
                # this would require a fragment query
                continue
            elif (
                type(field.type) is StrawberryOptional
                and type(field.type.of_type) is StrawberryUnion
            ):
                # this would require a fragment query
                continue
            elif (
                type(field.type) is StrawberryOptional
                and type(field.type.of_type) is LazyType
            ):
                fields_string += f"{field.name} {{ id }}\n"
            elif hasattr(field, "is_relation") and field.is_relation:
                # Ignore private fields
                if field.name.startswith("_"):
                    continue
                # Note: StrawberryField types do not have is_relation
                fields_string += f"{field.name} {{ id }}\n"
            elif inspect.isclass(field.type) and issubclass(
                field.type, IPAddressFamilyType
            ):
                fields_string += f"{field.name} {{ value, label }}\n"
            else:
                fields_string += f"{field.name}\n"

        return f"""
        {{
            {name}{filter_string} {{
                {fields_string}
            }}
        }}
        """

    def _graphql_type_exposes_id(self):
        """
        Return True when the model's GraphQL type exposes ``id`` as a
        queryable selection. Some NetBox types (e.g. Notification,
        Subscription) omit ``id`` from the output type; for those, the
        assertion path falls back to length-only comparison.
        """
        type_class = get_graphql_type_for_model(self.model)
        strawberry_definition = getattr(type_class, "__strawberry_definition__", None)
        if strawberry_definition is None:
            return False
        return any(field.name == "id" for field in strawberry_definition.fields)

    def _get_model_graphql_filter_class(self, model=None):
        model = model or self.model
        module_path = f"{model._meta.app_label}.graphql.filters"
        class_name = f"NetBoxSecurity{model.__name__}Filter"

        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError as exc:
            if exc.name == module_path or module_path.startswith(f"{exc.name}."):
                return None
            raise

        return getattr(module, class_name, None)


class ModelViewTestCase(NetBoxModelViewTestCase):
    def _get_base_url(self):
        return (
            f"plugins:{self.model._meta.app_label}:{self.model._meta.model_name}_{{}}"
        )


class APITestCase(NetBoxAPITestCase):
    def _get_detail_url(self, instance):
        viewname = f"plugins-api:{self._get_view_namespace()}:{instance._meta.model_name}-detail"
        return reverse(viewname, kwargs={"pk": instance.pk})

    def _get_list_url(self):
        viewname = f"plugins-api:{self._get_view_namespace()}:{self.model._meta.model_name}-list"
        return reverse(viewname)
