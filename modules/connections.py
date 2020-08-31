import sys
import traceback
from requests import request
from requests.exceptions import *
from pprint import pp
import time
import json


def timeit(method):

    def timed(*args, **kwargs):
        star_time = time.time()
        print(f'[*] Calling {kwargs.get("path")}', end='')
        result = method(*args, **kwargs)
        elapsed_time = time.time()
        print(f'\r[*] Calling {kwargs.get("path"):*^100} [{elapsed_time - star_time:.2f}] seconds')
        sys.stdout.flush()
        print(f'[*] Results: ')
        pp(result)
        print('', end="\n\n")
        return result

    return timed


@timeit
def call_path(**kwargs):
    # TODO add delay
    # TODO create error info
    # TODO handle authentication

    success_code = kwargs.get('success_code')
    failure_code = kwargs.get('failure_code')
    retry = kwargs.get('retry', 0)
    response = None

    assert retry >= 0

    response_body = {
        'response': response,
        'code': kwargs.get('code', None),
        'warning': kwargs.get('warning', None),
        'error': kwargs.get('error', None),
        'retry': retry,
        'return': True,
        'exit': False,
    }

    try:
        response = request(
                    url=kwargs.get('path'),
                    **call_kwargs_interface(kwargs)
        )

        if response.status_code in failure_code:
            response_body.update({
                'response': response.json(),
                'code': response.status_code,
                'warning': 'Response code declared in failure_code',
                'return': False,
            })
        elif not success_code or response.status_code in success_code:
            response_body.update({
                'response': response.json(),
                'code': response.status_code,
            })

    except (ConnectTimeout, ReadTimeout):
        response_body.update({
            'return': False,
        })
    except InvalidURL:
        response_body.update({
            'warning': 'URL is invalid',
            'error': traceback.format_exc(),
            'exit': True
        })
    except RequestException:
        response_body.update({
            'warning': traceback.format_exc(),
            'return': False
        })
    except json.JSONDecodeError:
        response_body.update({
            'response': str(response.content, 'utf-8') or None,
            'code': response.status_code or None,
            'warning': 'Response is not a valid JSON',
            'error': traceback.format_exc(),
            'exit': True
        })

    if not response_body['return'] and retry:
        # TODO append errors to a key on each retry
        kwargs['retry'] -= 1
        response_body = call_path(**kwargs)
    elif not response_body['return'] and not retry and not response_body['warning']:
        response_body.update({
            'warning': 'No more retries',
            'exit': True
        })

    _ = response_body.pop('return', None)

    return response_body


def call_kwargs_interface(kwargs):
    return {
        'data': kwargs.get('input_data'),
        'headers': kwargs.get('headers'),
        'timeout': kwargs.get('timeout'),
        'proxies': kwargs.get('proxies'),
        'cookies': kwargs.get('cookies'),
        'method': kwargs.get('method')
    }
