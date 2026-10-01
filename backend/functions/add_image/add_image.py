"""Create an external gallery item using API Gateway Cognito/JWT claims."""
import base64
import binascii
import json
import logging
import os
from datetime import date, datetime, timezone
from urllib.parse import urlsplit
from uuid import uuid4

import boto3

table = boto3.resource("dynamodb").Table(
    os.environ.get("GALLERY_TABLE", "critiq_gallery_items")
)
ALLOWED_ORIGINS = {
    "https://main.d2w9sax6krir3g.amplifyapp.com",
    "https://4h2ydmma65.execute-api.us-east-2.amazonaws.com/dev",
    "http://localhost:5173",
}


def response(code, origin, body):
    return {
        "statusCode": code,
        "headers": {
            "Access-Control-Allow-Origin": origin if origin in ALLOWED_ORIGINS else
                "https://main.d2w9sax6krir3g.amplifyapp.com",
            "Access-Control-Allow-Headers": "Authorization,Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
            "Content-Type": "application/json",
            "Vary": "Origin",
        },
        "body": json.dumps(body),
    }


def validate_item(body):
    if not isinstance(body, dict):
        raise ValueError("Request body must be a JSON object.")
    if body.get("imageSourceType", "external") != "external":
        raise ValueError("Only external image URLs are supported.")
    item = {}
    for field, limit in {
        "title": 200, "description": 2000, "artworkDate": 10,
        "imageUrl": 2048, "mediumImageUrl": 2048,
        "thumbnailUrl": 2048, "sourcePageUrl": 2048,
    }.items():
        value = body.get(field, "")
        if not isinstance(value, str):
            raise ValueError(f"{field} must be text.")
        value = value.strip()
        if len(value) > limit:
            raise ValueError(f"{field} cannot exceed {limit} characters.")
        item[field] = value
    if not item["title"] or not item["imageUrl"]:
        raise ValueError("Title and image URL are required.")
    for field in ("imageUrl", "mediumImageUrl", "thumbnailUrl", "sourcePageUrl"):
        value = item[field]
        if value:
            parsed = urlsplit(value)
            if (parsed.scheme not in ("https", "http") or not parsed.hostname
                    or parsed.username is not None or parsed.password is not None
                    or any(character.isspace() for character in value)):
                raise ValueError(f"{field} must be a public HTTP or HTTPS URL without credentials.")
    if item["artworkDate"]:
        try:
            if date.fromisoformat(item["artworkDate"]).isoformat() != item["artworkDate"]:
                raise ValueError()
        except ValueError:
            raise ValueError("Artwork date must be a valid date in YYYY-MM-DD format.") from None
    tags = body.get("tags", [])
    if not isinstance(tags, list) or len(tags) > 20:
        raise ValueError("Tags must be a list of up to 20 tags.")
    item["tags"] = []
    for tag in tags:
        if not isinstance(tag, str) or not tag.strip() or len(tag.strip()) > 50:
            raise ValueError("Each tag must contain between 1 and 50 characters.")
        if tag.strip() not in item["tags"]:
            item["tags"].append(tag.strip())
    for field in ("mediumImageUrl", "thumbnailUrl"):
        item[field] = item[field] or item["imageUrl"]
    return item


def lambda_handler(event, context):
    headers = event.get("headers") or {}
    origin = next((value for key, value in headers.items() if key.lower() == "origin"), "")
    request_context = event.get("requestContext") or {}
    method = ((request_context.get("http") or {}).get("method")
              or event.get("httpMethod") or "").upper()
    if origin not in ALLOWED_ORIGINS:
        return response(400, origin, {"message": "Invalid origin"})
    if method == "OPTIONS":
        return response(200, origin, {"status": "ok"})
    if method != "POST":
        return response(405, origin, {"message": "Method not allowed."})
    authorizer = request_context.get("authorizer") or {}
    claims = (authorizer.get("jwt") or {}).get("claims") or authorizer.get("claims") or {}
    user_id = claims.get("sub")
    if not user_id:
        return response(401, origin, {"message": "Authenticated user could not be identified."})
    try:
        raw_body = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            raw_body = base64.b64decode(raw_body, validate=True).decode("utf-8")
        body = json.loads(raw_body)
    except (ValueError, TypeError, binascii.Error):
        return response(400, origin, {"message": "Request body must contain valid JSON."})
    try:
        item = validate_item(body)
    except ValueError as error:
        return response(400, origin, {"message": str(error)})
    item.update({
        "galleryItemId": str(uuid4()),
        "userID": user_id,
        "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "imageSourceType": "external",
        "status": "active",
    })
    try:
        table.put_item(Item=item, ConditionExpression="attribute_not_exists(galleryItemId)")
    except Exception:
        logging.exception("Unable to create gallery item")
        return response(500, origin, {"message": "Unable to save your image."})
    return response(201, origin, {"status": "success", "item": item})
