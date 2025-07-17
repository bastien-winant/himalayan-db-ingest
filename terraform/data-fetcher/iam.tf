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
data "aws_iam_policy_document" "lambda_permission" {
  # Allow role to write to the data bucket
  statement {
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.data_bucket.arn}/*"]
  }

  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

# Create an IAM policy with the S3 write policy document
resource "aws_iam_policy" "lambda_policy" {
  name   = "lambda_data_write_policy"
  policy = data.aws_iam_policy_document.lambda_permission.json
}

# Attach the S3 policy to the Lambda-trusted role
resource "aws_iam_role_policy_attachment" "attach_lambda_policy" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}