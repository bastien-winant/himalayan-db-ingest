resource "aws_s3_bucket" "lambda_code_file" {
  bucket_prefix = var.code_bucket_prefix
  force_destroy = true

  tags = {
    Name        = "The Himalayan DB"
    Environment = "Dev"
  }
}