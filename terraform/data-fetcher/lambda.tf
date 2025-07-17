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