import logging
from shared.dynamodb import get_gallery_table

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# CORS Allowed Origins
ALLOWED_ORIGINS = [
    "https://main.d2w9sax6krir3g.amplifyapp.com",
    "http://localhost:3000"
]

def get_gallery(event):
    table = get_gallery_table()

    response = table.scan()

    return {
        "statusCode": 200,
        "body": response["Items"]
    }

def lambda_handler(event, context):
    """Main AWS Lambda handler"""

    # Ensure 'headers' exists in the event before accessing it
    headers = event.get('headers') or {}  # Ensure it's always a dictionary

    origin = headers.get('origin', '')  # Use default empty string if missing

    if origin == "" or "amazonaws.com" in headers.get("User-Agent", ""):
        origin = ALLOWED_ORIGINS[0]  # Default to Amplify origin for testing

    if origin not in ALLOWED_ORIGINS:
        return {
            "statusCode": 400,
            "body": json.dumps({"status": "error", "message": "Invalid origin"},)                           
        }

    logger.info(f"Received event: {json.dumps(event)}")

    # Detect the HTTP method
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')

    if http_method == 'GET':
        return {
            'statusCode': 200,
            "headers": {"Access-Control-Allow-Origin": ALLOWED_ORIGINS[0]},
            'body': json.dumps(get_gallery(event))
        }    
    else:
        return {
            "statusCode": 405,
            "headers": {"Access-Control-Allow-Origin": ALLOWED_ORIGINS[0]},
            "body": json.dumps({"message": "Method Not Allowed"})
        }
    