# virtual private network
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr_block
  instance_tenancy = "default"
}

# public subnet
resource "aws_subnet" "public_subnet" {
  vpc_id = aws_vpc.vpc.id
  cidr_block = var.vpc_public_cidr_block
  map_public_ip_on_launch = true
}

# private subnet that will host the database
resource "aws_subnet" "private_subnet" {
  vpc_id = aws_vpc.vpc.id
  cidr_block = var.vpc_private_cidr_block
}


resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "vpc_public_routing" {
  route_table_id = aws_route_table.route_table.id
  subnet_id = aws_subnet.public_subnet.id
}

# control traffic to and from the database
resource "aws_security_group" "db_sg" {
  name = "allow_"
  description = "Allow inbound traffic and outbound traffic"
  vpc_id = aws_vpc.vpc.id
}

# Inbound rule: allow SSH inbound traffic
resource "aws_vpc_security_group_ingress_rule" "allow_ssh_inbound" {
  security_group_id = aws_security_group.db_sg.id
  ip_protocol = "ssh"
  from_port = 22
  to_port = 22
}

# Allow all outbound traffic
resource "aws_vpc_security_group_egress_rule" "allow_all_outbound" {
  security_group_id = aws_security_group.db_sg.id
  from_port = 0
  to_port = 0
  ip_protocol = "-1"
}