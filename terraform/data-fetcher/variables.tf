# Set the AWS region to EU Central (Frankfurt)
variable "region" {
  type = string
  default = "eu-central-1"
  description = "Region in which resources are to be deployed by default"
}

variable "code_bucket_prefix" {
  type = string
  default = "himaldb-lambda-code-"
  description = "Prefix for the S3 bucket holding the S3 lambda scripts"
}