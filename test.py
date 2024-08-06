from unittest.mock import patch
from main import get_outages, get_site_info, post_site_outages, filtered_outages


@patch('requests.get')
def test_get_outages(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            'id': '04012c33-bafb-4b61-8f16-3cb5db8f6ced',
            'begin': '2022-05-06T15:01:33.813Z',
            'end': '2022-08-25T15:27:04.788Z'
        }
    ]
    outages = get_outages()
    assert outages == [
        {
            'id': '04012c33-bafb-4b61-8f16-3cb5db8f6ced',
            'begin': '2022-05-06T15:01:33.813Z',
            'end': '2022-08-25T15:27:04.788Z'
        }
    ]


@patch('requests.get')
def test_get_site_info(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "id": "norwich-pear-tree",
        "name": "Norwich Pear Tree",
        "devices":
            [
                {
                    'id': '111183e7-fb90-436b-9951-63392b36bdd2',
                    'name': 'Battery 1'
                }
            ]
    }
    site_info = get_site_info("norwich-pear-tree")
    assert site_info == {
        "id": "norwich-pear-tree",
        "name": "Norwich Pear Tree",
        "devices":
            [
                {
                    'id': '111183e7-fb90-436b-9951-63392b36bdd2',
                    'name': 'Battery 1'
                }
            ]
    }


@patch('requests.post')
def test_post_site_outages(mock_post):
    mock_post.return_value.status_code = 200
    response = post_site_outages("norwich-pear-tree", [
        {
            'id': '04012c33-bafb-4b61-8f16-3cb5db8f6ced',
            'begin': '2022-05-06T15:01:33.813Z',
            'end': '2022-08-25T15:27:04.788Z'
        }
    ]
                                 )
    assert response == 200


def test_filtered_outages():
    outages = [
        {"id": "1", "begin": "2022-01-01T00:00:00.000Z"},
        {"id": "2", "begin": "2021-01-01T00:00:00.000Z"}
    ]
    site_info = {"devices": [{"id": "1", "name": "Device 1"}]}
    result = filtered_outages(outages, site_info)
    assert result == [{"id": "1", "begin": "2022-01-01T00:00:00.000Z", "name": "Device 1"}]
