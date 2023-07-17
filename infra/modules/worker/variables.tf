locals {
  prefix = "${var.app_name}-worker"
}

variable "aws_region" {
  type        = string
  description = "AWS Region to run the task into"
}

variable "app_name" {
    type = string
}

variable "user_props" {
    type = map(string)
}

variable "ecs_task_execution_role_arn" {
  type = string
}

variable "ecs_cluster_arn" {
    type = string
}

variable "ecr_repository_url" {
  type = string
}

variable "ecr_repository_arn" {
  type = string
}

variable "vpc_subnet_id" {
    type = string
}

variable "vpc_default_security_group_id" {
    type = string
}

variable "cloudwatch_task_log_group_name" {
  type = string
}