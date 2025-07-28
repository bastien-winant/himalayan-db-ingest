# Package the Lambda function code
data "archive_file" "lambda_deployment_package" {
  type        = "zip"
  source_file = "${path.module}/../../src/${var.lambda_package_file}"
  output_path = "${path.module}/src/${var.lambda_package_file}"
}

# Load the deployment package to s3
resource "aws_s3_object" "lambda_deployment_package_object" {
  bucket = aws_s3_bucket.lambda_code_file.id
  key    = var.lambda_package_file
  source = "${path.module}/src/${var.lambda_package_file}"
}

# Create log group for lambda function logs
resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 14
}

# Lambda function
resource "aws_lambda_function" "lambda_function" {
  function_name    = var.lambda_function_name
  role             = aws_iam_role.lambda_exec_role.arn
  runtime          = "python3.9"
  handler          = "lambda_function.handler"
  source_code_hash = data.archive_file.lambda_deployment_package.output_base64sha256

  s3_bucket = aws_s3_object.lambda_deployment_package_object.bucket
  s3_key    = aws_s3_object.lambda_deployment_package_object.key

  # Advanced logging configuration
  logging_config {
    log_format            = "JSON"
    application_log_level = "INFO"
    system_log_level      = "WARN"
  }

  vpc_config {
    subnet_ids = var.private_subnets_cidr
    security_group_ids = [aws_security_group.lambda_vpc_sg.id]
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda_log_group,
    aws_s3_object.lambda_deployment_package_object
  ]
}