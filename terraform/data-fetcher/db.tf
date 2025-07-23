resource "aws_db_subnet_group" "vpc_db_subnet_group" {
  subnet_ids = [
    aws_subnet.db_vpc_private_subnets[0].id,
    aws_subnet.db_vpc_private_subnets[1].id]

  tags = {
    Name = "My DB subnet group"
  }
}

resource "aws_db_instance" "db" {
  allocated_storage    = 10
  db_name              = "himaldb"
  engine               = "postgres"
  engine_version       = "17.5"
  instance_class       = "db.t3.micro"
  username             = "postgres"
  password             = "postgres"
  db_subnet_group_name = aws_db_subnet_group.vpc_db_subnet_group.name
  port                 = 5432
  publicly_accessible  = false
  skip_final_snapshot = true
  apply_immediately = true
}