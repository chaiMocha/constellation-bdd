import os
import requests
from behave import given, when, then
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("Critical Error: MY_API_KEY is not set in the BDD environment.")

BASE_URL = "http://localhost:8000"

@given('the telemetry API is running locally')
def step_impl(context):
    context.base_url = BASE_URL
    
    context.headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        requests.get(f"{context.base_url}/health", headers=context.headers) 
    except requests.exceptions.ConnectionError:
        raise AssertionError("FastAPI server is not running on localhost:8000")

@when('I request the current telemetry for "{satellite_id}"')
def step_impl(context, satellite_id):
    endpoint = f"{context.base_url}/telemetry/{satellite_id}/latest"
    
    context.response = requests.get(endpoint, headers=context.headers)

@then('the API should respond with a {status_code:d} status code')
def step_impl(context, status_code):
    assert context.response.status_code == status_code, \
        f"Expected {status_code}, but got {context.response.status_code}. Response: {context.response.text}"

@then('the response should contain the "{field_name}" field')
def step_impl(context, field_name):
    json_data = context.response.json()
    assert field_name in json_data, f"Field '{field_name}' missing from API response"

@then('the response should contain a valid "status"')
def step_impl(context):
    json_data = context.response.json()
    status = json_data.get('status')
    
    valid_statuses = ['NOMINAL', 'WARNING', 'CRITICAL']
    assert status in valid_statuses, f"Invalid status returned: {status}"