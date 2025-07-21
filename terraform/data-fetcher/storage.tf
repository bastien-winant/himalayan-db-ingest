# S3 bucket to hold the Lambda scripts
resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = var.code_bucket_prefix
  force_destroy = true

  tags = {
    Name        = "Lambda code bucket"
    Environment = "Prod"
  }
}