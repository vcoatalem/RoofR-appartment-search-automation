# Create ECS task definition
resource "aws_ecs_task_definition" "task_definition" {
  family                   = local.task_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = var.ecs_task_execution_role_arn
  container_definitions    = <<-DEFINITION
[
  {
    "name": "${var.from_key}",
    "image": "${var.ecr_repository_url}:${var.from_key}",
    "memory": 256,
    "cpu": 128,
    "essential": true,
    "command": [],
    "environment": [
      {
        "name": "AWS_DYNAMODB_NAME",
        "value": "${var.dynamodb_table_name}"
      },
      {
        "name": "FROM_EMAIL",
        "value": "${var.from_email}"
      },
      {
        "name": "FROM_NAME",
        "value": "${var.from_name}"
      },
      {
        "name": "FROM_PHONE",
        "value": "${var.from_phone}"
      },
      {
        "name": "FROM_MESSAGE",
        "value": "${var.from_message}"
      },
      {
        "name": "AWS_ACCESS_KEY_ID",
        "value": "${var.dynamodb_user_key_id}"
      },
      {
        "name": "AWS_SECRET_ACCESS_KEY",
        "value": "${var.dynamodb_user_key_secret}"
      },
      {
        "name": "AWS_DEFAULT_REGION",
        "value": "${var.aws_region}"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${var.cloudwatch_task_log_group_name}",
        "awslogs-region": "${var.aws_region}",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }
]
  DEFINITION
}

# TODO: something missing on VPC to make fargate tasks able to fetch ecr (gateway ? routing ?)

# Create scheduled ECS task
resource "aws_cloudwatch_event_rule" "schedule_rule" {
  name        = local.cloudwatch_event_rule_name
  description = "Run ECS task ${local.cloudwatch_event_rule_name} daily at 8 am"
  schedule_expression = "cron(0 8 * * ? *)"
}

resource "aws_cloudwatch_event_target" "schedule_target" {
  rule      = aws_cloudwatch_event_rule.schedule_rule.name
  target_id = local.schedule_target_name
  arn       = var.ecs_cluster_arn //aws_ecs_cluster.cluster.arn
  role_arn  = var.ecs_task_execution_role_arn
  ecs_target {
    task_count          = 1
    task_definition_arn = aws_ecs_task_definition.task_definition.arn
    launch_type         = "FARGATE"
    network_configuration {
      subnets          = [var.vpc_subnet_id]
      security_groups  = [var.vpc_default_security_group_id]
      assign_public_ip = true
    }
  }
}

