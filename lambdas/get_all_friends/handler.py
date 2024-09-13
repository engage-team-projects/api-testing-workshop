import json
import logging
import os
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError

from lambdas.shared.output import (
    _construct_error_body,
    internal_server_error_response_constructor,
    ok_response_constructor,
)

INSTANCE = "/friends"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("TABLE_NAME", "FriendsTable"))
logger = logging.getLogger()


def handler(event, context):
    try:
        # Scan the DynamoDB table for all friends
        response = table.scan()

        # Extract the friends from the response
        friends = response["Items"]

        # Create the response
        response = ok_response_constructor(friends)

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        logger.error(error_message)
        response = internal_server_error_response_constructor(
            "Internal Server Error", error_message, INSTANCE
        )

    return response
