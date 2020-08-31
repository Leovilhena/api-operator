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
        'code': None,
        'warning': None,
        'error': None,
        'retry': retry,
        'return': True,
    }

    try:
        response = request(
                    method=kwargs.get('method'),
                    url=kwargs.get('path'),
                    **call_kwargs_interface(kwargs)
        )

        if response.status_code in failure_code:
            response_body.update({
                'response': response.json(),
                'code': response.status_code,
                'warning': 'Response code declared in failure_code',
                'return': False
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
            'error': traceback.format_exc()
        })
    except RequestException:
        response_body.update({
            'warning': traceback.format_exc(),
        })
    except json.JSONDecodeError:
        response_body.update({
            'response': response.content or None,
            'code': response.status_code or None,
            'warning': 'Response is not a valid JSON',
            'error': traceback.format_exc()
        })

    if not response_body.get('return') and retry:
        # TODO append errors to a key on each retry
        kwargs['retry'] -= 1
        response_body = call_path(**kwargs)
    elif not response_body.get('return') and not retry:
        response_body.update({
            'warning': 'No more retries',
        })

    _ = response_body.pop('return', None)

    return response_body


def call_kwargs_interface(kwargs):
    return {
        'data': kwargs.get('input_data'),
        'headers': kwargs.get('headers'),
        'timeout': kwargs.get('timeout'),
        'proxies': kwargs.get('proxies'),
        'cookies': kwargs.get('cookies')
    }
