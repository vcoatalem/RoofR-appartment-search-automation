
# Create DynamoDB table
resource "aws_dynamodb_table" "table" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  attribute {
    name = "id"
    type = "S"
  }
  attribute {
    name = "url"
    type = "S"
  }
  global_secondary_index {
    name            = "urlIndex"
    hash_key        = "url"
    projection_type = "ALL"
    read_capacity   = 5
    write_capacity  = 5
  }
}

module "ecs_ecr" {
  source     = "./modules/ecs"
  aws_region = var.aws_region
}

module "vpc" {
  source     = "./modules/vpc"
  aws_region = var.aws_region
}


# Create ECS task definition
resource "aws_ecs_task_definition" "task_definition" {
  family                   = var.task_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = module.ecs_ecr.ecs_task_role_arn
  container_definitions    = <<-DEFINITION
[
  {
    "name": "${var.image_name}",
    "image": "${module.ecs_ecr.ecr_repository_url}:${var.who[0]}",
    "memory": 256,
    "cpu": 128,
    "essential": true,
    "command": [],
    "environment": [
      {
        "name": "DYNAMO_DB_TABLE_NAME",
        "value": "${var.table_name}"
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
        "name": "IMAGE_NAME",
        "value": "${var.image_name}"
      },
      {
        "name": "AWS_ACCESS_KEY_ID",
        "value": "${var.aws_access_key}"
      },
      {
        "name": "AWS_ACCESS_KEY_SECRET",
        "value": "${var.aws_access_key_secret}"
      },
      {
        "name": "AWS_DEFAULT_REGION",
        "value": "${var.aws_region}"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${module.ecs_ecr.task_log_group_name}",
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
  name        = "schedule-${var.task_name}"
  description = "Run ECS task ${var.task_name} daily at 8 am"

  schedule_expression = "cron(0 8 * * ? *)"

  tags = {
    Name = "schedule-${var.task_name}"
  }
}

resource "aws_cloudwatch_event_target" "schedule_target" {
  rule      = aws_cloudwatch_event_rule.schedule_rule.name
  target_id = "daily-job"
  arn       = module.ecs_ecr.ecs_cluster_arn //aws_ecs_cluster.cluster.arn
  role_arn  = module.ecs_ecr.ecs_task_role_arn
  ecs_target {
    task_count          = 1
    task_definition_arn = aws_ecs_task_definition.task_definition.arn
    launch_type         = "FARGATE"
    network_configuration {
      subnets          = [module.vpc.public_subnet_id]
      security_groups  = [module.vpc.security_group_id]
      assign_public_ip = true
    }
  }
}



resource "local_file" "push_to_registry_script" {
  filename        = "${path.root}/../push-${var.who[0]}.sh"
  file_permission = "744"
  content         = <<EOF
  AWS_ACCESS_KEY_ID="${module.ecs_ecr.iam_user_access_key_id}"
  AWS_SECRET_ACCESS_KEY="${module.ecs_ecr.iam_user_access_key_secret}"
  AWS_DEFAULT_REGION=${var.aws_region}
  AWS_ECR_URL=${module.ecs_ecr.ecr_repository_url}
  IMAGE_NAME=${var.who[0]}

  aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ECR_URL
  docker build . -t $IMAGE_NAME
  docker tag $IMAGE_NAME $AWS_ECR_URL:$IMAGE_NAME
  docker push $AWS_ECR_URL:$IMAGE_NAME
  EOF
}

