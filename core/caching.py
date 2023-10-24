import functools
from datetime import datetime, timedelta

from django.core.cache import cache

from core.logging import get_logger

prefix = "func_"
logger = get_logger()


def gen_cache_key(fn):
    """generates caching key for function"""
    return ":".join([prefix, fn.__module__, fn.__name__])


def calc_expiration_date(time_delta: timedelta = None, dt_args=None):
    """
        takes datetime.now(), replaces with dt_args values and adds time_delta
    """
    dt_args = dt_args or {}
    now = datetime.now()
    expiration_dt_args = {
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'microsecond': now.microsecond
    }
    expiration_dt_args.update(dt_args)
    expiration_date = datetime(**expiration_dt_args)
    if time_delta:
        expiration_date = expiration_date + time_delta
    return expiration_date

def is_result_expired(cached_result):
    ts = cached_result['expires']
    if datetime.now() < datetime.fromtimestamp(ts):
        print("returned from cache")
        return cached_result["value"]


def memoize_with_expiration(calc_expiration):
    """
        store results that expires at time calculated with calc_expiration

    """

    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            key = gen_cache_key(fn)
            cached_result = cache.get(key)
            if cached_result is not None:
                print(f"cached result: {cached_result}")
                ts = cached_result['expires']
                if datetime.now() < datetime.fromtimestamp(ts):
                    print("returned from cache")
                    return cached_result["value"]

            result = fn(*args, **kwargs)
            print("create cache")
            cache.set(key, {
                'value': result,
                'expires': calc_expiration().timestamp()
            }, timeout=None)
            return result


        return wrapped

    return wrapper
