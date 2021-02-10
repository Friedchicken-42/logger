from src.logger import Logger


def test_args():
    logger = Logger(['testing'], 20)

    @logger.log(level='testing')
    def func(n):
        return n * 2

    func(21)
