# Set the AWS region to EU Central (Frankfurt)
variable "region" {
  type        = string
  default     = "eu-central-1"
  description = "Region in which resources are to be deployed by default"
}

variable "availability_zones" {
  type        = list(string)
  default     = ["eu-central-1a", "eu-central-1b"]
  description = "AZs in which resources are to be deployed by default"
}

variable "code_bucket_prefix" {
  type        = string
  default     = "himaldb-lambda-code-"
  description = "Prefix for the S3 bucket holding the S3 lambda scripts"
}

variable "lambda_function_name" {
  type    = string
  default = "himaldb_lambda_function"
}

variable "lambda_package_file" {
  type    = string
  default = "lambda_function.zip"
}

variable "vpc_cidr_block" {
  type        = string
  default     = "192.168.0.0/16"
  description = "IPv4 CIDR block for the database VPC"
}

variable "private_subnets_cidr" {
  type    = list(string)
  default = ["192.168.1.0/24", "192.168.2.0/24"]
}