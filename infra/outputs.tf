# Output the ECS cluster and task information
output "cluster_id" {
  value = module.ecs_ecr.ecs_cluster_id
}

output "repository_id" {
  value = module.ecs_ecr.ecr_repository_id
}

output "task_definition_arn" {
  value = aws_ecs_task_definition.task_definition.arn
}
