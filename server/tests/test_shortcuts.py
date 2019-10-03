import pytest

from datetime import datetime

from protocol import make_200, make_400, make_404, make_500


@pytest.fixture
def code_200():
    return 200

@pytest.fixture
def code_400():
    return 400

@pytest.fixture
def code_404():
    return 404

@pytest.fixture
def code_500():
    return 500

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


def test_make_200(initial_request, code_200, expected_data, expected_time):
    response = make_200(initial_request, expected_data, date=expected_time)
    assert response.get('code') == code_200


def test_make_400(initial_request, code_400, expected_data, expected_time):
    response = make_400(initial_request, expected_data, date=expected_time)
    assert response.get('code') == code_400


def test_make_404(initial_request, code_404, expected_time):
    response = make_404(initial_request, date=expected_time)
    assert response.get('code') == code_404


def test_make_500(initial_request, code_500, expected_time):
    response = make_500(initial_request, date=expected_time)
    assert response.get('code') == code_500