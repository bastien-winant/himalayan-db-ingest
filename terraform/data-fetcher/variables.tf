variable "aws_region" {
  type        = string
  default     = "eu-central-1" # Set the AWS region to EU Central (Frankfurt)
  description = "Overall region to host the project resources"
}

variable "data_bucket_prefix" {
  type        = string
  default     = "himaldb-data-"
  description = "Data S3 bucket name prefix"
}

variable "code_bucket_prefix" {
  type        = string
  default     = "himaldb-code-"
  description = "Code S3 bucket name prefix"
}