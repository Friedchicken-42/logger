from src.logger import Logger

logger = Logger()


def test_standard():
    @logger.log
    def x(n):
        print(f'n : {n}')

    x(42)


def test_parameterized():
    @logger.log(level='error', verbose=3)
    def x(n):
        print(f'n : {n}')

    x(42)


@logger
def test_call():
    @logger
    def x(n):
        print(f'n : {n}')
        return n
    x(42)


def test_fail():
    @logger
    def x():
        raise Exception
    x()
