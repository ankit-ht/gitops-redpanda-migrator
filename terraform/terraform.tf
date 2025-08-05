terraform {
  backend "s3" {
    bucket = "myterraformbackupbucket"
    key = "envs/dev/terraform.tfstate"#path inside s3
    encrypt = true
    region = "us-east-1"
    dynamodb_table = "terraform-state-locking"
  }
}
