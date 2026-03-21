import allure
import pytest
import requests
from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature('Test Create Booking')
@allure.story('Positive: creating booking with custom data')
def test_creating_booking_with_custom_data(api_client):
    with allure.step('Sending a request to create booking'):
        booking_data = {
            "firstname": "Ivan",
            "lastname": "Ivanovich",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-02-01",
                "checkout": "2025-02-10"
            },
            "additionalneeds": "Dinner"
        }

        response = api_client.create_booking(booking_data)
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValueError(f'Response validation failed: {e}')

        assert response['booking']['firstname'] == booking_data['firstname']
        assert response['booking']['lastname'] == booking_data['lastname']
        assert response['booking']['totalprice'] == booking_data['totalprice']
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
        assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.story('Positive: creating booking with random dates')
def test_creating_booking_with_random_dates(api_client, booking_dates):
    with allure.step('Sending a request to create booking'):
        booking_data = {
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": booking_dates["checkin"],
                "checkout": booking_dates["checkout"]
            },
            "additionalneeds": "Breakfast"
        }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValueError(f'Response validation failed: {e}')

    assert 'bookingid' in response
    assert response['bookingid'] > 0
    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.story('Positive: creating booking without optional field')
def test_creating_booking_without_optional_field(api_client):
    with allure.step('Sending a request to create booking'):
        booking_data = {
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            }
        }
        response = api_client.create_booking(booking_data)
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValueError(f'Response validation failed: {e}')

        assert 'bookingid' in response
        assert response['bookingid'] > 0
        assert response['booking']['firstname'] == booking_data['firstname']
        assert response['booking']['lastname'] == booking_data['lastname']
        assert response['booking']['totalprice'] == booking_data['totalprice']
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
        assert 'additionalneeds' not in response['booking']


@allure.story('Positive: creating booking with same bookingdates')
def test_creating_booking_with_same_bookingdates(api_client):
    with allure.step('Sending a request to create booking'):
        booking_data = {
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2019-01-01",
                "checkout": "2019-01-01"
            },
            "additionalneeds": "Breakfast"
        }
        response = api_client.create_booking(booking_data)
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValueError(f'Response validation failed: {e}')

        assert 'bookingid' in response
        assert response['bookingid'] > 0
        assert response['booking']['firstname'] == booking_data['firstname']
        assert response['booking']['lastname'] == booking_data['lastname']
        assert response['booking']['totalprice'] == booking_data['totalprice']
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
        assert response['booking']['additionalneeds'] == booking_data['additionalneeds']
        assert response["booking"]["bookingdates"]["checkin"] == response["booking"]["bookingdates"]["checkout"]


@allure.story('Positive: creating bookings with the same data')
def test_create_bookings_with_same_data(api_client):
    with allure.step('Sending a request to create booking'):
        booking_data = {
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            },
            "additionalneeds": "Breakfast"
        }

        response1 = api_client.create_booking(booking_data)
        response2 = api_client.create_booking(booking_data)

        try:
            BookingResponse(**response1)
        except ValidationError as e:
            raise ValueError(f'Response validation failed: {e}')

        try:
            BookingResponse(**response2)
        except ValidationError as e:
            raise ValueError(f'Response validation failed: {e}')

    with allure.step('Checking bookingid'):
        assert response1['bookingid'] != response2['bookingid']

    with allure.step('Checking params of the booking'):
        assert response1['booking'] == response2['booking']


@allure.story('Positive: creating booking with minimum values')
def test_creating_booking_with_minimum_values(api_client):
    with allure.step('Sending a request to create booking'):
        booking_data = {
            "firstname": "J",
            "lastname": "B",
            "totalprice": 0,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "0001-01-01",
                "checkout": "0001-01-01"
            }
        }
        response = api_client.create_booking(booking_data)
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValueError(f'Response validation failed: {e}')

        assert 'bookingid' in response
        assert response['bookingid'] > 0
        assert response['booking']['firstname'] == booking_data['firstname']
        assert response['booking']['lastname'] == booking_data['lastname']
        assert response['booking']['totalprice'] == booking_data['totalprice']
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']


@allure.story('Positive: creating booking with maximum values')
def test_creating_booking_with_maximum_values(api_client):
    with allure.step('Sending a request to create booking'):
        booking_data = {
            "firstname": "J" * 255,
            "lastname": "B" * 255,
            "totalprice": 9999999,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "9999-12-31",
                "checkout": "9999-12-31"
            },
            "additionalneeds": "C" * 255
        }
        response = api_client.create_booking(booking_data)
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValueError(f'Response validation failed: {e}')

        assert 'bookingid' in response
        assert response['bookingid'] > 0
        assert response['booking']['firstname'] == booking_data['firstname']
        assert response['booking']['lastname'] == booking_data['lastname']
        assert response['booking']['totalprice'] == booking_data['totalprice']
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
        assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.story('Positive: creating booking with special symbols in name')
def test_creating_booking_with_special_symbols_in_name(api_client):
    with allure.step('Sending a request to create booking'):
        booking_data = {
            "firstname": "Jim123!?<>",
            "lastname": "Brown123!?<>",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            },
            "additionalneeds": "Breakfast"
        }
        response = api_client.create_booking(booking_data)
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValueError(f'Response validation failed: {e}')

        assert 'bookingid' in response
        assert response['bookingid'] > 0
        assert response['booking']['firstname'] == booking_data['firstname']
        assert response['booking']['lastname'] == booking_data['lastname']
        assert response['booking']['totalprice'] == booking_data['totalprice']
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
        assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.story('Negative: creating booking with empty booking_data')
def test_create_booking_with_empty_booking_data(api_client):
    with allure.step('Sending a request to create booking'):
        booking_data = {}
        with pytest.raises(requests.exceptions.HTTPError) as e:
            api_client.create_booking(booking_data)

        assert e.value.response.status_code == 500


@allure.story('Negative: creating booking with missing params')
@pytest.mark.parametrize(
    'booking_data',
    [
        ({
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            }
        }),
        ({
            "firstname": "Jim",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            }
        }),
        ({
            "firstname": "Jim",
            "lastname": "Brown",
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            }
        }),
        ({
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            }
        }),
        ({
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True
        }),
        ({
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01"
            }
        }),
        ({
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkout": "2019-01-01"
            }
        })
    ]
)
def test_create_booking_with_missing_params(api_client, booking_data):
    with allure.step('Sending a request to create booking'):

        with pytest.raises(requests.exceptions.HTTPError) as e:
            api_client.create_booking(booking_data)

        assert e.value.response.status_code == 500
