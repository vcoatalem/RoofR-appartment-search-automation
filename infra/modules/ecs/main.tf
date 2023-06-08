
variable "aws_region" {
    type = string
    description = "AWS Region to run the task into"
}


locals {
  app_name = "far"
  cluster_name = "far_cluster"
  repository_name = "far_repository"
}

# Create ECS cluster
resource "aws_ecs_cluster" "cluster" {
  name = local.cluster_name
}

# Create ECR repository
resource "aws_ecr_repository" "repository" {
  name = local.repository_name
  force_delete = true
}

# Create a CloudWatch Logs Group for ECS task logs
resource "aws_cloudwatch_log_group" "ecs_task_logs" {
  name              = "/ecs/${local.app_name}"
  retention_in_days = 7  # Define the number of days to retain the logs (adjust as needed)

}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

  inline_policy {
    name = "runTask"
    policy = jsonencode({
      Version = "1012-10-17"
      Statement = [
        {
          Action = [
            "ecr:GetAuthorizationToken",
            "ecr:BatchCheckLayerAvailability",
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ]
          Effect = "Allow"
          Resource = "*"
        }
      ]
    })
  }
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}