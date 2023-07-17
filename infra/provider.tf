# Configure AWS provider
provider "aws" {
  region = var.aws_region

  shared_credentials_files = ["./.aws.credentials"]
  default_tags {
    tags = {
      "Terraform" : true
      "Purpose" : local.prefix
    }
  }
}