# variables.tf
variable "kubernetes_version" {
  default     = "1.28"
  description = "EKS Kubernetes version"
  type        = string
}

variable "vpc_cidr" {
  default     = "10.0.0.0/16"
  description = "VPC CIDR range"
  type        = string
}

variable "aws_region" {
  default     = "us-east-1"
  description = "AWS region"
  type        = string
}

variable "cluster_name" {
  default     = "demo-eks"
  description = "EKS cluster name"
  type        = string
}