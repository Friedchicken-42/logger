from src.logger import Logger


logger = Logger()


def test_obj():
    class Test:
        def __init__(self):
            self.x = 0

        def inc(self):
            self.x += 1
            return 42

    test = Test()
    logger.inject(test, 2)
    test.inc()
