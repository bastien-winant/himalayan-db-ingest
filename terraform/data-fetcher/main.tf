provider "aws" {
  region = var.aws_region
}

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

# IAM trust policy for Lambda (allow Lambda to assume a role)
data "aws_iam_policy_document" "lambda_assume_policy" {
  statement {
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Create an IAM role that Lamda is trusted to assume
resource "aws_iam_role" "lambda_exec_role" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_policy.json
}

# Policy document with write access to the S3 data bucket
data "aws_iam_policy_document" "lambda_permissions" {
  # Allow role to write to the data bucket
  statement {
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.data_bucket.arn}/*"]
  }
}

# Create an IAM policy with the S3 write policy document
resource "aws_iam_policy" "lambda_policy" {
  name   = "lambda_data_write_policy"
  policy = data.aws_iam_policy_document.lambda_permissions.json
}

# Attach the S3 policy to the Lambda-trusted role
resource "aws_iam_role_policy_attachment" "attach_lambda_policy" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# create archive file for the Python script
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../lambda"
  output_path = "${path.module}/lambda_function.zip"
}

# store the lambda package to s3
resource "aws_s3_object" "lambda_code_object" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "lambda_function.zip"
  source = data.archive_file.lambda_zip.output_path
  etag   = filemd5(data.archive_file.lambda_zip.output_path)
}

# Create Lambda function from S3 object
resource "aws_lambda_function" "fetch_function" {
  function_name = "lambda_function"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  timeout       = 600

  s3_bucket = aws_s3_bucket.code_bucket.bucket
  s3_key    = aws_s3_object.lambda_code_object.key

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  # Advanced logging configuration
  logging_config {
    log_format            = "JSON"
    application_log_level = "INFO"
    system_log_level      = "WARN"
  }
}