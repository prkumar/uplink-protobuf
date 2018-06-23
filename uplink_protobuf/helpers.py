def get_first_of_type(iterable, type_):
    return next(i for i in iterable if isinstance(i, type_))


def has_value_of_type(iterable, type_):
    return any(isinstance(i, type_) for i in iterable)
