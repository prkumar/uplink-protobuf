def get_first_of_type(iterable, type_):  # pragma: no cover
    return next(i for i in iterable if isinstance(i, type_))


def get_values_of_type(iterable, type_):
    return (i for i in iterable if isinstance(i, type_))
