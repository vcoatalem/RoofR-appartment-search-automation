output "ecr_repository_url" {
  value = module.ecr.ecr_repository_url
}

output "ecr_repository_arn" {
  value = module.ecr.ecr_repository_arn
}

output "ecr_admin_user_key_id" {
    value = module.ecr.iam_user_access_key_id
}

output "ecr_admin_user_key_secret" {
  value = module.ecr.iam_user_access_key_secret
  sensitive = true
}

output "cloudwatch_task_log_group_name" {
  value = module.ecs.task_log_group_name
}

output "ecs_task_execution_role_arn" {
    value = module.ecs.ecs_task_execution_role_arn
}

output "ecs_cluster_arn" {
    value = module.ecs.ecs_cluster_arn
}

output "vpc_public_subnet_id" {
  value = module.vpc.public_subnets[0]
}

output "vpc_default_security_group_id" {
    value = module.vpc.default_security_group_id
}
