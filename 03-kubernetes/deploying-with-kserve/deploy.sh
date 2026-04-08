#!/usr/bin/env bash
# deploy.sh — Deploy a KServe InferenceService and test the endpoint
#
# PREREQUISITES:
#   - kubectl configured and pointing at your cluster
#   - KServe installed (with Istio or Knative serving)
#   - inferenceservice-churn.yaml applied (or use inference-service.yaml)
#   - The model artifact accessible at the storageUri (S3/MinIO must be reachable)

# Apply the InferenceService manifest.
# KServe will create a Revision, download the model from storageUri, and start
# the serving container. The InferenceService moves through states:
#   Unknown → False (downloading) → True (ready)
kubectl apply -f inferenceservice-churn.yaml

# Check current status immediately after apply.
# READY=True means the model is loaded and serving traffic.
# READY=False means still starting up — check the message column for details.
# READY=Unknown means the controller hasn't processed the resource yet.
kubectl get inferenceservice churn-predictor -n ml-serving

# Block the script until READY=True.
# timeout=300s (5 minutes) accounts for:
#   - Model download time (proportional to artifact size over S3 bandwidth)
#   - Container cold start time (pulling the sklearn serving image if not cached)
#   - Knative revision initialization
# If this times out, run: kubectl describe inferenceservice churn-predictor -n ml-serving
# and look at the Conditions section for the root cause.
kubectl wait --for=condition=Ready inferenceservice/churn-predictor -n ml-serving --timeout=300s

# Get the Istio ingress gateway hostname.
# All KServe traffic routes through Istio. The model is NOT directly accessible
# via a ClusterIP — you must go through the ingress gateway and set the
# Host header to route to the correct InferenceService.
INGRESS_HOST=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# KServe implements the Open Inference Protocol (v2) for model serving.
# URL format: /v2/models/{model-name}/infer
# The Host header tells Istio which InferenceService to route to.
MODEL_URL="http://${INGRESS_HOST}/v2/models/churn-predictor/infer"

# Test inference with a sample request using the v2 protocol payload format.
# inputs[] array fields:
#   name      — arbitrary label for this input tensor (matches model signature)
#   shape     — [batch_size, num_features]: [1, 5] = 1 row with 5 feature values
#   datatype  — FP32 = 32-bit float; use INT64 for integer features, BYTES for strings
#   data      — flat list of values; shape tells the server how to reshape it
#
# Sample row: [age=45, tenure_months=12, num_products=3, monthly_charge=0.25, total_charges=180.5]
# The response will contain an "outputs" array with the predicted class probabilities.
curl -X POST "${MODEL_URL}" \
  -H "Content-Type: application/json" \
  -H "Host: churn-predictor.ml-serving.example.com" \
  -d '{
    "inputs": [{
      "name": "predict",
      "shape": [1, 5],
      "datatype": "FP32",
      "data": [[45, 12, 3, 0.25, 180.5]]
    }]
  }'
