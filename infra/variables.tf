variable "aws_region" {
  description = "aws region to deploy infrastructure into"
}

variable "application_name" {
  type        = string
  description = "name of the app"
  default     = "FindARoof"
}

variable "cluster_name" {
  description = "ECS Cluster Name"
}

variable "repository_name" {
  description = "ECR Repository Name"
}

variable "table_name" {
  description = "Cache DynamoDB Table Name"
}

variable "image_name" {
  description = "Docker Image Name"
}

variable "task_name" {
  description = "Name for Task Definition"
}

variable "from_email" {
  description = ".env.FROM_EMAIL"
}

variable "from_name" {
  description = ".env.FROM_NAME"
}

variable "from_phone" {
  description = ".env.FROM_PHONE"
}

variable "aws_access_key" {
  description = ".env.AWS_ACCESS_KEY_ID"
}

variable "aws_access_key_secret" {
  description = ".env.AWS_SECRET_ACCESS_KEY"
}

variable "who" {
  type = list(string)
  description = "who is this for ?"
}