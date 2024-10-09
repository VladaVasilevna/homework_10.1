import logging

import pytest

from src.decorators import log


@log()
def add(x: int, y: int) -> int:
    return x + y


@log()
def divide(x: int, y: int) -> float:
    return x / y


def test_add_function(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO):
        add(1, 2)

    assert "Calling function: add with args: (1, 2), kwargs: {}" in caplog.text
    assert "add ok, result: 3" in caplog.text


def test_divide_function(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO):
        divide(4, 2)

    assert "Calling function: divide with args: (4, 2), kwargs: {}" in caplog.text
    assert "divide ok, result: 2.0" in caplog.text


def test_divide_by_zero(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    with caplog.at_level(logging.ERROR):
        assert "Calling function: divide with args: (1, 0), kwargs: {}" in caplog.text
        assert "divide error: ZeroDivisionError. Inputs: (1, 0), {}" in caplog.text


if __name__ == "__main__":
    pytest.main()
