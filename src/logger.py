from typing import List


class Logger:

    def __init__(self, custom_levels: List[str] = []):
        self.levels = ['critical', 'error', 'warning', 'info', 'debug']
        self.levels.extend(custom_levels)
        self.lenght = max(len(i) for i in self.levels)

    def log(self, function=None, level='warning', verbose=1):
        level = level.ljust(self.lenght)

        def wrapper(f):
            def wrapper_function(*args, **kwargs):
                name = f.__name__

                if verbose > 1:
                    print(f'[{level}] | [{name}] call')

                f(*args, **kwargs)

                if verbose:
                    print(f'[{level}] | [{name}] end')

            return wrapper_function

        if callable(function):
            return wrapper(function)
        return wrapper
