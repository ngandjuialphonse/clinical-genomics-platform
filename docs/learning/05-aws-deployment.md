# Learning Module 5: AWS Deployment with Terraform

This module explains how we deploy our platform to AWS using Terraform.

## Why Terraform?

Terraform is an Infrastructure as Code (IaC) tool that allows us to define and manage our cloud infrastructure in a declarative way. Instead of clicking around in the AWS console, we write code to describe our desired state.

**Benefits:**
-   **Reproducibility:** We can create identical environments (dev, staging, prod) from the same code.
-   **Automation:** Infrastructure changes can be automated and integrated into our CI/CD pipeline.
-   **Version Control:** Our infrastructure is versioned in Git, just like our application code.

## Our Terraform Structure

Our Terraform code is organized into modules for reusability:

-   **`environments/dev/`**: The root module for our development environment. It calls the other modules.
-   **`modules/vpc/`**: Creates a Virtual Private Cloud (VPC) with public and private subnets.
-   **`modules/rds/`**: Creates a PostgreSQL database using Amazon RDS.
-   **`modules/ecs/`**: Creates an Amazon ECS (Elastic Container Service) cluster to run our Docker containers.

## Deployment Strategy

We are using **AWS Fargate**, a serverless compute engine for containers. This means we don't have to manage any EC2 instances ourselves—AWS handles the underlying infrastructure.

**The deployment process:**
1.  The CI/CD pipeline builds our Docker images and pushes them to Amazon ECR (Elastic Container Registry).
2.  Terraform creates the ECS cluster, task definitions (which point to our ECR images), and services.
3.  ECS pulls the images from ECR and runs them as containers.
4.  An Application Load Balancer (ALB) is used to route traffic to our API and dashboard.

