# Virtual Private Network
resource "aws_vpc" "db_vpc" {
  cidr_block       = var.vpc_cidr_block
  instance_tenancy = "default"

  tags = {
    Name        = "The Himalayan DB"
    Environment = "Dev"
  }
}

# Private Subnets
resource "aws_subnet" "public" {
  count             = length(var.private_subnets_cidr)
  vpc_id            = aws_vpc.db_vpc.id
  cidr_block        = element(var.private_subnets_cidr, count.index)
  availability_zone = element(var.availability_zones, count.index)

  tags = {
    Name = "Subnet-${count.index + 1}"
  }
}

# Inbound Rule and Security Group
resource "aws_security_group" "db_vpc_sg" {
  vpc_id = aws_vpc.db_vpc.id
}

resource "aws_vpc_security_group_ingress_rule" "allow_tls_ipv6" {
  security_group_id = aws_security_group.db_vpc_sg.id
  ip_protocol       = "tcp"
  from_port         = 5432
  to_port           = 5432
  cidr_ipv4         = "0.0.0.0/0"
}