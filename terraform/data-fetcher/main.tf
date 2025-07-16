provider "aws" {
  region = var.aws_region
}

# S3 bucket to hold the raw data
resource "aws_s3_bucket" "data_bucket" {
  bucket_prefix = var.data_bucket_prefix
  force_destroy = true

  tags = {
    Name        = "HIMDATA raw data bucket"
    Environment = "Prod"
  }
}

# IAM role for Lambda execution
data "aws_iam_policy_document" "assume_role" {
  # Allow the lambda service to assume this role
  statement {
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }

  # Allow role to write to the data bucket
  statement {
    actions = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.data_bucket.arn}/*"]
  }
}

resource "aws_iam_role" "example" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}