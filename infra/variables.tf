variable "aws_region" {
  description = "aws region to deploy infrastructure into"
}

variable "contacts" {
  type        = map(object({
    from_key = string
    from_email = string
    from_name = string
    from_phone = string
    from_message = string
  }))
  description = "⚠️ Users contact informations ⚠️"
}
