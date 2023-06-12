terraform {

  required_version = ">= 1.4.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
    
  }

  cloud {
    organization = "victorcoatalem"

    workspaces {
      name = "example-workspace"
    }
  }
  /*
  backend "s3" {
    bucket = "tfstate-far"
    dynamodb_table = "tfstate.lock"
    region = "eu-west-1"
    key    = "terraform.tfstate"
    encrypt = true
  }*/
}
