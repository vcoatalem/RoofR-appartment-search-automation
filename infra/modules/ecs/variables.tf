variable "aws_region" {
  type        = string
  description = "AWS Region to run the task into"
}

locals {
  app_name                 = "far"
  cluster_name             = "far_cluster"
  repository_name          = "far_repository"
}