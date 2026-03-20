# Label nodes by workload type
kubectl label node gpu-node-01 workload-type=gpu-training gpu-type=a100
kubectl label node gpu-node-02 workload-type=gpu-training gpu-type=a100
kubectl label node cpu-large-01 workload-type=ml-training
kubectl label node cpu-large-02 workload-type=ml-training
kubectl label node general-01 workload-type=general
kubectl label node general-02 workload-type=general

# Verify labels
kubectl get nodes --show-labels | grep workload-type
