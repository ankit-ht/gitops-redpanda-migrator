

resource "aws_s3_bucket" "tf_state" {
  bucket = "eks-terraform-state-ht"  # must be globally unique
  force_destroy = true

  tags = {
    Name        = "Terraform State Bucket"
    Environment = "dev"
  }
}

resource "aws_s3_bucket_versioning" "tf_state_versioning" {
  bucket = aws_s3_bucket.tf_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "tf_lock" {
  name           = "terraform-lock-table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "Terraform Lock Table"
    Environment = "dev"
  }
}

terraform {
   backend "s3" {
   bucket         = "eks-terraform-state-ht"
   key            = "global/s3/terraform.tfstate"
   region         = "us-east-1"
   encrypt        = true
  }
}
