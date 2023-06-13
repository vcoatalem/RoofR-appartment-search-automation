locals {
  prefix = "far"
}

module "backbone" {
  source     = "./modules/backbone"
  aws_region = var.aws_region
  app_name     = local.prefix
}


module "worker" {
  for_each = var.contacts

  source     = "./modules/worker"
  aws_region = var.aws_region
  app_name     = "${local.prefix}_4_${each.key}"

  user_props = each.value

  vpc_subnet_id = module.backbone.vpc_public_subnet_id
  vpc_default_security_group_id = module.backbone.vpc_default_security_group_id

  ecs_task_execution_role_arn = module.backbone.ecs_task_execution_role_arn
  ecs_cluster_arn = module.backbone.ecs_cluster_arn
  cloudwatch_task_log_group_name = module.backbone.cloudwatch_task_log_group_name

  ecr_repository_url = module.backbone.ecr_repository_url
  ecr_repository_arn = module.backbone.ecr_repository_arn
}


resource "local_file" "push_to_registry_script" {
  for_each = var.contacts
  filename        = "${path.root}/generated-scripts/push-${each.key}.sh"
  file_permission = "744"
  content         = <<EOF
export AWS_ACCESS_KEY_ID=${module.backbone.ecr_admin_user_key_id}
export AWS_SECRET_ACCESS_KEY=${module.backbone.ecr_admin_user_key_secret}
export AWS_DEFAULT_REGION=${var.aws_region}
AWS_ECR_URL=${module.backbone.ecr_repository_url}
IMAGE_NAME=${each.key}

aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ECR_URL
cd ${path.root}/..
docker build . -t $IMAGE_NAME -f Dockerfile
docker tag $IMAGE_NAME $AWS_ECR_URL:$IMAGE_NAME
docker push $AWS_ECR_URL:$IMAGE_NAME
EOF
}

/*
resource "local_file" "run_task_script" {
  filename        = "${path.root}/generated-scripts/test-dariatolo.sh"
  file_permission = "744"
  content         = <<EOF
export AWS_ACCESS_KEY_ID=${module.ecs.iam_user_access_key_id}
export AWS_SECRET_ACCESS_KEY=${module.ecs.iam_user_access_key_secret}
export AWS_DEFAULT_REGION=${var.aws_region}

AWS_CLUSTER_NAME=${module.backbone.cluster_name}
TASK_NAME=${module.}
TASK_DEFINITION_REVISION=${aws_ecs_task_definition.task_definition.revision}

SUBNET_ID=${module.vpc.public_subnets[0]}
SECURITY_GROUP_ID=${module.vpc.default_security_group_id}

aws ecs run-task --launch-type FARGATE \
    --cluster $AWS_CLUSTER_NAME \
    --task-definition $TASK_NAME:$TASK_DEFINITION_REVISION \
    --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_ID],securityGroups=[$SECURITY_GROUP_ID],assignPublicIp=ENABLED}"
EOF
}
*/



