{{- define "inference-platform.discoveredModels" -}}
{{- $root := . }}
{{- $list := list }}
{{- range $path, $_ := $root.Files.Glob "models/*/config.yaml" }}
  {{- $parts := splitList "/" $path }}
  {{- $name := index $parts 1 }}
  {{- $yaml := $root.Files.Get $path | fromYaml }}
  {{- $m := default (dict) $yaml.model }}
  {{- $id := "unknown" }}
  {{- if hasKey $m "id" }}
  {{- $id = $m.id }}
  {{- end }}
  {{- $replicas := 1 }}
  {{- if hasKey $m "replicas" }}
  {{- $replicas = $m.replicas }}
  {{- end }}
  {{- $enabled := false }}
  {{- if hasKey $m "enabled" }}
  {{- $enabled = $m.enabled }}
  {{- end }}
  {{- $sizesIn := default list $yaml.sizes }}
  {{- $sizeList := list }}
  {{- range $size := $sizesIn }}
    {{- $size_id := "unknown" }}
    {{- if hasKey $size "id" }}
    {{- $size_id = $size.id }}
    {{- end }}
    {{- $size_replicas := 1 }}
    {{- if hasKey $size "replicas" }}
    {{- $size_replicas = $size.replicas }}
    {{- end }}
    {{- $size_enabled := true }}
    {{- if hasKey $size "enabled" }}
    {{- $size_enabled = $size.enabled }}
    {{- end }}
    {{- $size_path := "unknown" }}
    {{- if hasKey $size "path" }}
    {{- $size_path = $size.path }}
    {{- end }}
    {{- $sizeList = append $sizeList (dict "name" $size_id "replicas" $size_replicas "enabled" $size_enabled "path" $size_path) }}
  {{- end }}
  {{- $datasetsIn := default list $yaml.datasets }}
  {{- $datasetList := list }}
  {{- range $dataset := $datasetsIn }}
    {{- $dataset_id := "unknown" }}
    {{- if hasKey $dataset "id" }}
    {{- $dataset_id = $dataset.id }}
    {{- end }}
    {{- $dataset_path := "unknown" }}
    {{- if hasKey $dataset "path" }}
    {{- $dataset_path = $dataset.path }}
    {{- end }}
    {{- $datasetList = append $datasetList (dict "name" $dataset_id "path" $dataset_path) }}
  {{- end }}
  {{- $list = append $list (dict "name" $name "enabled" $enabled "replicas" $replicas "sizes" $sizeList "datasets" $datasetList) }}
{{- end }}
{{- $list | toYaml }}
{{- end }}
