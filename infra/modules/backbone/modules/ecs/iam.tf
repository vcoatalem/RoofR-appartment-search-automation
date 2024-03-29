
data "aws_iam_policy" "task_execution_policy" {
  name = "AmazonECSTaskExecutionRolePolicy"
}

data "aws_iam_policy_document" "instance-assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = local.task_execution_role_name
  assume_role_policy = data.aws_iam_policy_document.instance-assume-role-policy.json
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = data.aws_iam_policy.task_execution_policy.arn
}

resource "aws_iam_user" "task_execution_user" {
  name = local.task_execution_user_name
}

resource "aws_iam_access_key" "task_execution_user_key" {
  user = aws_iam_user.task_execution_user.name
}

resource "aws_iam_user_policy" "task_execution_user_policy" {
  name = local.task_execution_user_policy_name
  user = aws_iam_user.task_execution_user.name
  policy = jsonencode({
    Version = "2012-10-17"
    "Statement" : [
      {
        "Sid" : "ECR",
        "Effect" : "Allow",
        "Action" : [
          "ecr:*"
        ],
        "Resource" : "*"
      },
      {
        "Sid" : "ECS",
        "Effect" : "Allow",
        "Action" : [
          "ecs:RunTask",
          "ecs:ListClusters"
        ],
        "Resource" : "*"
      },
      {
        "Sid" : "IAM",
        "Effect" : "Allow",
        "Action" : [
          "iam:PassRole"
        ],
        "Resource" : "*"
      }
    ]
  })
}
