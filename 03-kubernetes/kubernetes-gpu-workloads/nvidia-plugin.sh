# Install NVIDIA device plugin via Helm
helm repo add nvdp https://nvidia.github.io/k8s-device-plugin
helm repo update

helm install nvidia-device-plugin nvdp/nvidia-device-plugin \
  --namespace kube-system \
  --set tolerations[0].key=dedicated \
  --set tolerations[0].operator=Equal \
  --set tolerations[0].value=gpu-training \
  --set tolerations[0].effect=NoSchedule \
  --set migStrategy=mixed   # Enable MIG support

# Verify the DaemonSet is running on GPU nodes
kubectl get ds nvidia-device-plugin-daemonset -n kube-system
kubectl get pods -n kube-system -l name=nvidia-device-plugin-ds -o wide
