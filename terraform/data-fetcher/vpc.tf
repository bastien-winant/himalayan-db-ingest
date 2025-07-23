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
resource "aws_subnet" "db_vpc_private_subnets" {
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

resource "aws_vpc_security_group_ingress_rule" "allow_postgres_inbound" {
  security_group_id = aws_security_group.db_vpc_sg.id
  ip_protocol       = "tcp"
  from_port         = 5432
  to_port           = 5432
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_vpc_security_group_egress_rule" "allow_all_outbound" {
  security_group_id = aws_security_group.db_vpc_sg.id
  ip_protocol       = "-1"
  from_port         = 0
  to_port           = 0
  cidr_ipv4         = "0.0.0.0/0"
}