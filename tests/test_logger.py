from src.logger import logger
import os
import pytest


def test_base():
    @logger
    def func():
        return 42

    assert func() == 42


def test_args():
    @logger
    def func(n):
        return n * 2

    assert func(21) == 42


def test_params():
    @logger(verbose=['all'])
    def func(n):
        return n * 2

    assert func(21) == 42


def test_file():
    f = open('log.txt', 'w')

    @logger(verbose=['all'], file=f)
    def func(n):
        return n * 2

    assert func(21) == 42
    f.close()
    with open('log.txt', 'r') as f:
        assert f.readlines() == ['[   func   ] start\n', '[   func   ] end\n']
    os.remove('log.txt')


def test_exception():
    @logger(verbose=['all'])
    def func():
        1 / 0

    with pytest.raises(Exception):
        func()


def test_block_exception():
    # TODO
    pass
