from abc import ABC, abstractmethod
from .helpers import *


class Action(ABC):
    # TODO add ignore errors
    # TODO add key for passing forward data
    __slots__ = ('_path', '_method',
                 '_input_data', '_output_data',
                 '_success_code', '_failure_code',
                 '_headers', '_body', '_body_type', '_cookies',
                 '_proxies', '_timeout',
                 '_delay', '_retry',
                 '_extra_keys')

    def __init__(self, **kwargs):
        self._path = kwargs.pop('path')
        self._method = set_method(kwargs.pop('method', 'GET'))
        self._input_data = kwargs.pop('input', None)
        self._output_data = None
        self._success_code, self._failure_code = set_code_defaults_kwargs(kwargs)
        self._headers = kwargs.pop('headers', None)
        self._body = kwargs.pop('body', {})
        self._body_type = kwargs.pop('body_type', None)
        self._cookies = kwargs.pop('cookies', None)
        self._proxies = kwargs.pop('proxies', None)
        self._timeout = kwargs.pop('timeout', None)
        self._delay = kwargs.pop('delay', 0)
        self._retry = kwargs.pop('retry', 0)
        self._extra_keys = kwargs

    @property
    # @abstractmethod
    def path(self):
        return self._path

    @property
    def method(self):
        return self._method

    @property
    def input_data(self):
        return self._input_data

    @property
    def output_data(self):
        return self._output_data

    @output_data.setter
    def output_data(self, json):
        self._output_data = json

    @property
    def success_code(self):
        return self._success_code

    @property
    def failure_code(self):
        return self._failure_code

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body

    @property
    def body_type(self):
        return self._body_type

    @property
    def cookies(self):
        return self._cookies

    @property
    def delay(self):
        return self._delay

    @property
    def debug(self):
        return {k[1:]: getattr(self, k) for k in self.__slots__ if k not in ['_extra_keys']}


class Call(Action):  # TODO add expose param?
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def path(self):
        return


# TODO Implement and add subclasses or parameters if, elif, else based on success or failure code as booleans
class Conditional:
    pass


# TODO Use mapping for paths to call
class Switch:
    pass


# TODO Do all requests asynchronously and gather the results
class PartyLine:
    pass


# TODO Allows to parse JSON objects in a simple way to prepare data and structure for next call
class Parse:
    pass


# TODO Set/save variables to be available for the whole run
class Pager:
    pass
