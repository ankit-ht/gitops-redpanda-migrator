resource "aws_s3_bucket" "redpanda-config" {
  bucket = "redpanda-config"

  tags = {
    Name        = "redpanda-config"
    Environment = "dev"
  }
}