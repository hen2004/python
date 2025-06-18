terraform {
  backend "s3" {
    bucket = "lawyal-terraform-state-20250618"
    key    = "eks/terraform.tfstate"
    region = "us-east-1"
  }
}
