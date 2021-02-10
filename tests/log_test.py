from src.logger import Logger


def test_standard():
    logger = Logger()

    @logger.log
    def x(n):
        print(f'n : {n}')

    x(3)


def test_parameterized():
    logger = Logger()

    @logger.log(level='error')
    def x(n):
        print(f'n : {n}')

    x(3)
