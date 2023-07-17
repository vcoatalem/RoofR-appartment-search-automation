locals {
  prefix                          = "${var.backbone_prefix}-ecr"
  repository_name                    = "${local.prefix}-repository"
  repository_admin_user_name        = "${local.prefix}-repository-admin-user"
  repository_admin_user_policy_name = "${local.prefix}-repository-admin-user-policy"
}

variable "backbone_prefix" {
  type = string
}

variable "aws_region" {
  type        = string
  description = "AWS Region to run the task into"
}
