terraform {
  backend "s3" {
    bucket = "myterraformbackupbucket"
    key = "envs/dev/terraform.tfstate"#path inside s3
    encrypt = true
    region = "us-east-1"
    dynamodb_table = "terraform-state-locking"
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locking"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "Terraform State Lock Table"
    Environment = "dev"
  }
}
