# dynamodb.py

import boto3

dynamodb = boto3.resource('dynamodb')

def get_gallery_table():
    return dynamodb.Table('critiq_gallery_items')