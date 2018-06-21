# Third party imports
from uplink import decorators, returns, json

__all__ = ["protobuf"]


class _FromJson(returns.json):
    _can_be_static = True

    def __init__(self, model=None, member=(), ignore_unknown_fields=False):
        super(_FromJson, self).__init__(model, member)
        self._options = {
            "ignore_unknown_fields": ignore_unknown_fields,
        }

    @property
    def options(self):
        return self._options.copy()


class _ToJson(json):
    _can_be_static = True

    def __init__(self,
                 including_default_value_fields=False,
                 preserving_proto_field_name=False,
                 use_integers_for_enums=False):
        super(_ToJson, self).__init__()
        self._options = {
            "including_default_value_fields": including_default_value_fields,
            "preserving_proto_field_name": preserving_proto_field_name,
            "use_integers_for_enums": use_integers_for_enums,
        }

    @property
    def options(self):
        return self._options.copy()


# noinspection PyPep8Naming
class protobuf(decorators.MethodAnnotation):
    _can_be_static = True

    def modify_request(self, request_builder):
        pass

    from_json = _FromJson

    send_json = _ToJson
