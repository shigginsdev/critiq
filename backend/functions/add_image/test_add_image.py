import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

spec = importlib.util.spec_from_file_location("add_image", Path(__file__).with_name("add_image.py"))
module = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {"boto3": MagicMock()}):
    spec.loader.exec_module(module)


class AddImageTests(unittest.TestCase):
    def setUp(self):
        module.table = MagicMock()
        self.event = {
            "httpMethod": "POST",
            "headers": {"Origin": "http://localhost:5173"},
            "requestContext": {"authorizer": {"claims": {"sub": "owner"}}},
            "body": json.dumps({"title": "Landscape", "imageUrl": "https://example.com/art.jpg"}),
        }

    def test_server_controls_ownership_and_defaults(self):
        body = json.loads(self.event["body"])
        body.update(userID="attacker", galleryItemId="override", status="deleted")
        self.event["body"] = json.dumps(body)
        result = module.lambda_handler(self.event, None)
        self.assertEqual(result["statusCode"], 201)
        item = module.table.put_item.call_args.kwargs["Item"]
        self.assertEqual(item["userID"], "owner")
        self.assertNotEqual(item["galleryItemId"], "override")
        self.assertEqual(item["status"], "active")
        self.assertEqual(item["imageSourceType"], "external")
        self.assertEqual(item["thumbnailUrl"], item["imageUrl"])
        self.assertEqual(item["mediumImageUrl"], item["imageUrl"])

    def test_jwt_authorizer(self):
        self.event["requestContext"] = {"http": {"method": "POST"},
            "authorizer": {"jwt": {"claims": {"sub": "jwt-owner"}}}}
        self.assertEqual(module.lambda_handler(self.event, None)["statusCode"], 201)
        self.assertEqual(module.table.put_item.call_args.kwargs["Item"]["userID"], "jwt-owner")

    def test_missing_authentication(self):
        self.event["requestContext"] = {}
        self.assertEqual(module.lambda_handler(self.event, None)["statusCode"], 401)
        module.table.put_item.assert_not_called()

    def test_invalid_inputs_never_write(self):
        for value in [[], {"title": "Missing URL"},
                      {"title": "Bad", "imageUrl": "data:image/png;base64,abc"},
                      {"title": "Bad", "imageUrl": "https://example.com/a", "artworkDate": "2026-02-30"},
                      {"title": "Bad", "imageUrl": "https://example.com/a", "tags": "tag"},
                      {"title": "Bad", "imageUrl": "https://example.com/a", "imageSourceType": "upload"}]:
            with self.subTest(value=value):
                self.event["body"] = json.dumps(value)
                self.assertEqual(module.lambda_handler(self.event, None)["statusCode"], 400)
        module.table.put_item.assert_not_called()

    def test_preflight_and_wrong_method(self):
        self.event["requestContext"] = {}
        self.event["httpMethod"] = "OPTIONS"
        self.assertEqual(module.lambda_handler(self.event, None)["statusCode"], 200)
        self.event["httpMethod"] = "GET"
        self.assertEqual(module.lambda_handler(self.event, None)["statusCode"], 405)
        module.table.put_item.assert_not_called()

    def test_database_failure(self):
        module.table.put_item.side_effect = RuntimeError("database failure")
        with self.assertLogs(level="ERROR"):
            result = module.lambda_handler(self.event, None)
        self.assertEqual(result["statusCode"], 500)
        self.assertNotIn("database failure", result["body"])


if __name__ == "__main__":
    unittest.main()
