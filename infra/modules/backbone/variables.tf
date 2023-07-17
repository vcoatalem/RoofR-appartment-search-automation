locals {
  prefix = "${var.app_name}-backbone"
  vpc_name = "${local.prefix}-VPC"
  vpc_subnet_name = "${local.vpc_name}-public-subnet"
}

variable "aws_region" {
  type        = string
  description = "AWS Region to run the task into"
}

variable "app_name" {
  type = string
}