# Create ECS cluster
resource "aws_ecs_cluster" "cluster" {
  name = local.cluster_name
}

# Create ECR repository
resource "aws_ecr_repository" "repository" {
  name         = local.repository_name
  force_delete = true
}

# Create a CloudWatch Logs Group for ECS task logs
resource "aws_cloudwatch_log_group" "ecs_task_logs" {
  name              = "/ecs/${local.app_name}"
  retention_in_days = 7 # Define the number of days to retain the logs (adjust as needed)
}
