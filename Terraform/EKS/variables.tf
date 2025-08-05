variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "cluster_name" {
  type    = string
  default = "demo-cluster"
}

variable "kubernetes_version" {
  type    = string
  default = "1.29"
}
