output "vpc_id" {
  value = aws_vpc.my_vpc.id
}

output "public_subnet_id" {
  value = aws_subnet.my_public_subnet.id
}

output "security_group_id" {
  value = aws_security_group.my_security_group.id
}