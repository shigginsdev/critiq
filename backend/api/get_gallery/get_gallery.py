import logging
import json
from shared.dynamodb import get_gallery_table

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ALLOWED_ORIGINS = [
    "https://main.d2w9sax6krir3g.amplifyapp.com",
    "http://localhost:3000"
]


def get_user_id(event):
    request_context = event.get("requestContext", {})
    authorizer = request_context.get("authorizer", {})

    # REST API / Cognito Authorizer
    claims = authorizer.get("claims", {})

    # HTTP API / JWT Authorizer
    if not claims:
        claims = authorizer.get("jwt", {}).get("claims", {})

    return claims.get("sub")


def get_gallery(event):
    table = get_gallery_table()

    logger.info(
        f"Authorizer: {json.dumps(event.get('requestContext', {}).get('authorizer', {}))}"
    )
    
    user_id = get_user_id(event)

    if not user_id:
        raise ValueError("Unable to determine authenticated user")

    logger.info(f"Getting gallery for user: {user_id}")

    response = table.scan(
        FilterExpression="userID = :userID",
        ExpressionAttributeValues={
            ":userID": user_id
        }
    )

    return response["Items"]


def lambda_handler(event, context):
    """Main AWS Lambda handler"""

    headers = event.get("headers") or {}
    origin = headers.get("origin", "")

    if origin == "" or "amazonaws.com" in headers.get("User-Agent", ""):
        origin = ALLOWED_ORIGINS[0]

    if origin not in ALLOWED_ORIGINS:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "status": "error",
                "message": "Invalid origin"
            })
        }

    logger.info(f"Received event: {json.dumps(event)}")

    http_method = (
        event.get("httpMethod")
        or event.get("requestContext", {})
                .get("http", {})
                .get("method", "")
    )

    if http_method == "GET":
        try:
            items = get_gallery(event)

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": origin
                },
                "body": json.dumps(items)
            }

        except ValueError as ex:
            logger.error(str(ex))

            return {
                "statusCode": 401,
                "headers": {
                    "Access-Control-Allow-Origin": origin
                },
                "body": json.dumps({
                    "message": "Unauthorized"
                })
            }

    return {
        "statusCode": 405,
        "headers": {
            "Access-Control-Allow-Origin": origin
        },
        "body": json.dumps({
            "message": "Method Not Allowed"
        })
    }