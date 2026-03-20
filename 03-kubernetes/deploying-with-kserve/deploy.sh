# Deploy and check status
kubectl apply -f inferenceservice-churn.yaml
kubectl get inferenceservice churn-predictor -n ml-serving

# Wait for READY=True (model download + startup can take a minute)
kubectl wait --for=condition=Ready inferenceservice/churn-predictor -n ml-serving --timeout=300s

# Get the endpoint URL
INGRESS_HOST=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
MODEL_URL="http://${INGRESS_HOST}/v2/models/churn-predictor/infer"

# Test inference with the v2 protocol
curl -X POST ${MODEL_URL} \
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
