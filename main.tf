# main.tf - Infrastructure configuration

provider "aws" {
  region     = "us-east-1"
  access_key = "AKIAIOSFODNN7EXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

# Security group with overly permissive rules
resource "aws_security_group" "allow_all" {
  name        = "allow_all"
  description = "Allow all inbound traffic"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Open to the entire internet
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # SSH open to the world
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# S3 bucket with public access
resource "aws_s3_bucket" "data" {
  bucket = "my-company-sensitive-data"
  acl    = "public-read"  # Anyone can read this bucket
}

# RDS instance with weak settings
resource "aws_db_instance" "main" {
  identifier           = "production-db"
  engine               = "postgres"
  instance_class       = "db.t3.micro"
  username             = "admin"
  password             = "password123"  # Weak password hardcoded
  publicly_accessible  = true           # Database exposed to internet
  skip_final_snapshot  = true
  storage_encrypted    = false          # No encryption at rest
}
