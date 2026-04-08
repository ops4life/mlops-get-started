#!/usr/bin/env bash
# node-labels.sh — Apply workload-type labels to cluster nodes
#
# WHY LABELS MATTER:
# Kubernetes labels are key=value metadata attached to nodes. Pod scheduling
# rules (nodeAffinity in pod-affinity.yaml) use these labels to control WHICH
# nodes a pod is allowed to land on. Without labels, the scheduler places pods
# on any available node — training jobs could end up on small general-purpose
# nodes and run out of memory or miss GPUs entirely.
#
# LABEL STRATEGY USED HERE:
#   workload-type=  broad category (routing tier)
#   gpu-type=       specific GPU chip model (preference tier)
#
# This two-tier approach lets you write affinity rules like:
#   "must be on a gpu-training node" AND "prefer A100 over V100"
#
# CONVENTION: replace node names (gpu-node-01, etc.) with your actual
# node names from `kubectl get nodes`.

# GPU nodes: dedicated for CUDA training workloads.
# The gpu-type label lets pods prefer specific GPU hardware via weighted affinity.
kubectl label node gpu-node-01 workload-type=gpu-training gpu-type=a100
kubectl label node gpu-node-02 workload-type=gpu-training gpu-type=a100

# Large CPU nodes: no GPU, but high RAM/core count for CPU-intensive training
# (e.g., scikit-learn, XGBoost, large feature engineering jobs).
kubectl label node cpu-large-01 workload-type=ml-training
kubectl label node cpu-large-02 workload-type=ml-training

# General nodes: for lightweight workloads (MLflow server, Airflow scheduler,
# web UIs). Training jobs should NOT land here — enforce this with affinity rules.
kubectl label node general-01 workload-type=general
kubectl label node general-02 workload-type=general

# Verify labels were applied.
# Look for workload-type= in the LABELS column for each node.
# If a node is missing its label, re-run the kubectl label command above.
kubectl get nodes --show-labels | grep workload-type
