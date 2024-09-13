import json
import logging
import os
import uuid
import boto3
from botocore.exceptions import ClientError

from lambdas.shared.output import (
    internal_server_error_response_constructor,
    created_response_constructor,
    bad_request_response_constructor,
)

INSTANCE = "/friends"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("TABLE_NAME", "FriendsTable"))
logger = logging.getLogger()


def handler(event, context):
    try:
        # Extract the name and age from the event body
        body = json.loads(event["body"])
        name = body.get("name", None)
        age = body.get("age", None)

        if not name or not age:
            return bad_request_response_constructor(
                "Missing required fields",
                "name and age are required and should be not null",
                INSTANCE,
            )

        # Generate a unique id for the new friend
        friend_id = str(uuid.uuid4())

        # Put the new friend into the DynamoDB table
        table.put_item(Item={"id": friend_id, "name": name, "age": age})

        return created_response_constructor({"id": friend_id, "name": name, "age": age})

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        logger.error(error_message)
        return internal_server_error_response_constructor(
            "Internal Server Error", error_message, INSTANCE
        )
