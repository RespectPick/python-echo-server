import zlib
from functools import wraps


def compression_middleware(func):
    @wraps(func)
    def wrapper(raw_request, *args, **kwargs):
        bytes_request = zlib.decompress(raw_request)
        bytes_response = func(bytes_request, *args, **kwargs)
        return zlib.compress(bytes_response)
    return wrapper
