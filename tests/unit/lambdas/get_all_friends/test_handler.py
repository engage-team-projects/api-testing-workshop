import json
import pytest
from lambdas.get_all_friends.handler import handler


def test_get_all_friends_handler():
    event = {}
    context = {}

    # response = handler(event, context)
    #
    # assert response['statusCode'] == 200
    # friends = json.loads(response['body'])
    # assert isinstance(friends, list)
