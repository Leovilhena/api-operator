from typing import TypeVar


def set_method(method: str) -> str:
    available_methods = {'GET', 'HEAD', 'POST', 'PUT', 'DELETE'}
    method = method.upper()

    if method not in available_methods:
        raise NotImplementedError  # TODO create exception

    return method


def set_code_defaults_kwargs(kwargs: dict) -> tuple:
    success_code, failure_code = [], []

    # TODO parse string to list[str]
    # TODO add regex check
    if 'success' in kwargs:
        success_code = get_codes_list(kwargs.pop('success'))
    elif 'failure' in kwargs:
        failure_code = get_codes_list(kwargs.pop('failure'))

    if not isinstance(success_code, list) or not isinstance(failure_code, list):
        raise NotImplementedError(f'Code is not a list {success_code} {failure_code}')  # TODO create Exception

    return success_code, failure_code


def get_codes_list(codes: [str, list]) -> list:
    if isinstance(codes, list):
        return codes
    elif isinstance(codes, str):
        return codes.replace(',', '').split(' ')
    else:
        raise NotImplementedError(f'Bad type for code {type(codes)}')


def check_module_integrity(action_class: TypeVar) -> TypeVar:
    if action_class._extra_keys:
        raise NotImplementedError('Bad argument')  # TODO create Exception class
    else:
        delattr(action_class, '_extra_keys')

    return action_class  # FIXME
