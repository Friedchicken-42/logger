import sys


def check(a, b):
    b = set(b)
    a = set([a]).union({'all'})
    return not a.isdisjoint(b)


def logger(function=None, *, verbose=['all'], file=sys.stdout):
    '''logger decorator
    verbose (start|exception|end)[data]
    '''

    def wrapper(f):
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


def inject(c=None, *, verbose=['all'], file=sys.stdout):
    def _inject(obj):
        meths = {}

        for attr, function in obj.__class__.__dict__.items():
            if callable(getattr(obj, attr)) and attr != '__init__':
                if check('inject', verbose):
                    print(
                        f'inject "{attr[:10].center(10)}" in "{obj.__class__.__name__[:10].center(10)}"    id: "{id(obj)}"')
                meths[attr] = logger(
                    function=function, verbose=verbose, file=file)

        obj.__class__ = type(obj.__class__.__name__, (obj.__class__,), meths)

    def wrapper(c):
        name = c.__name__[:10].center(10)

        def _wrapper(*args, **kwargs):
            if check('init', verbose):
                print(f'[{name}] init {args, kwargs}', file=file)
            obj = c(*args, **kwargs)
            _inject(obj)
            return obj

        return _wrapper

    if isinstance(c, type):  # class
        return wrapper(c)
    elif c is not None:  # inject(obj)
        _inject(c)
        return c
    else:  # class + params
        return wrapper
