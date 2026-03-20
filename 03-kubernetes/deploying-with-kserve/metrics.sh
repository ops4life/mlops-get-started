# Key KServe metrics exposed at /metrics on port 8080:
# revision_request_count          — total requests (label: response_code)
# revision_request_latencies      — request latency histogram
# revision_request_concurrencies  — concurrent requests in flight
# kserve_request_duration_seconds — model inference duration

# Useful PromQL queries:
# Request rate:
sum(rate(revision_request_count{namespace="ml-serving"}[5m]))

# P99 latency:
histogram_quantile(0.99, sum(rate(revision_request_latencies_bucket{
  namespace="ml-serving",
  revision_name=~"churn-predictor.*"
}[5m])) by (le))

# Error rate:
sum(rate(revision_request_count{
  namespace="ml-serving",
  response_code!="200"
}[5m])) / sum(rate(revision_request_count{namespace="ml-serving"}[5m]))
