import csv
import os
import boto3
import json

from src.domain.cache_port import CachePort
from src.domain.domain_types import Annonce


class DynamodbAdapter(CachePort):
    def __init__(self, dynamodb_table_name: str) -> None:
        # Create a DynamoDB client
        self.dynamodb = boto3.client('dynamodb', region_name='us-east-1')
        # Define the table name
        self.table_name = dynamodb_table_name
        super().__init__()

    @staticmethod
    def __annonce_from_dynamodb(item):
        print(item)
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