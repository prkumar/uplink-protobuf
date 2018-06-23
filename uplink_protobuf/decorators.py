# Third party imports
from uplink import returns, json

__all__ = ["from_json", "to_json"]


# noinspection PyPep8Naming
class from_json(returns.json):
    _can_be_static = True

    def __init__(self, model=None, member=(), ignore_unknown_fields=False):
        super(from_json, self).__init__(model=model, member=member)
        self._options = {"ignore_unknown_fields": ignore_unknown_fields}

    @property
    def options(self):
        return self._options.copy()


# noinspection PyPep8Naming
class to_json(json):
    _can_be_static = True

    def __init__(
        self,
        including_default_value_fields=False,
        preserving_proto_field_name=False,
        use_integers_for_enums=False,
    ):
        super(to_json, self).__init__()
        self._options = {
            "including_default_value_fields": including_default_value_fields,
            "preserving_proto_field_name": preserving_proto_field_name,
            "use_integers_for_enums": use_integers_for_enums,
        }

    @property
    def options(self):
        return self._options.copy()
