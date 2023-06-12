variable "aws_region" {
  type        = string
  description = "AWS Region to run the task into"
}

variable "table_name" {
  type = string
  description = "Name for the DynamoDB table"
}