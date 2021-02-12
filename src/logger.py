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
        for attr in dir(obj):
            if callable(getattr(obj, attr)) and not attr.startswith('_'):
                setattr(obj, attr, logger(
                    getattr(obj, attr), verbose=verbose, file=file))
                if check('inject', verbose):
                    print(f'injected "{attr}" in "{obj.__class__.__name__}"')

    def wrapper_class(*args, **kwargs):
        for attr in c.__dict__:
            if callable(getattr(c, attr)):
                setattr(c, attr, logger(getattr(c, attr)))
                if check('inject', verbose):
                    print(f'injected "{attr}" in "{c.__name__}"')
        o = c(*args, **kwargs)
        return o

    def wrapper(c):
        def _wrapper_class(*args, **kwargs):
            for attr in c.__dict__:
                if callable(getattr(c, attr)):
                    setattr(c, attr, logger(getattr(c, attr)))
                    if check('inject', verbose):
                        print(f'injected "{attr}" in "{c.__name__}"')
            o = c(*args, **kwargs)
            return o
        return _wrapper_class

    if isinstance(c, type):  # class
        return wrapper_class
    elif c is not None:  # inject(obj)
        _inject(c)
        return c
    else:  # class + params
        return wrapper
