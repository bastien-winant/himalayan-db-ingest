# Virtual Private Network
resource "aws_vpc" "db_vpc" {
  cidr_block       = var.vpc_cidr_block
  instance_tenancy = "default"

  tags = {
    Name        = "The Himalayan DB"
    Environment = "Dev"
  }
}

# Private Subnet
resource "aws_subnet" "db_vpc_subnet" {
  vpc_id     = aws_vpc.db_vpc.id
  cidr_block = var.private_subnet_cidr_block
}

# Inbound Rule and Security Group
resource "aws_security_group" "db_vpc_sg" {
  vpc_id = aws_vpc.db_vpc.id
}

resource "aws_vpc_security_group_ingress_rule" "allow_tls_ipv6" {
  security_group_id = aws_security_group.db_vpc_sg.id
  ip_protocol       = "tcp"
  from_port         = 22
  to_port           = 22
  cidr_ipv4         = "0.0.0.0/0"
}