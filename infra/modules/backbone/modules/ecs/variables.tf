locals {
  prefix                          = "${var.backbone_prefix}-ecs"
  cluster_name                    = "${local.prefix}-cluster-name"
  task_execution_user_name        = "${local.prefix}-execution-user"
  task_execution_role_name        = "${local.prefix}-execution-role"
  task_execution_user_policy_name = "${local.prefix}-execution-policy"
}

variable "backbone_prefix" {
  type = string
}

variable "aws_region" {
  type        = string
  description = "AWS Region to run the task into"
}
