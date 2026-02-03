provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "../../modules/vpc"

  project_name = var.project_name
  environment  = var.environment
  vpc_cidr     = var.vpc_cidr
}

module "rds" {
  source = "../../modules/rds"

  project_name          = var.project_name
  environment           = var.environment
  vpc_id                = module.vpc.vpc_id
  private_subnets       = module.vpc.private_subnets
  db_instance_class     = var.db_instance_class
  db_allocated_storage  = var.db_allocated_storage
  db_username           = var.db_username
  db_password           = var.db_password
}

module "ecs" {
  source = "../../modules/ecs"

  project_name      = var.project_name
  environment       = var.environment
  vpc_id            = module.vpc.vpc_id
  public_subnets    = module.vpc.public_subnets
  api_image_url     = var.api_image_url
  dashboard_image_url = var.dashboard_image_url
  database_url      = module.rds.db_url
}
