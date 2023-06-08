
# Configure AWS provider
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      "Terraform" : true
      "App Name" : var.application_name
    }
  }
}