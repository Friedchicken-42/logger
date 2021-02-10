from src.logger import Logger
import pytest

logger = Logger()


def test_exception():
    @logger.log(verbose=2)
    def exception():
        1 / 0
    with pytest.raises(Exception):
        exception()
