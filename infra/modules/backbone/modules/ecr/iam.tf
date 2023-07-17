resource "aws_iam_user" "registry_admin" {
  name = local.repository_admin_user_name
}

resource "aws_iam_access_key" "registry_admin_user_key" {
  user = aws_iam_user.registry_admin.name
}

resource "aws_iam_user_policy" "registry_admin_policy" {
  name = local.repository_admin_user_policy_name
  user = aws_iam_user.registry_admin.name
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
      }
    ]
  })
}
