from typing import List


class Logger:

    def __init__(self, custom_levels: List[str] = [], size: int = 10):
        self.levels = ['critical', 'error', 'warning', 'info', 'debug']
        self.levels.extend(custom_levels)
        self.lenght = max(len(i) for i in self.levels)
        self.size = size

    def write(self, name, status, mode, extra=None):
        string = '[{name}] | '
        string += '{status} ' if status else ''
        string += '{mode}'
        string += ' > {extra}' if extra else ''
        name = name.ljust(self.size)[: self.size]
        status = status.ljust(self.lenght)

        print(string.format(name=name, status=status, mode=mode, extra=extra))

    def log(self, function=None, level='', verbose=1):
        level = level.upper() if level in self.levels else ''

        def wrapper(f):
            def wrapper_function(*args, **kwargs):
                name = f.__name__

                if verbose > 1:
                    self.write(name, level, 'call')

                value = f(*args, **kwargs)

                if verbose:
                    self.write(name, level, 'end', value)

                return value

            return wrapper_function

        if callable(function):
            return wrapper(function)
        return wrapper

    def __call__(self, function=None, **kwargs):
        return self.log(function=function, **kwargs)
