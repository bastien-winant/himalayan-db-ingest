# Package the Lambda function code
data "archive_file" "lambda_deployment_package" {
  type        = "zip"
  source_file = "${path.module}/../../src/${var.lambda_package_file}"
  output_path = "${path.module}/src/${var.lambda_package_file}.zip"
}

# Load the deployment package to s3
resource "aws_s3_object" "lambda_deployment_package_object" {
  bucket = aws_s3_bucket.lambda_code_file.id
  key    = var.lambda_package_file
}

# Create log group for lambda function logs
resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/himaldb_lambda_function_log"
  retention_in_days = 14

  tags = {
    Environment = "production"
    Application = "example"
  }
}

# Lambda function
resource "aws_lambda_function" "lambda_function" {
  function_name = "himaldb_lambda_function"
  role = aws_iam_role.lambda_exec_role.arn
  runtime = "python3.9"
  handler = "lambda_function.handler"

  # Advanced logging configuration
  logging_config {
    log_format            = "JSON"
    application_log_level = "INFO"
    system_log_level      = "WARN"
  }

  environment {
    variables = {
      ENVIRONMENT = "production"
      LOG_LEVEL   = "info"
    }
  }

  tags = {
    Environment = "production"
    Application = "example"
  }
}