# S3 bucket to hold the raw data
resource "aws_s3_bucket" "data_bucket" {
  bucket_prefix = var.data_bucket_prefix
  force_destroy = true

  tags = {
    Name        = "Raw data bucket"
    Environment = "Prod"
  }
}

# S3 bucket to hold the Lambda scripts
resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = var.code_bucket_prefix
  force_destroy = true

  tags = {
    Name        = "Lambda code bucket"
    Environment = "Prod"
  }
}