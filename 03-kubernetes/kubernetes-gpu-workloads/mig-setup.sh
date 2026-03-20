# Enable MIG mode on an A100 (requires node drain first)
kubectl drain gpu-node-01 --ignore-daemonsets --delete-emptydir-data

# SSH to the node and configure MIG
nvidia-smi -mig 1                              # Enable MIG mode (requires reboot)
nvidia-smi mig -cgi 3g.40gb,3g.40gb -C        # Create 2x 3g.40gb instances on A100-80GB
nvidia-smi mig -lgi                            # List GPU instances

# Label the node with its MIG profile
kubectl label node gpu-node-01 nvidia.com/mig.strategy=mixed

# The GPU Operator's MIG manager handles profile configuration:
# Add annotation to node to set desired MIG config
kubectl annotate node gpu-node-01 \
  nvidia.com/mig-config=all-3g.40gb \
  --overwrite

# In pod specs, request specific MIG profiles:
# resources:
#   limits:
#     nvidia.com/mig-3g.40gb: 1    # Request a 3g.40gb MIG instance
