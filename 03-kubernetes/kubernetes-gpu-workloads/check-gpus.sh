#!/usr/bin/env bash
# check-gpus.sh — Inspect GPU capacity and current allocation across the cluster
#
# CAPACITY vs ALLOCATABLE:
#   Capacity    — total hardware resources on the node (raw count from the OS)
#   Allocatable — Capacity minus resources reserved for system daemons
#                 (kubelet, kube-proxy, OS processes). This is what pods can use.
#
# For GPUs, Capacity and Allocatable are usually identical because the NVIDIA
# device plugin reserves no GPUs for system use. For CPU and memory, Allocatable
# is typically 10-15% less than Capacity due to kubelet reservations.
#
# WHAT "nvidia.com/gpu: 8" MEANS:
# The NVIDIA device plugin registers each physical GPU as a countable resource.
# A node with 2× A100 GPUs shows nvidia.com/gpu: 2.
# When a pod claims nvidia.com/gpu: 1, the device plugin pins one physical GPU
# to that pod's container (via CUDA_VISIBLE_DEVICES) and decrements Allocatable by 1.

# Inspect a specific node's full resource breakdown.
# Look for the Allocatable: block — it shows what's available for new pods.
# Compare nvidia.com/gpu in Allocatable vs the Allocated resources section
# (shown in `kubectl describe node`) to see how many are already in use.
kubectl describe node gpu-node-01 | grep -A5 "Allocatable:"
# Expected output:
# Allocatable:
#   cpu:                          96
#   memory:                       755Gi
#   nvidia.com/gpu:               8      ← 8 GPUs allocatable on this node
#   pods:                         110

# Cluster-wide GPU inventory: capacity and allocatable for every node.
# GPU-CAP  = total GPUs the hardware has
# GPU-ALLOC = GPUs available to be scheduled (should equal CAP if device plugin is healthy)
# If GPU-ALLOC is 0 but GPU-CAP is 8, the NVIDIA device plugin is not running on that node.
kubectl get nodes -o custom-columns=\
"NAME:.metadata.name,\
GPU-CAP:.status.capacity.nvidia\.com/gpu,\
GPU-ALLOC:.status.allocatable.nvidia\.com/gpu"

# To also see how many GPUs are currently IN USE (vs available), run:
# kubectl describe nodes | grep -A4 "nvidia.com/gpu"
# Look for "Requests" vs "Allocatable" in the per-node output.
# Or use: kubectl get pods --all-namespaces -o json | \
#   jq '[.items[].spec.containers[].resources.requests."nvidia.com/gpu" // 0 | tonumber] | add'
