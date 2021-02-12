import sys


def logger(function=None, *, verbose=['end'], file=sys.stdout):
    '''logger decorator
    verbose (start|exception|end)[data]
    '''

    verbose = set(verbose)

    def wrapper(f):
        def check(a, b):
            assert isinstance(b, set)
            a = set([a]).union({'all'})
            return not a.isdisjoint(b)

        name = f.__name__[:10].center(10)

        def _wrapper(*args, **kwargs):
            if check('start', verbose):
                print(f'[{name}] start', file=file)

            try:
                res = f(*args, **kwargs)
            except Exception as e:
                if check('exception', verbose):
                    print(f'[{name}] exception', file=file)
                raise e

            if check('end', verbose):
                print(f'[{name}] end', file=file)

            return res

        return _wrapper

    if callable(function):
        return wrapper(function)
    else:
        return wrapper


def inject(c=None, *, verbose=['end'], file=sys.stdout):
    def _inject(obj):
        for method_name in dir(obj):
            method = getattr(obj, method_name)
            if callable(method) and not method_name.startswith('_'):
                setattr(obj, method_name, logger(
                    method, verbose=verbose, file=file))

    def wrapper_class(*args, **kwargs):
        o = c(*args, **kwargs)
        _inject(o)
        return o

    def wrapper(c):
        def _wrapper_class(*args, **kwargs):
            o = c(*args, **kwargs)
            _inject(o)
            return o
        return _wrapper_class

    if isinstance(c, type):  # class
        return wrapper_class
    elif c is not None:  # inject(obj)
        _inject(c)
        return c
    else:  # class + params
        return wrapper
