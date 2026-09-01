import json
import os
from datetime import datetime, timezone
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
    allowed_origin = (
        origin if origin in ALLOWED_ORIGINS else next(iter(ALLOWED_ORIGINS))
    )

    return {
        "Access-Control-Allow-Origin": allowed_origin,
        "Access-Control-Allow-Headers": "Authorization,Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,PUT",
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
         return (
            jwt_claims.get("sub"),
            jwt_claims.get("email"),
        )

    # API Gateway REST API Cognito authorizer
    claims = authorizer.get("claims") or {}
    email = claims.get("email")

    return (
        claims.get("sub"),
        claims.get("email"),
    )


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
        return create_response(
            400,
            origin,
            {
                "status": "error",
                "message": "Invalid origin",
            },
        )

    user_id, email = get_user_id(event)

    if not user_id or not email:
        return create_response(
            401,
            origin,
            {
                "status": "error",
                "message": "Authenticated user could not be identified.",
            },
        )

    try:
        request_body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return create_response(
            400,
            origin,
            {
                "status": "error",
                "message": "Request body must contain valid JSON.",
            },
        )

    display_name = str(request_body.get("displayName") or "").strip()
    artist_website = str(request_body.get("artistWebsite") or "").strip()
    bio = str(request_body.get("bio") or "").strip()
    avatar_url = str(request_body.get("avatarUrl") or "").strip()
    instagram_handle = str(
        request_body.get("instagramHandle") or ""
    ).strip().lstrip("@")

    if len(display_name) > 100:
        return create_response(
            400,
            origin,
            {
                "status": "error",
                "message": "Display name cannot exceed 100 characters.",
            },
        )

    if len(bio) > 1000:
        return create_response(
            400,
            origin,
            {
                "status": "error",
                "message": "Bio cannot exceed 1,000 characters.",
            },
        )

    if len(instagram_handle) > 30:
        return create_response(
            400,
            origin,
            {
                "status": "error",
                "message": "Instagram handle cannot exceed 30 characters.",
            },
        )

    now = datetime.now(timezone.utc).isoformat()

    try:
        table.update_item(
            Key={
                "userID": user_id,
                "email": email
            },
            UpdateExpression=(
                "SET displayName = :displayName, "
                "artistWebsite = :artistWebsite, "
                "bio = :bio, "
                "avatarUrl = :avatarUrl, "
                "instagramHandle = :instagramHandle, "
                "updatedAt = :updatedAt"
            ),
            ExpressionAttributeValues={
                ":displayName": display_name,
                ":artistWebsite": artist_website,
                ":bio": bio,
                ":avatarUrl": avatar_url,
                ":instagramHandle": instagram_handle,
                ":updatedAt": now,
            },
            ConditionExpression="attribute_exists(userID)",
        )
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return create_response(
            404,
            origin,
            {
                "status": "error",
                "message": "A profile could not be found for this user.",
            },
        )
    except Exception as error:
        print(f"Unable to update profile: {error}")

        return create_response(
            500,
            origin,
            {
                "status": "error",
                "message": "Unable to update the profile.",
            },
        )

    return create_response(
        200,
        origin,
        {
            "status": "success",
            "message": "Profile updated successfully.",
            "updatedAt": now,
        },
    )