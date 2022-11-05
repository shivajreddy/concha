"""
Tests for /audio-data endpoint
"""
from pydantic import ValidationError

from server.config import settings

from psql_db import schemas
from psql_db.models import AudioData

from tests.database import client, session

base_url = settings.base_url_test


def test_audio_get_all(client):
    url = base_url + '/audio-data/all'
    res = client.get(url=url)

    # test -> get all audio-data
    assert res.status_code == 200
    if res.json():
        schemas.AudioDataResponseSchema(**res.json())  # response schema validation
    assert isinstance(res.json(), list)  # only list, not other collections


def test_audio_new(test_fixture_audio_1, client):
    url = base_url + '/audio-data/new'
    res = test_fixture_audio_1

    # test -> insert new audio with proper fields
    assert res.status_code == 200
    schemas.AudioDataResponseSchema(**res.json())  # schema validation

    # test -> only post method is allowed
    res = client.get(url=url)
    assert res.status_code == 405
    assert res.json() == {'detail': 'Method Not Allowed'}


def test_audio_get_all_by_userid(test_fixture_audio_1, test_fixture_user_1_token, client):
    url = base_url + "/audio-data/all-by-userid"

    token = test_fixture_user_1_token.json()['token']
    headers_user_1 = {"Authorization": f"Bearer {token}"}

    res = client.get(url=url, headers=headers_user_1)
    assert res.status_code == 200
    schemas.AudioDataDbSchema(**res.json()[0])
    assert isinstance(res.json(), list)
    assert len(res.json()[0]["ticks"]) == 15


