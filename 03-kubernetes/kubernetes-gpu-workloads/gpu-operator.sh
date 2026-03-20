# Install GPU Operator (includes device plugin, driver installer, DCGM)
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update

helm install gpu-operator nvidia/gpu-operator \
  --namespace gpu-operator \
  --create-namespace \
  --set driver.enabled=true \
  --set driver.version="550.90.07" \
  --set toolkit.enabled=true \
  --set devicePlugin.enabled=true \
  --set dcgm.enabled=true \
  --set dcgmExporter.enabled=true \
  --set gfd.enabled=true \
  --set migManager.enabled=true

# Watch the operator install components on GPU nodes
kubectl get pods -n gpu-operator -w

# Verify GPU operator status
kubectl get clusterpolicy gpu-cluster-policy -o yaml | grep -A20 "status:"
