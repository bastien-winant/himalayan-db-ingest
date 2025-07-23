# Set the AWS region to EU Central (Frankfurt)
variable "region" {
  type        = string
  default     = "eu-central-1"
  description = "Region in which resources are to be deployed by default"
}

variable "code_bucket_prefix" {
  type        = string
  default     = "himaldb-lambda-code-"
  description = "Prefix for the S3 bucket holding the S3 lambda scripts"
}

variable "vpc_cidr_block" {
  type        = string
  default     = "192.168.0.0/16"
  description = "IPv4 CIDR block for the database VPC"
}

variable "private_subnet_cidr_block" {
  type        = string
  default     = "192.168.1.0/24"
  description = "IPv4 CIDR block for the private VPC subnet"
}