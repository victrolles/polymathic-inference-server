{{- define "inference-platform.name" -}}
{{- .Chart.Name -}}
{{- end }}

{{- define "inference-platform.frontend.name" -}}
{{- $root := .root | default . -}}
{{- printf "%s-frontend" (include "inference-platform.name" $root) -}}
{{- end }}

{{- define "inference-platform.frontend.service" -}}
{{- $root := .root | default . -}}
{{- printf "%s-frontend-service" (include "inference-platform.name" $root) -}}
{{- end }}

{{- define "inference-platform.gateway.name" -}}
{{- $root := .root | default . -}}
{{- printf "%s-gateway" (include "inference-platform.name" $root) -}}
{{- end }}

{{- define "inference-platform.gateway.service" -}}
{{- $root := .root | default . -}}
{{- printf "%s-gateway-service" (include "inference-platform.name" $root) -}}
{{- end }}

{{- define "inference-platform.media_service.name" -}}
{{- $root := .root | default . -}}
{{- printf "%s-media-service-%s" (include "inference-platform.name" $root) .modelName -}}
{{- end }}

{{- define "inference-platform.media_service.service" -}}
{{- $root := .root | default . -}}
{{- printf "%s-media-service-%s-service" (include "inference-platform.name" $root) .modelName -}}
{{- end }}

{{- define "inference-platform.worker.name" -}}
{{- $root := .root | default . -}}
{{- printf "%s-worker-%s-%s" (include "inference-platform.name" $root) .modelName .sizeName }}
{{- end }}

{{- define "inference-platform.mediaFiles.name" -}}
{{- $root := .root | default . -}}
{{- printf "%s-media-files" (include "inference-platform.name" $root) -}}
{{- end }}

{{- define "inference-platform.models.name" -}}
{{- $root := .root | default . -}}
{{- printf "%s-models" (include "inference-platform.name" $root) -}}
{{- end }}

{{- define "inference-platform.weights.name" -}}
{{- $root := .root | default . -}}
{{- printf "%s-weights" (include "inference-platform.name" $root) -}}
{{- end }}

{{- define "inference-platform.datasets.name" -}}
{{- $root := .root | default . -}}
{{- printf "%s-datasets" (include "inference-platform.name" $root) -}}
{{- end }}
