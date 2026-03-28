{{- define "inference-platform.name" -}}
{{- .Chart.Name -}}
{{- end }}

{{- define "inference-platform.fullname" -}}
{{- .Release.Name }}-{{ .Chart.Name }}
{{- end }}

{{- define "inference-platform.frontend.name" -}}
{{- printf "%s-frontend" .Release.Name -}}
{{- end }}

{{- define "inference-platform.gateway.name" -}}
{{- printf "%s-gateway" .Release.Name -}}
{{- end }}

{{- define "inference-platform.media_service.name" -}}
{{- printf "%s-media-service" .Release.Name -}}
{{- end }}

{{- define "inference-platform.gateway.service" -}}
{{- printf "%s-gateway-service" .Release.Name -}}
{{- end }}

{{- define "inference-platform.mediaPvc.name" -}}
{{- printf "%s-media-files" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}