def test_audio_invalid_field_input(test_fixture_user_1_token, client):
    url = base_url + '/audio-data/new'

    token = test_fixture_user_1_token.json()["token"]
    headers_user_1 = {"Authorization": f"Bearer {token}"}

    # test -> no request body
    res = client.post(url=url, headers=headers_user_1)
    assert res.status_code == 422
    assert res.json() == {'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}

    # test -> incorrect length for ticks array
    data_ticks_wrong_length = {
        "ticks": [-96.33, -66.89, -62.46, -58.03],
        "selected_tick": 5,
        "session_id": 3448,
        "step_count": 1}
    res = client.post(url=url, headers=headers_user_1, json=data_ticks_wrong_length)
    assert res.status_code == 422
    assert res.json() == {'detail': [{'loc': ['body', 'ticks'], 'msg': 'ensure this value has at least 15 items',
                                      'type': 'value_error.list.min_items', 'ctx': {'limit_value': 15}}]}

    # test -> incorrect data type for items in ticks array
    data_ticks_wrong_data_type = {
        "ticks": [-96, -96.33, -93.47, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03,
                  -53.6, -49.17, -44.74, -40.31],
        "selected_tick": 5,
        "session_id": 3448,
        "step_count": 1}
    res = client.post(url=url, headers=headers_user_1, json=data_ticks_wrong_data_type)
    assert res.status_code == 422
    assert res.json() == {
        'detail': [{'loc': ['body', 'ticks', 0], 'msg': 'value is not a valid float', 'type': 'type_error.float'}]}

    # test -> each tick in tick's should be in range -100.0 t0 -10.0, changing the first value to -100.1
    data_ticks_out_of_range_value = {
        "ticks": [-100.1, -96.33, -93.47, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03,
                  -53.6, -49.17, -44.74, -40.31],
        "selected_tick": 5,
        "session_id": 3448,
        "step_count": 1}
    res = client.post(url=url, headers=headers_user_1, json=data_ticks_out_of_range_value)
    assert res.status_code == 422
    res_error_val = res.json()['detail'][0]
    assert res_error_val['loc'] == ['body', 'ticks', 0]
    assert res_error_val['msg'] == "ensure this value is greater than or equal to -100.0"
    assert res_error_val['ctx'] == {'limit_value': -100.0}

    # test -> each tick in tick's should be in range -100.0 t0 -10.0. changing the 2nd value to -9.9
    data_ticks_out_of_range_value = {
        "ticks": [-96.33, -9.9, -93.47, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03,
                  -53.6, -49.17, -44.74, -40.31],
        "selected_tick": 5,
        "session_id": 3448,
        "step_count": 1}
    res = client.post(url=url, headers=headers_user_1, json=data_ticks_out_of_range_value)

    assert res.status_code == 422
    res_error_val = res.json()['detail'][0]
    assert res_error_val['loc'] == ['body', 'ticks', 1]
    assert res_error_val['msg'] == "ensure this value is less than or equal to -10.0"
    assert res_error_val['ctx'] == {'limit_value': -10.0}

    # test -> session_id must be int
    data_session_id_not_int = {
        "ticks": [-96.33, -96.33, -93.47, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03,
                  -53.6, -49.17, -44.74, -40.31],
        "selected_tick": 5,
        "session_id": "3448",
        "step_count": 1}
    res = client.post(url=url, headers=headers_user_1, json=data_session_id_not_int)
    assert res.status_code == 422
    res_error_val = res.json()['detail'][0]
    assert res_error_val['loc'] == ['body', 'session_id']
    assert res_error_val['msg'] == 'value is not a valid integer'
    res_error_val['type'] = 'value_error.number.not_le'

    # test -> selected_tick must be int
    data_selected_tick_not_int = {
        "ticks": [-96.33, -96.33, -93.47, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03,
                  -53.6, -49.17, -44.74, -40.31],
        "selected_tick": "5",
        "session_id": 3448,
        "step_count": 1}
    res = client.post(url=url, headers=headers_user_1, json=data_selected_tick_not_int)
    assert res.status_code == 422
    res_error_val = res.json()['detail'][0]
    assert res_error_val['loc'] == ['body', 'selected_tick']
    assert res_error_val['msg'] == 'value is not a valid integer'
    res_error_val['type'] = 'type_error.integer'

    # test -> selected_tick must within range 0 to 14
    data_selected_tick_not_in_range = {
        "ticks": [-96.33, -96.33, -93.47, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03,
                  -53.6, -49.17, -44.74, -40.31],
        "selected_tick": 20,
        "session_id": 3448,
        "step_count": 1}
    res = client.post(url=url, headers=headers_user_1, json=data_selected_tick_not_in_range)
    assert res.status_code == 422
    res_error_val = res.json()['detail'][0]
    assert res_error_val['loc'] == ['body', 'selected_tick']
    assert res_error_val['msg'] == 'ensure this value is less than or equal to 14'
    assert res_error_val['ctx'] == {'limit_value': 14}
    res_error_val['type'] = 'type_error.integer'


def test_audio_new_session_id(test_fixture_audio_1, test_fixture_user_1, test_fixture_user_2, test_fixture_user_2_token,
                              client):
    # test -> adding a new audio data cant have session_id if it doesn't belong to prev. user
    url = base_url + '/audio-data/new'
    token = test_fixture_user_2_token.json()["token"]
    headers_user_1 = {"Authorization": f"Bearer {token}"}

    data = {
        "ticks": [-96.33, -96.33, -93.47, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03,
                  -53.6, -49.17, -44.74, -40.31],
        "selected_tick": 5,
        "session_id": 3448,
        "step_count": 2}

    res = client.post(url=url, headers=headers_user_1, json=data)
    assert res.status_code == 422
    assert res.json() == {
        'detail': f'session_id:{data["session_id"]} is taken by user with email: {test_fixture_user_1["email"]}'}


# TODO
# test_audio_update
# test_audio_search_by_session_id
def test_audio_update(test_fixture_audio_1, test_fixture_user_1, test_fixture_user_1_token, client):
    # print("test-audio-1=", test_fixture_audio_1)
    # print("test-audio-1=", test_fixture_audio_1.json())
    url = base_url + "/audio-data/update"
    token = test_fixture_user_1_token.json()["token"]
    headers_user_1 = {"Authorization": f"Bearer {token}"}

    # test -> must pass session_id, step_count to update
    no_data = {}
    res = client.patch(url=url, headers=headers_user_1, json=no_data)
    assert res.status_code == 422
    res_error_val = res.json()['detail']
    assert res_error_val[0]['loc'] == ['body', 'session_id']
    assert res_error_val[1]['loc'] == ['body', 'step_count']
    assert res_error_val[0]['msg'] and res_error_val[1]['msg'] == 'field required'
    assert res_error_val[0]['type'] and res_error_val[1]['type'] == 'value_error.missing'

    # test -> current users session
    def test_fail_on_attempt_to_edit_step_count_to_duplicate(self):
        """Test to ensure exception when attempting to edit step_count to the same number as a preexisting step in session"""
