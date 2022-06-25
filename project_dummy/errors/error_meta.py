from typing import Tuple, Dict, Any, Union


class ErrorMeta(type):

    def __new__(mcs, name: str, bases: Tuple, attrs: Dict[str, Any]):
        if name == 'BaseError':
            return type.__new__(mcs, name, bases, attrs)
        __error_mapper__ = dict()
        for k, v in attrs.items():
            if isinstance(v, ErrorField):
                __error_mapper__[k] = v
        # for k in __error_mapper__.keys():
        #     attrs.pop(k)
        attrs['__error_mapper__'] = __error_mapper__
        return type.__new__(mcs, name, bases, attrs)


class ErrorField:

    __slots__ = ['error_code', 'error_type', 'message']

    def __init__(self, code: int, error_type: str, message: str):
        self.error_code = code
        self.error_type = error_type
        self.message = message

    def __repr__(self):
        return f"Error({self.error_code}, '{self.error_type}', '{self.message}')"


class BaseError(dict, metaclass=ErrorMeta):

    @classmethod
    def get(cls, error_type: str):
        for k, v in cls.__error_mapper__.items():
            if v.error_type == error_type:
                return v
        return None


class SerializedException(Exception):
    LETTER_CASE = "camel"
    RESULT_KEY = "result"
    RESULT_TYPE = dict
    TRACEBACK = True
    DEFAULT_ERROR = BaseError

    def __init__(self, error_type: Union[str, ErrorField], exc):
        self._exc = exc
        if isinstance(error_type, ErrorField):
            self._error = error_type
        else:
            self._error = self.DEFAULT_ERROR.get(error_type)

    def serialize(self):
        if self.LETTER_CASE == 'snake':
            error_detail = {
                'error_code': self._error.error_code,
                'error_message': self._error.message
            }
        elif self.LETTER_CASE == 'camel':
            error_detail = {
                'errorCode': self._error.error_code,
                'errorMessage': self._error.message
            }
        else:
            error_detail = {
                'code': self._error.error_code,
                'message': self._error.message
            }
        error_detail[self.RESULT_KEY] = self.RESULT_TYPE()
        if self.TRACEBACK:
            import traceback
            error_detail['traceback'] = '\n'.join(traceback.format_exception(type(self._exc), self._exc, self._exc.__traceback__))
        return error_detail

    @classmethod
    def configure(cls,
                  error_cls=BaseError,
                  *,
                  letter_case='camel',
                  result_key='result',
                  result_type=dict,
                  traceback=True):
        cls.DEFAULT_ERROR = error_cls
        assert letter_case in ['short', 'snake', 'camel']
        cls.LETTER_CASE = letter_case
        assert result_key in ['result', 'data']
        cls.RESULT_KEY = result_key
        assert result_type in [list, dict]
        cls.RESULT_TYPE = result_type
        cls.TRACEBACK = traceback
