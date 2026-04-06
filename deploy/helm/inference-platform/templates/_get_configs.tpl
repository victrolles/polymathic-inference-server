{{- define "inference-platform.discoveredModels" -}}
{{- $root := . }}
{{- $list := list }}
{{- range $path, $_ := $root.Files.Glob "models/*/config.yaml" }}
  {{- $parts := splitList "/" $path }}
  {{- $name := index $parts 1 }}
  {{- $yaml := $root.Files.Get $path | fromYaml }}
  {{- $m := default (dict) $yaml.model }}

  {{- $id := dig "id" "unknown" $m }}
  {{- $replicas := dig "replicas" 1 $m }}
  {{- $enabled := dig "enabled" true $m }}

  {{- $sizesIn := default list $yaml.sizes }}
  {{- $sizeList := list }}
  {{- range $size := $sizesIn }}

    {{- $size_id := dig "id" "unknown" $size }}
    {{- $size_replicas := dig "replicas" 1 $size }}
    {{- $size_enabled := dig "enabled" true $size }}
    {{- $size_enabled_gpu := dig "enabled_gpu" false $size }}
    {{- $size_path := dig "path" "unknown" $size }}
    {{- $size_requests_memory := dig "resources" "requests" "memory" "1Gi" $size }}
    {{- $size_requests_cpu := dig "resources" "requests" "cpu" 1 $size }}
    {{- $size_limits_memory := dig "resources" "limits" "memory" "1Gi" $size }}
    {{- $size_limits_cpu := dig "resources" "limits" "cpu" 2 $size }}

    {{- $sizeList = append $sizeList (dict
        "name" $size_id
        "replicas" $size_replicas
        "enabled" $size_enabled
        "path" $size_path
        "enabled_gpu" $size_enabled_gpu
        "resources" (dict
          "requests" (dict "memory" $size_requests_memory "cpu" $size_requests_cpu)
          "limits" (dict "memory" $size_limits_memory "cpu" $size_limits_cpu)
        )
      ) }}
  {{- end }}
  {{- $datasetsIn := default list $yaml.datasets }}
  {{- $datasetList := list }}
  {{- range $dataset := $datasetsIn }}

    {{- $dataset_id := dig "id" "unknown" $dataset }}
    {{- $dataset_path := dig "path" "unknown" $dataset }}
    
    {{- $datasetList = append $datasetList (dict "name" $dataset_id "path" $dataset_path) }}
  {{- end }}
  {{- $list = append $list (dict "name" $name "enabled" $enabled "replicas" $replicas "sizes" $sizeList "datasets" $datasetList) }}
{{- end }}
{{- $list | toYaml }}
{{- end }}
