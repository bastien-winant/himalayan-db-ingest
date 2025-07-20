variable "aws_region" {
  type        = string
  default     = "eu-central-1" # Set the AWS region to EU Central (Frankfurt)
  description = "Overall region to host the project resources"
}

variable "code_bucket_prefix" {
  type        = string
  default     = "himaldb-code-"
  description = "Code S3 bucket name prefix"
}

variable "vpc_cidr_block" {
  type = string
  default = "192.168.0.0/16"
  description = "Address range for the VPC"
}

variable "vpc_public_cidr_block" {
  type = string
  default = "192.168.1.0/24"
}

variable "vpc_private_cidr_block" {
  type = string
  default = "192.168.2.0/24"
}