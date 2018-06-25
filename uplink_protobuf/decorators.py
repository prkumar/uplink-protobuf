# Third party imports
from uplink import decorators

__all__ = ["configure_json_response", "configure_json_request"]


# noinspection PyPep8Naming
class configure_json_response(decorators.MethodAnnotation):
    _can_be_static = False

    def __init__(self, ignore_unknown_fields=False, **kwargs):
        self._options = {"ignore_unknown_fields": ignore_unknown_fields}
        self._options.update(kwargs)

    @property
    def options(self):
        return self._options.copy()


# noinspection PyPep8Naming
class configure_json_request(decorators.MethodAnnotation):
    _can_be_static = False

    def __init__(
        self,
        include_default_value_fields=False,
        preserve_proto_field_names=False,
        use_integers_for_enums=False,
        **kwargs
    ):
        self._options = {
            "including_default_value_fields": include_default_value_fields,
            "preserving_proto_field_name": preserve_proto_field_names,
            "use_integers_for_enums": use_integers_for_enums,
        }
        self._options.update(kwargs)

    @property
    def options(self):
        return self._options.copy()
