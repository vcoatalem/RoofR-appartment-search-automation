resource "aws_dynamodb_table" "table" {
  name         = local.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  attribute {
    name = "id"
    type = "S"
  }
  attribute {
    name = "url"
    type = "S"
  }
  global_secondary_index {
    name            = "urlIndex"
    hash_key        = "url"
    projection_type = "ALL"
  }
}