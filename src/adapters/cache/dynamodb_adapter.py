import csv
import os
import boto3
import json

from botocore.config import Config
from src.domain.cache_port import CachePort
from src.domain.domain_types import Annonce


class DynamodbAdapter(CachePort):
    def __init__(self, table_name: str, region: str) -> None:
        # Create a DynamoDB client
        self.dynamodb = boto3.client(
            'dynamodb',
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = os.getenv("AWS_ACCESS_KEY_SECRET")
            config=Config(region_name = region)
        )
        
        # Define the table name
        self.table_name = table_name
        super().__init__()

    @staticmethod
    def from_env():
        region = os.getenv("AWS_DEFAULT_REGION")
        table_name = os.getenv("DYNAMO_DB_TABLE_NAME")
        return DynamodbAdapter(
            table_name,
            region
        )

    @staticmethod
    def __annonce_from_dynamodb(item):
        print("parsed annonce:", item)
        return Annonce(item['id']['S'], item['url']['S'])

    @staticmethod
    def __annonce_to_dynamodb(annonce: Annonce) -> list[str]:
        return {
            'id': {'S': annonce.id},
            'url': {'S': annonce.url}
        }

    def load(self) -> set[Annonce]:

        # Scan the table and retrieve all items
        query = self.dynamodb.scan(TableName=self.table_name)
        #print(query)
        for item in query['Items']:
            self.annonces.add(DynamodbAdapter.__annonce_from_dynamodb(item))
        return self.annonces
    
    def save(self) -> bool:
        for annonce in self.annonces_to_save:
            self.dynamodb.put_item(
                TableName=self.table_name,
                Item=DynamodbAdapter.__annonce_to_dynamodb(annonce)
            )
        return True