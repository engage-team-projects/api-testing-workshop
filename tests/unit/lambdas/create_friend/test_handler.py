import json
import pytest
from lambdas.create_friend.handler import handler


def test_create_friend_handler():
    event = {"body": json.dumps({"name": "John Doe", "age": 30})}
    context = {}

    # response = handler(event, context)
    #
    # assert response["statusCode"] == 201
    # body = json.loads(response["body"])
    # assert "id" in body
    # assert body["name"] == "John Doe"
    # assert body["age"] == 30
