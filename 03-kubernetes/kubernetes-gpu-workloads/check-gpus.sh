# Check GPU resources available on nodes
kubectl describe node gpu-node-01 | grep -A5 "Allocatable:"
# Output:
# Allocatable:
#   cpu:                          96
#   memory:                       755Gi
#   nvidia.com/gpu:               8      ← 8 GPUs available
#   pods:                         110

# Check current GPU allocation across the cluster
kubectl get nodes -o custom-columns=\
"NAME:.metadata.name,\
GPU-CAP:.status.capacity.nvidia\.com/gpu,\
GPU-ALLOC:.status.allocatable.nvidia\.com/gpu"
