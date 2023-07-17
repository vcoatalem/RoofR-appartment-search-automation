

module "dynamodb" {
  source        = "./modules/dynamodb"
  worker_prefix = local.prefix
  aws_region    = var.aws_region
}

module "task_definition" {
  source     = "./modules/task_definition"
  aws_region = var.aws_region

  worker_prefix = local.prefix

  from_key     = var.user_props.from_key
  from_email   = var.user_props.from_email
  from_name    = var.user_props.from_name
  from_phone   = var.user_props.from_phone
  from_message = var.user_props.from_message

  cloudwatch_task_log_group_name = var.cloudwatch_task_log_group_name

  ecs_task_execution_role_arn = var.ecs_task_execution_role_arn
  ecs_cluster_arn = var.ecs_cluster_arn
  ecr_repository_arn = var.ecr_repository_arn
  ecr_repository_url = var.ecr_repository_url

  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  dynamodb_user_key_id = module.dynamodb.iam_user_access_key_id
  dynamodb_user_key_secret = module.dynamodb.iam_user_access_key_secret

  vpc_default_security_group_id = var.vpc_default_security_group_id
  vpc_subnet_id = var.vpc_subnet_id
}