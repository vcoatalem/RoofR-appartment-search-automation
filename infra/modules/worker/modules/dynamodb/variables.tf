locals {
  prefix      = "${var.worker_prefix}-dynamodb"
  table_name  = "${local.prefix}-table"
  user_name   = "${local.prefix}-user"
  policy_name = "${local.user_name}-policy"
}

variable "aws_region" {
  type        = string
  description = "AWS Region to run the task into"
}

variable "worker_prefix" {
  type = string
}



