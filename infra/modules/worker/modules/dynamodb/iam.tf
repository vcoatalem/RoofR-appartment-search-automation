resource "aws_iam_user" "dynamodb_user" {
  name = local.user_name
}

resource "aws_iam_access_key" "dynamodb_user_key" {
  user = aws_iam_user.dynamodb_user.name
}

resource "aws_iam_user_policy" "dynamodb_user_policy" {
  name = local.policy_name
  user = aws_iam_user.dynamodb_user.name
  policy = jsonencode({
    Version = "2012-10-17"
    "Statement" : [
      {
        "Sid" : "ListAndDescribe",
        "Effect" : "Allow",
        "Action" : [
          "dynamodb:List*",
          "dynamodb:DescribeReservedCapacity*",
          "dynamodb:DescribeLimits",
          "dynamodb:DescribeTimeToLive"
        ],
        "Resource" : "*"
      },
      {
        "Sid" : "SpecificTable",
        "Effect" : "Allow",
        "Action" : [
          "dynamodb:BatchGet*",
          "dynamodb:DescribeStream",
          "dynamodb:DescribeTable",
          "dynamodb:Get*",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWrite*",
          "dynamodb:Delete*",
          "dynamodb:Update*",
          "dynamodb:PutItem"
        ],
        "Resource" : "*"
      }
    ]
  })
}
