terraform {
  required_providers {
    random = {
      source = "hashicorp/random"
    }
    aws = {
      source = "hashicorp/aws"
    }
    local = {
      source = "hashicorp/local"
    }
  }
}