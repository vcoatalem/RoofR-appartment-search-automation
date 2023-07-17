output "dynamodb_admin_user_key_id" {
  value = module.dynamodb.iam_user_access_key_id
}

output "dynamodb_admin_user_key_secret" {
  value = module.dynamodb.iam_user_access_key_secret
}

output "task_name" {
  value = module.task_definition.task_name
}