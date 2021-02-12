from src.logger import inject


def test_class_base():
    @inject
    class Test1:
        def __init__(self, x, y):
            self.x = 0

        def inc1(self):
            self.x += 1

    t1 = Test1(1, 2)
    t1.inc1()


def test_class_args():
    @inject(verbose=['all'])
    class Test2:
        def __init__(self, x, y):
            self.x = 0

        def inc2(self):
            self.x += 1

    t2 = Test2(1, 2)
    t2.inc2()


def test_obj():
    class Test3:
        def __init__(self, x, y):
            self.x = 0

        def inc3(self):
            self.x += 1

    t3 = Test3(1, 2)
    t3 = inject(t3, verbose=['all'])
    t3.inc3()
