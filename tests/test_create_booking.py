import allure
import pytest
import requests


@allure.feature('Test Create Booking')
@allure.story('Creating booking')
def test_creating_success_booking(api_client):
    with allure.step('Authenticate to get token'):
        api_client.auth()

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
        response = api_client.create_booking(booking_data)
        response_json = response.json()

    with allure.step('Assert status code'):
        assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'

    with allure.step('Checking params of the booking'):
        assert 'bookingid' in response_json
        assert response_json['bookingid'] > 0
        assert response_json['booking']['firstname'] == booking_data['firstname']
        assert response_json['booking']['lastname'] == booking_data['lastname']
        assert response_json['booking']['totalprice'] == booking_data['totalprice']
        assert response_json['booking']['depositpaid'] == booking_data['depositpaid']
        assert response_json['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response_json['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
        assert response_json['booking']['additionalneeds'] == booking_data['additionalneeds']
