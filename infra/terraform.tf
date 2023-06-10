terraform {

  required_version = ">= 1.4.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
  }

  backend "s3" {
    bucket = "tfstate-far"
    region = "eu-west-1"
    key="terraform.tfstate"
  }
}
