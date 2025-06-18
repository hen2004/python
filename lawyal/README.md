# LAWYAL DevOps Assignment - Deployment Guide

This README walks you through provisioning, containerizing, and deploying a Flask application to AWS EKS using Terraform, Docker, Helm, and ECR. It follows best practices in terms of ordering, permissions, and resource dependencies.

---

## 📦 Prerequisites
- AWS CLI configured (`aws configure`)
- Docker installed
- kubectl and Helm installed
- Terraform v1.5+

---

## 🚀 Step-by-Step Deployment Guide

### 1️⃣ Terraform Setup

#### a. Create Terraform backend S3 bucket using Terraform
Since Terraform needs the S3 bucket before using it as a backend, create it with a targeted apply:
```bash
# Temporarily disable backend.tf if it exists
mv backend.tf backend.tf.disabled

# Initialize Terraform
terraform init

# Apply only the S3 bucket and its versioning
terraform apply -target=aws_s3_bucket.tf_state -target=aws_s3_bucket_versioning.tf_state_versioning
```

#### b. Enable the S3 backend
```bash
# Restore backend.tf with the correct bucket name
# backend.tf:
terraform {
  backend "s3" {
    bucket = "lawyal-terraform-state-20250618"
    key    = "eks/terraform.tfstate"
    region = "us-east-1"
  }
}

# Re-initialize with the remote backend
terraform init -reconfigure
```

#### c. Apply full infrastructure
```bash
terraform apply
```
This provisions:
- S3 backend (if not already)
- VPC with public/private subnets
- EKS Cluster
- ECR repository
- IAM roles
- Node groups

#### d. Configure kubectl access
```bash
aws eks update-kubeconfig --region us-east-1 --name lawyal-eks-cluster
kubectl get nodes
```

---

### 2️⃣ Dockerize Flask App

#### a. Create `app.py` (example):
```python
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello from LAWYAL!"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

#### b. Dockerfile
```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY app.py /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

#### c. requirements.txt
```
flask
```

#### d. Build and test locally (optional)
```bash
docker build -t lawyal-app ./app
docker run -p 5000:5000 lawyal-app
```

---

### 3️⃣ Push Image to AWS ECR

#### a. Authenticate to ECR
```bash
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin 768997460089.dkr.ecr.us-east-1.amazonaws.com
```

#### b. Tag and push
```bash
docker tag lawyal-app:latest 768997460089.dkr.ecr.us-east-1.amazonaws.com/lawyal-app:latest
docker push 768997460089.dkr.ecr.us-east-1.amazonaws.com/lawyal-app:latest
```

---

### 4️⃣ Deploy Using Helm

#### a. Navigate to Helm chart directory
```bash
cd helm/lawyal-app
```

#### b. Install
```bash
kubectl create namespace lawyal || true
helm install lawyal-app . --namespace lawyal
```

#### c. Get public endpoint
```bash
kubectl get svc -n lawyal
```
Visit the `EXTERNAL-IP` in your browser to see your app.

---

## ✅ Outputs (from Terraform)
- Cluster name
- Cluster endpoint
- ECR repo URL
- IAM role ARN

---

## 💡 Notes
- `aws-auth` ConfigMap was applied manually to avoid Terraform conflicts.
- Order of operations matters — especially with backend creation and ECR availability before pushing.
- We used `terraform apply -target=...` for the S3 bucket before configuring the backend.

---

## 🧩 Next Steps
- Automate deployments with GitHub Actions
- Add monitoring (bonus)

---

🍀 Good luck and enjoy deploying like a pro!

