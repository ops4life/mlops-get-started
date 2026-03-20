# Taint GPU nodes — only pods with this toleration will be scheduled here
kubectl taint nodes gpu-node-01 dedicated=gpu-training:NoSchedule
kubectl taint nodes gpu-node-02 dedicated=gpu-training:NoSchedule

# Taint with NoExecute to also evict existing pods that don't tolerate it
# (use with caution — will evict running system pods too)
# kubectl taint nodes gpu-node-01 dedicated=gpu-training:NoExecute
