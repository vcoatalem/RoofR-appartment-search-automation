output "ecs_cluster_id" {
  value = aws_ecs_cluster.cluster.id
}

output "ecs_cluster_arn" {
  value = aws_ecs_cluster.cluster.arn
}

output "ecr_repository_id" {
  value = aws_ecr_repository.repository.id
}

output "ecr_repository_url" {
  value = aws_ecr_repository.repository.repository_url
}

output "cloudwatch_logs_id" {
    value = aws_cloudwatch_log_group.ecs_task_logs.id
}

output "task_log_group_name" {
  value = aws_cloudwatch_log_group.ecs_task_logs.name
}

output "ecs_task_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}
