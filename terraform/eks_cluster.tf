# eks-cluster.tf
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.8.5"

  cluster_name                   = var.cluster_name
  cluster_version                = var.kubernetes_version
  cluster_endpoint_public_access = true
  enable_irsa                    = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    main = {
      name            = "node-group"
      instance_types  = ["t3.medium"]
      min_size        = 1
      max_size        = 2
      desired_size    = 1
      capacity_type   = "ON_DEMAND"
      ami_type        = "AL2_x86_64"
      disk_size       = 20

      # Required for security group rules
      cluster_primary_security_group_id = module.eks.cluster_primary_security_group_id

      tags = {
        Environment = "demo"
      }
    }
  }

  node_security_group_additional_rules = {
    ingress_self_all = {
      description = "Node to node all ports/protocols"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      type        = "ingress"
      self        = true
    }
    egress_all = {
      description      = "Node all egress"
      protocol         = "-1"
      from_port        = 0
      to_port          = 0
      type             = "egress"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }
  }

  tags = {
    Environment = "dev"
  }
}