import pytest

from datetime import datetime

from protocol import make_response


@pytest.fixture
def expected_code():
    return 200

@pytest.fixture
def expected_action():
    return 'test'

@pytest.fixture
def expected_time():
    return datetime.now().timestamp()

@pytest.fixture
def expected_data():
    return 'some client data'

@pytest.fixture
def initial_request(expected_action, expected_time, expected_data):
    return {
        'action': expected_action,
        'time': expected_time,
        'data': expected_data
    }


def test_action_make_response(initial_request, expected_action, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, date=expected_time)
    action = response.get('action')
    assert action == expected_action


def test_code_make_response(initial_request, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, date=expected_time)
    action = response.get('code')
    assert action == expected_code


def test_time_make_response(initial_request, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, date=expected_time)
    action = response.get('time')
    assert action == expected_time


def test_data_make_response(initial_request, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, date=expected_time)
    action = response.get('data')
    assert action == expected_data


def test_none_request_make_response(expected_code):
    with pytest.raises(AttributeError):
        make_response(None, expected_code)
