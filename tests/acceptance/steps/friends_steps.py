from behave import given, when, then
import boto3
import requests
import json


@given("the Friends API is running")
def step_impl(context):
    context.apigateway = boto3.client(
        "apigateway", endpoint_url="http://localhost:4566"
    )
    context.lambda_client = boto3.client("lambda", endpoint_url="http://localhost:4566")

    # Get the list of REST APIs
    rest_apis = context.apigateway.get_rest_apis()

    print(rest_apis["items"])

    # Find the REST API with the name "FriendsAPI"
    for item in rest_apis["items"]:
        if item["name"] == "FriendsApi":
            context.rest_api_id = item["id"]
            break
    else:
        raise Exception("FriendsAPI not found")


@when('I create a friend with name "{name}" and age {age}')
def step_impl(context, name, age):
    url = f"http://localhost:4566/restapis/{context.rest_api_id}/test/_user_request_/friends"
    print(url)
    data = {
        "name": name,
        "age": int(age),
    }
    response = requests.post(url, data=json.dumps(data))
    context.response = response


@then("the response status code should be {status_code}")
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code)


@then("the response should include the friend's ID")
def step_impl(context):
    response_body = context.response.json()
    assert "id" in response_body


@when("I get all friends")
def step_impl(context):
    url = f"http://localhost:4566/restapis/{context.rest_api_id}/test/_user_request_/friends"
    response = requests.get(url)
    context.response = response


@then("the response should be a list of friends")
def step_impl(context):
    response_body = context.response.json()
    assert isinstance(response_body, list)
