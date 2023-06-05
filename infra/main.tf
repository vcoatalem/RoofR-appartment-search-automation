/*
*
*    VARIABLES
*
*/

variable "aws_region" {
    description = "aws region to deploy infrastructure into"
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

variable "form_email" {
  description = ".env.FROM_EMAIL"
}

variable "form_name" {
  description = ".env.NAME"
}

variable "form_phone" {
  description = ".env.PHONE"
}

variable "aws_access_key" {
  description = ".env.AWS_ACCESS_KEY_ID"
}

variable "aws_access_key_secret" {
  description = ".env.AWS_SECRET_ACCESS_KEY"
}


/*
*
*    Provider
*
*/

# Configure AWS provider
provider "aws" {
  region = var.aws_region
}

/*
*
*    RESOURCES
*
*/

# Create DynamoDB table
resource "aws_dynamodb_table" "table" {
  name           = var.table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"
  attribute {
    name = "id"
    type = "S"
  }
  attribute {
    name = "url"
    type = "S"
  }
  global_secondary_index {
    name               = "urlIndex"
    hash_key           = "url"
    projection_type    = "ALL"
    read_capacity      = 5
    write_capacity     = 5
  }
}

# Create ECS cluster
resource "aws_ecs_cluster" "cluster" {
  name = var.cluster_name
}

# Create ECR repository
resource "aws_ecr_repository" "repository" {
  name = var.repository_name
}

# Create a CloudWatch Logs Group for ECS task logs
resource "aws_cloudwatch_log_group" "ecs_task_logs" {
  name              = "/ecs/${var.image_name}"
  retention_in_days = 7  # Define the number of days to retain the logs (adjust as needed)

  tags = {
    Name = "${var.image_name} job task logs"
  }
}


# Create ECS task definition
resource "aws_ecs_task_definition" "task_definition" {
  family                   = "${var.task_name}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = "arn:aws:iam::601899071982:role/ecsTaskExecutionRole"
  container_definitions    = <<-DEFINITION
[
  {
    "name": "${var.image_name}",
    "image": "${aws_ecr_repository.repository.repository_url}:latest",
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
        "value": "${var.form_email}"
      },
      {
        "name": "NAME",
        "value": "${var.form_name}"
      },
      {
        "name": "PHONE",
        "value": "${var.form_phone}"
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
        "awslogs-group": "${aws_cloudwatch_log_group.ecs_task_logs.name}",
        "awslogs-region": "${var.aws_region}",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }
]
  DEFINITION
}

# TODO: something missing on VPC to make fargate tasks able to fetch ecr (gateway ? routing ?)

# Create a VPC
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "FAR-vpc"
  }
}

# Create an internet gateway
resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.my_vpc.id

  tags = {
    Name = "FAR-igw"
  }
}

# Create a public subnet
resource "aws_subnet" "my_public_subnet" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "FAR-public-subnet"
  }
}

resource "aws_route_table" "my_route_table" {
  vpc_id = aws_vpc.my_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my_igw.id
  }

  tags = {
    Name = "FAR-route-table"
  }
}

resource "aws_route_table_association" "my_route_table_association" {
  subnet_id      = aws_subnet.my_public_subnet.id
  route_table_id = aws_route_table.my_route_table.id
}

# Create a security group allowing all inbound/outbound traffic
resource "aws_security_group" "my_security_group" {
  name = "FAR-security-group"
  vpc_id = aws_vpc.my_vpc.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "FAR-security-group"
  }
}


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
  arn       = aws_ecs_cluster.cluster.arn#aws_ecs_task_definition.task_definition.arn
  role_arn = "arn:aws:iam::601899071982:role/ecsTaskExecutionRole"
  ecs_target {
    task_count = 1
    task_definition_arn = aws_ecs_task_definition.task_definition.arn
    launch_type = "FARGATE"
    network_configuration {
      subnets = ["${aws_subnet.my_public_subnet.id}"] 
      security_groups = ["${aws_security_group.my_security_group.id}"] 
      assign_public_ip = true
    }
  }
}

# Output the ECS cluster and task information
output "cluster_name" {
  value = aws_ecs_cluster.cluster.name
}

output "repository_url" {
  value = aws_ecr_repository.repository.repository_url
}

output "task_definition_arn" {
  value = aws_ecs_task_definition.task_definition.arn
}
