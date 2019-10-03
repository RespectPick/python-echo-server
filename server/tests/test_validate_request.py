import pytest

from datetime import datetime

from protocol import validate_request


@pytest.fixture
def valid_request():
    return {
        'action': 'test',
        'time': datetime.now().timestamp(),
        'data': 'some test data'
    }

@pytest.fixture
def invalid_request():
    return {
        'data': 'some test data'
    }


def test_valid_validate_request(valid_request):
    assert validate_request(valid_request)


def test_invalid_validate_request(invalid_request):
    assert validate_request(invalid_request) == False
