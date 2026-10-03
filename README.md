# Dynatrace and Istio 📈

This workload combines Dynatrace observability with Istio service mesh on Amazon EKS to improve workload visibility and service security. Kubernetes manifests and Python diagnostic scripts support deployment checks and troubleshooting, with Istio providing a foundation for mTLS, smoke testing, and traffic control.

# Dynatrace Install 🖥️
```bash
helm install dynatrace-operator oci://public.ecr.aws/dynatrace/dynatrace-operator \
--set "csidriver.enabled=false" \
--create-namespace \
--namespace dynatrace \
--rollback-on-failure
```

# Update kubeconfig ☁️
```bash
aws eks update-kubeconfig \
  --region us-east-1 \
  --name aws-eks-cluster
```

# Istio Service mesh 
This service provides your workloads with additional 

- Observability 🔭
- mTLS 🔐
- Traffic Control 🎛️
- Policy Enforcement and Security 
- Smoke Test 
  
# Installing Istio Service Mesh with helm ☸️

```bash
helm repo add istio https://istio-release.storage.googleapis.com/charts

helm repo update 
```
# Creating namespace and installing istio base chart and pod 📈

```bash
kubectl create namespace istio-system

# Install CRDS 
helm install istio-base istio/base -n istio-system 

# Install control plane
helm install istiod istio/istiod -n istio-system
```

# Label workloads namespace for Istio Enforcement 
```bash
kubectl label namespace nginx istio-injection=enabled --overwrite
```

# Uninstall istio service-mesh and remove ns label 
```bash
kubectl label namespace nginx istio-injection=enabled-

kubectl get ns -L istio-injection 

helm uninstall istio-base istio/base -n istio-system 

helm uninstall istiod istio/istiod -n istio-system
```

# Terraform 🏗️
```bash
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

Verify Dynakubes 
```bash
kubectl get dynakubes -n dynatrace
```
