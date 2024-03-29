output "ecs_cluster_id" {
  value = aws_ecs_cluster.cluster.id
}

output "ecs_cluster_arn" {
  value = aws_ecs_cluster.cluster.arn
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.cluster.name
}

output "cloudwatch_logs_id" {
  value = aws_cloudwatch_log_group.ecs_task_logs.id
}

output "task_log_group_name" {
  value = aws_cloudwatch_log_group.ecs_task_logs.name
}

output "ecs_task_execution_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}

output "iam_user_access_key_id" {
  value = aws_iam_access_key.task_execution_user_key.id
}

output "iam_user_access_key_secret" {
  value = aws_iam_access_key.task_execution_user_key.secret
  sensitive = true
}