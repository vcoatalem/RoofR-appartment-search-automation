locals {
  prefix = "${var.worker_prefix}-${var.from_key}"
  task_definition_name = "${local.prefix}-taskdef"
  task_name = "${local.prefix}-task"
  cloudwatch_event_rule_name = "${local.prefix}-eventrule"
  schedule_target_name = "${local.task_name}-daily-job"
}

variable "aws_region" {
  type        = string
  description = "AWS Region to run the task into"
}

variable "worker_prefix" {
  type = string
}

variable "from_key" {
  type        = string
  description = "n"
}

variable "from_email" {
  type        = string
  description = "contacts[n].from_email"
}

variable "from_name" {
  type        = string
  description = "contacts[n].from_name"
}

variable "from_phone" {
  type        = string
  description = "contacts[n].from_phone"
}

variable "from_message" {
  type        = string
  description = "contacts[n].from_message"
}

variable "dynamodb_table_name" {
  type = string
}

variable "dynamodb_user_key_id" {
  type = string
}

variable "dynamodb_user_key_secret" {
  type = string
}

variable "cloudwatch_task_log_group_name" {
  type = string
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