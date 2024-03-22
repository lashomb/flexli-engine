import os

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from pydantic import parse_obj_as

from apis.middleware import api_middleware_v1
from apis.models import ApiMiddlewareEvent, ApiResponse
from database.connectors import list_connectors

from local import ConnectorsV1List, ConnectorsV1ListItem

logger = Logger()

TABLE_NAME = os.getenv("TABLE_NAME")

dynamodb_table = boto3.resource("dynamodb").Table(TABLE_NAME)


@api_middleware_v1(output_validator=ConnectorsV1List)
def lambda_handler(event: ApiMiddlewareEvent, context: LambdaContext) -> ApiResponse:
    response = list_connectors(dynamodb_table, tenant_id=event.tenant_id)
    return ApiResponse(
        200,
        {
            "items": [
                parse_obj_as(ConnectorsV1ListItem, item).dict() for item in response
            ]
        },
    )