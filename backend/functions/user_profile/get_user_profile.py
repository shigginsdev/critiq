import json
import os
from typing import Any

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["USER_PROFILE_TABLE"])

ALLOWED_ORIGINS = {
    "https://main.d2w9sax6krir3g.amplifyapp.com",
    "http://localhost:5173",
}


def get_header(headers: dict[str, Any], name: str) -> str:
    """
    API Gateway header capitalization can vary, so compare names
    without regard to case.
    """
    name = name.lower()

    for key, value in headers.items():
        if key.lower() == name:
            return value or ""

    return ""


def get_response_headers(origin: str) -> dict[str, str]:
    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Headers": "Authorization,Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,GET",
        "Content-Type": "application/json",
    }


def create_response(
    status_code: int,
    origin: str,
    body: dict[str, Any],
) -> dict[str, Any]:

    return {
        "statusCode": status_code,
        "headers": get_response_headers(origin),
        "body": json.dumps(body),
    }


def get_user_id(event: dict[str, Any]) -> str | None:
    request_context = event.get("requestContext") or {}
    authorizer = request_context.get("authorizer") or {}

    # API Gateway HTTP API JWT authorizer
    jwt = authorizer.get("jwt") or {}
    jwt_claims = jwt.get("claims") or {}

    if jwt_claims.get("sub"):
        return jwt_claims["sub"]

    # API Gateway REST API Cognito authorizer
    claims = authorizer.get("claims") or {}

    return claims.get("sub")


def lambda_handler(event, context):
    headers = event.get("headers") or {}
    origin = get_header(headers, "origin")

    request_context = event.get("requestContext") or {}
    http_context = request_context.get("http") or {}

    method = (
        http_context.get("method")
        or event.get("httpMethod")
        or ""
    ).upper()

    if method == "OPTIONS":
        return create_response(
            200,
            origin,
            {"status": "ok"},
        )

    if origin not in ALLOWED_ORIGINS:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "status": "error",
                "message": "Invalid origin",
            }),
        }

    user_id = get_user_id(event)

    if not user_id:
        return create_response(
            401,
            origin,
            {
                "status": "error",
                "message": "Authenticated user could not be identified.",
            },
        )

    response = table.get_item(
        Key={
            "userID": user_id
        }
    )

    profile = response.get("Item")

    if not profile:
        return create_response(
            404,
            origin,
            {
                "status": "error",
                "message": "User profile not found",
            },
        )

    return create_response(
        200,
        origin,
        profile,
    )