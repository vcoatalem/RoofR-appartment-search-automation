variable "aws_region" {
  description = "aws region to deploy infrastructure into"
}

variable "application_name" {
  type        = string
  description = "name of the app"
  default     = "FindARoof"
}

variable "cluster_name" {
  type        = string
  description = "ECS Cluster Name"
}

variable "repository_name" {
  type        = string
  description = "ECR Repository Name"
}

variable "table_name" {
  type        = string
  description = "Cache DynamoDB Table Name"
}

variable "image_name" {
  type        = string
  description = "Docker Image Name"
}

variable "task_name" {
  type        = string
  description = "Name for Task Definition"
}

variable "from_email" {
  type        = string
  description = ".env.FROM_EMAIL"
}

variable "from_name" {
  type        = string
  description = ".env.FROM_NAME"
}

variable "from_phone" {
  type        = string
  description = ".env.FROM_PHONE"
}

variable "from_message" {
  type        = string
  description = ".env.FROM_MESSAGE"
}


variable "aws_access_key" {
  description = ".env.AWS_ACCESS_KEY_ID"
}

variable "aws_secret_access_key" {
  description = ".env.AWS_SECRET_ACCESS_KEY"
}

variable "who" {
  type        = list(string)
  description = "who is this for ?"
}