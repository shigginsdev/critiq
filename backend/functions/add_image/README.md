# Add Image Lambda

Deploy `add_image.py` with handler `add_image.lambda_handler` using the same Python runtime and Cognito/API Gateway setup as `update_user_profile.py`. The Lambda runtime supplies boto3.

- Set `GALLERY_TABLE=critiq_gallery_items` (also the default).
- Grant its execution role `dynamodb:PutItem` on that table and standard CloudWatch logging permissions.
- Connect an API Gateway `POST` route (for example `/gallery`) to this Lambda using proxy integration. Require the Cognito or JWT authorizer; ownership comes exclusively from its `sub` claim.
- Allow unauthenticated `OPTIONS` preflight with `Authorization,Content-Type` headers and `POST,OPTIONS` methods. If API Gateway handles CORS, configure the same allowed frontend origins there, including CORS on gateway errors.
- Set the frontend build variable `VITE_ADD_IMAGE_API_URL` to the full POST endpoint URL and rebuild the frontend.

The request uses ordinary JSON (not DynamoDB's typed export format): required `title` and `imageUrl`; optional `description`, `artworkDate` (`YYYY-MM-DD`), `mediumImageUrl`, `thumbnailUrl`, `sourcePageUrl`, and `tags` (string array). Blank medium and thumbnail URLs default to `imageUrl`. The Lambda generates `galleryItemId`, `createdAt`, `userID`, `imageSourceType=external`, and `status=active`. boto3 serializes these values to the DynamoDB types in the gallery schema.

No image bytes are uploaded or fetched by the Lambda. Image URLs must point to externally hosted images accessible to gallery visitors.
