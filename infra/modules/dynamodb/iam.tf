resource "aws_iam_user" "far_user" {
  name = "far-user"
}

resource "aws_iam_access_key" "far_user_key" {
  user = aws_iam_user.far_user.name
}

resource "aws_iam_user_policy" "script_user_policy" {
  name = "far-user-policy"
  user = aws_iam_user.far_user.name
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
