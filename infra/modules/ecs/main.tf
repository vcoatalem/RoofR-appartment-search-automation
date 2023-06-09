
resource "random_string" "random_key"{
  keepers = {
    first = "${timestamp()}"
  }    
  length = 16
  special = false
}

variable "aws_region" {
    type = string
    description = "AWS Region to run the task into"
}

locals {
  app_name = "far"
  cluster_name = "far_cluster"
  repository_name = "far_repository"
  task_execution_role_hash = replace(trimspace(random_string.random_key.result), "/[^a-zA-Z0-9]/", "")
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

data "aws_iam_policy" "task_execution_policy" {
  name = "AmazonECSTaskExecutionRolePolicy"
}

/*
resource "aws_iam_policy" "allow-run-task" {
  name = "allow run task"
  policy = jsonencode({
      Version = "1012-10-17",
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
*/

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs-task-execution-role-${local.task_execution_role_hash}"
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
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = data.aws_iam_policy.task_execution_policy.arn
}

resource "aws_iam_user" "script_user" {
  name = "${local.app_name}-service-user" 
}

resource "aws_iam_access_key" "script_user_key" {
  user = aws_iam_user.script_user.name
}

resource "aws_iam_user_policy" "script_user_policy" {
  name = "${local.app_name}-service-user-policy"
  user = aws_iam_user.script_user.name
  policy = jsonencode({
    Version = "2012-10-17"
    "Statement": [
        {
            "Sid": "ListAndDescribe",
            "Effect": "Allow",
            "Action": [
                "dynamodb:List*",
                "dynamodb:DescribeReservedCapacity*",
                "dynamodb:DescribeLimits",
                "dynamodb:DescribeTimeToLive"
            ],
            "Resource": "*"
        },
        {
            "Sid": "SpecificTable",
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGet*",
                "dynamodb:DescribeStream",
                "dynamodb:DescribeTable",
                "dynamodb:Get*",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWrite*",
                "dynamodb:CreateTable",
                "dynamodb:Delete*",
                "dynamodb:Update*",
                "dynamodb:PutItem"
            ],
            "Resource": "*"
        },
        {
            "Sid": "ECR",
            "Effect": "Allow",
            "Action": [
                "ecr:*"
            ],
            "Resource": "*"
        }
    ]
  })
}
