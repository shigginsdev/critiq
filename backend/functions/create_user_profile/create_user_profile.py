import os
from datetime import datetime, timezone

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["USER_PROFILE_TABLE"])


def lambda_handler(event, context):
    attributes = event["request"]["userAttributes"]

    user_id = attributes["sub"]
    email = attributes.get("email")
    now = datetime.now(timezone.utc).isoformat()

    table.put_item(
        Item={
            "userID": user_id,
            "email": email,
            "createdAt": now,
            "updatedAt": now,
            "status": "active",
            "role": "user",
        },
        ConditionExpression="attribute_not_exists(userId)",
    )

    # Cognito requires the original event to be returned.
    return event