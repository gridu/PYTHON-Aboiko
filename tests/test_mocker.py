# from pytest_mock import mocker


def adder(a, b):
    return a + b


def fun(a, b):
    if adder(a, b) == 5:
        return "passed"
    else:
        return "failed"


def test_fun(mocker):
    mocker.patch("tests.test_mocker.adder", return_value=5)
    assert fun(4, 2) == "passed"
