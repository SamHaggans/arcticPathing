import pytest
from arcticpathing import utils

from app import create_app


@pytest.fixture
def client():
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_root(client):
    request = client.get('/')
    assert b'<!DOCTYPE html>' in request.data
    assert b'<title>Arctic Pathing</title>' in request.data
    assert b'Starting Lat: <input type = "text" name = "lat_start">' in request.data


def test_getting_path(client):
    request = client.get('/route?lat_start=80&lon_start=80&lat_end=82&lon_end=82')

    expect_path = [[209, 189], [209, 188],
                   [209, 187], [210, 186],
                   [210, 185], [211, 184],
                   [212, 183], [212, 182]]

    assert request.get_json()['path'] == expect_path
    # Extract value from the pint tuples for distance and straight_distance
    path_distance = request.get_json()['path_distance'][0]
    straight_distance = request.get_json()['straight_distance'][0]
    assert utils.float_is_equal(request.get_json()['path_difficulty'], 75.6238140960203)
    assert utils.float_is_equal(path_distance, 241.421)
    assert utils.float_is_equal(straight_distance, 223.607)


def test_getting_plot(client):
    path_request = [[209, 189], [209, 188],
                    [209, 187], [210, 186],
                    [210, 185], [211, 184],
                    [212, 183], [212, 182]]

    request = client.get(f'/plot?path={path_request}')
    assert b"PNG" in request.data


def test_routing_path(client):
    request = client.post('/submit', data=dict(
        lat_start=80,
        lon_start=90,
        lat_end=82,
        lon_end=82
    ), follow_redirects=True)
    assert b'Path coordinates' in request.data
