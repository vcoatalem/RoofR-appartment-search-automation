output "dynamodb_table_name" {
  value = aws_dynamodb_table.table.name
}

output "iam_user_arn" {
  value = aws_iam_user.far_user.arn
}

output "iam_user_access_key_id" {
  value = aws_iam_access_key.far_user_key.id
}

output "iam_user_access_key_secret" {
  value = aws_iam_access_key.far_user_key.secret
}