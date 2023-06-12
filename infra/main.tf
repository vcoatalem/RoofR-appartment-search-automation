
# Create DynamoDB table


module "ecs_ecr" {
  source     = "./modules/ecs"
  aws_region = var.aws_region
  cluster_name = var.cluster_name
  repository_name = var.repository_name
}

module "vpc" {
  source     = "./modules/vpc"
  aws_region = var.aws_region
}

module "dynamodb" {
  source     = "./modules/dynamodb"
  aws_region = var.aws_region
  table_name = var.table_name
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
        "name": "AWS_DYNAMODB_NAME",
        "value": "${module.dynamodb.dynamodb_table_name}"
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
        "name": "IMAGE_NAME",
        "value": "${var.image_name}"
      },
      {
        "name": "AWS_ACCESS_KEY_ID",
        "value": "${module.dynamodb.iam_user_access_key_id}"
      },
      {
        "name": "AWS_SECRET_ACCESS_KEY",
        "value": "${module.dynamodb.iam_user_access_key_secret}"
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
  filename        = "${path.root}/generated-scripts/push-${var.who[0]}.sh"
  file_permission = "744"
  content         = <<EOF
AWS_ACCESS_KEY_ID=${module.dynamodb.iam_user_access_key_id}
AWS_SECRET_ACCESS_KEY=${module.dynamodb.iam_user_access_key_secret}
AWS_DEFAULT_REGION=${var.aws_region}
AWS_ECR_URL=${module.ecs_ecr.ecr_repository_url}
IMAGE_NAME=${var.who[0]}

aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ECR_URL
cd ${path.root}/..
docker build . -t $IMAGE_NAME -f Dockerfile
docker tag $IMAGE_NAME $AWS_ECR_URL:$IMAGE_NAME
docker push $AWS_ECR_URL:$IMAGE_NAME
EOF
}

resource "local_file" "run_task_script" {
  filename        = "${path.root}/generated-scripts/test-${var.who[0]}.sh"
  file_permission = "744"
  content         = <<EOF
AWS_ACCESS_KEY_ID=${module.ecs_ecr.iam_user_access_key_id}
AWS_SECRET_ACCESS_KEY=${module.ecs_ecr.iam_user_access_key_secret}
AWS_DEFAULT_REGION=${var.aws_region}

AWS_CLUSTER_NAME=${var.cluster_name}
TASK_NAME=${var.task_name}
TASK_DEFINITION_REVISION=${aws_ecs_task_definition.task_definition.revision}

SUBNET_ID=${module.vpc.public_subnet_id}
SECURITY_GROUP_ID=${module.vpc.security_group_id}

aws ecs run-task --launch-type FARGATE \
    --cluster $AWS_CLUSTER_NAME \
    --task-definition $TASK_NAME:$TASK_DEFINITION_REVISION \
    --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_ID],securityGroups=[$SECURITY_GROUP_ID],assignPublicIp=ENABLED}"
EOF
}



