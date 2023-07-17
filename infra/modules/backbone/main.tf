module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = local.vpc_name

  cidr = "10.0.0.0/16"

  azs = ["${var.aws_region}a"]

  public_subnets      = ["10.0.1.0/24"]
  public_subnet_names = [local.vpc_subnet_name]

  create_igw = true


  default_security_group_name = "default: do not use"
  default_security_group_egress = [
    {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = "0.0.0.0/0"
    }
  ]
  default_security_group_ingress = [
    {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = "0.0.0.0/0"
    }
  ]
}
/* 
module "dynamodb" {
  source     = "./modules/dynamodb"
  aws_region = var.aws_region
} */

module "ecr" {
  source     = "./modules/ecr"
  aws_region = var.aws_region
  backbone_prefix = local.prefix
}

module "ecs" {
  source     = "./modules/ecs"
  aws_region = var.aws_region
  backbone_prefix = local.prefix
}