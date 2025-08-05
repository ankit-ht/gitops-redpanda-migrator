terraform {
  backend "s3" {
    bucket = "myterraformbackupbucket"
    key = "envs/dev/terraform.tfstate"
    encrypt = true
    region = "us-east-1"
    dynamodb_table = "terraform-state-locking"
  }
}
