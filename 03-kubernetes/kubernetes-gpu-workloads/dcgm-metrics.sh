# Key DCGM metrics (query from Prometheus):
# GPU utilization: DCGM_FI_DEV_GPU_UTIL
# Memory used:     DCGM_FI_DEV_FB_USED
# Memory total:    DCGM_FI_DEV_FB_TOTAL
# GPU temperature: DCGM_FI_DEV_GPU_TEMP
# Power draw:      DCGM_FI_DEV_POWER_USAGE
# SM clock:        DCGM_FI_DEV_SM_CLOCK
# NVLink errors:   DCGM_FI_DEV_NVLINK_CRC_FLIT_ERROR_COUNT_TOTAL

# Example Prometheus alert: GPU too hot
# - alert: GPUTemperatureHigh
#   expr: DCGM_FI_DEV_GPU_TEMP > 85
#   for: 5m
#   annotations:
#     summary: "GPU temperature above 85°C on {{ $labels.instance }}"

# Check current GPU utilization from the CLI
kubectl exec -n gpu-operator ds/nvidia-dcgm-exporter -- \
  curl -s localhost:9400/metrics | grep DCGM_FI_DEV_GPU_UTIL
