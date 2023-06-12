variable "aws_region" {
  type        = string
  description = "AWS Region to run the task into"
}

variable "cluster_name" {
    type = string
    description = "Name for our ECS Cluster"
  
}

variable "repository_name" {
  type = string
  description = "Name for our ECR Repository"
}
