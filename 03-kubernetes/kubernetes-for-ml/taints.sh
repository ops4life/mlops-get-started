#!/usr/bin/env bash
# taints.sh — Apply taints to GPU nodes to reserve them for ML workloads
#
# HOW TAINTS WORK:
# A taint on a node says "don't schedule pods here unless they tolerate this."
# Three taint effects control exactly what "don't schedule" means:
#
#   NoSchedule    — New pods without a matching toleration are REJECTED.
#                   Already-running pods are NOT evicted (they stay put).
#                   Use this to reserve a node going forward.
#
#   PreferNoSchedule — Scheduler tries to avoid placing pods here, but will
#                   do so if no other node is available. Soft constraint.
#
#   NoExecute     — New pods are rejected AND existing pods without a
#                   matching toleration are EVICTED immediately.
#                   Use this for hard eviction (e.g., draining a node).
#                   CAUTION: will also evict DaemonSet pods unless they
#                   have the toleration, which can break node-level agents.
#
# PATTERN: label first (node-labels.sh), then taint.
# Labels let pods TARGET a node via affinity.
# Taints PREVENT other pods from landing there without explicit permission.
# Together they create a dedicated pool: only ML training pods that have
# both the affinity rule AND the toleration will be scheduled on GPU nodes.

# Reserve GPU nodes for GPU training workloads.
# NoSchedule means existing pods (e.g., kube-proxy DaemonSets) are unaffected,
# but any new general-purpose pod will be rejected by the scheduler.
kubectl taint nodes gpu-node-01 dedicated=gpu-training:NoSchedule
kubectl taint nodes gpu-node-02 dedicated=gpu-training:NoSchedule

# To REMOVE a taint (e.g., when decommissioning the reservation):
# kubectl taint nodes gpu-node-01 dedicated=gpu-training:NoSchedule-
#   (note the trailing dash — that's the kubectl syntax for removal)

# Use NoExecute only when you want to drain all non-tolerating pods immediately,
# for example before maintenance or hardware replacement.
# WARNING: this will evict any running training jobs on the node.
# kubectl taint nodes gpu-node-01 dedicated=gpu-training:NoExecute

# Verify taints were applied. Look for "Taints:" in the output.
kubectl describe node gpu-node-01 | grep -A3 "Taints:"
kubectl describe node gpu-node-02 | grep -A3 "Taints:"
