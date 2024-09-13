import json
from datetime import datetime
from decimal import Decimal

response_constructors = {
    200: ok_response_constructor,
    201: created_response_constructor,
    400: bad_request_response_constructor,
    500: internal_server_error_response_constructor,
}


def _decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")


def construct_response(status_code, body):
    response = {
        "isBase64Encoded": False,
        "statusCode": 500,
        "body": json.dumps({"error": "Could not get friends"}),
        "headers": {"Content-Type": "application/json"},
    }
    return {
        "statusCode": status_code,
        "body": body,
        "headers": {"Content-Type": "application/json"},
    }


def ok_response_constructor(body):
    return _construct_response(200, json.dumps(body, default=_decimal_serializer))


def created_response_constructor(body):
    return _construct_response(201, json.dumps(body, default=_decimal_serializer))


def bad_request_response_constructor(title, detail, instance, error_type=None):
    return _construct_response(
        400, _construct_error_body(title, 400, detail, instance, error_type)
    )


def internal_server_error_response_constructor(
    title, detail, instance, error_type=None
):
    return _construct_response(
        500, _construct_error_body(title, 500, detail, instance, error_type)
    )


def _construct_response(status_code, body):
    return {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "body": body,
        "headers": {"Content-Type": "application/json"},
    }


def _construct_error_body(title, status_code, detail, instance, error_type=None):
    """Returns an RFC 9475 compliant error response JSON object

    :param error_type: The type of the error
    :param title: The title of the error
    :param status_code: The HTTP status code of the error
    :param detail: A detailed description of the error
    :param instance: A URI that identifies the specific occurrence of the error

    :return: A JSON object representing the error response
    """
    if error_type is None:
        error_type = title.lower().replace(" ", "-")
    return {
        "type": error_type,
        "title": title,
        "status": status_code,
        "detail": detail,
        "instance": instance,
        "timestamp": rfc3339_timestamp(),
    }


def rfc3339_timestamp():
    """Returns the current time in RFC 3339 format
    :return: a string representing the current time in RFC 3339 format
    """
    return datetime.datetime.utcnow().isoformat("T") + "Z"
