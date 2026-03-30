{{/*
Init container: create mount dirs, then copy model weights (sizes[].path) and datasets (datasets[].path)
from config.yaml into PVCs. Paths come from inference-platform.discoveredModels (_get_configs.tpl).

Sources must exist inside the pod (same absolute paths as in config), e.g. hostPath volumes — see values.initContainers.

Context: (dict "root" $ "model" <discovered model dict>)
See values: initContainers.enabled, initContainers.image, initContainers.extraShell
*/}}
{{- define "inference-platform.mediaService.initContainers" -}}
{{- $root := .root -}}
{{- $model := .model -}}
{{- if $root.Values.initContainers.enabled }}
- name: init-data
  image: {{ $root.Values.initContainers.image | quote }}
  command:
    - /bin/sh
    - -c
    - |
      set -e
      MOUNT_MODELS="{{ $root.Values.storage.models.mountPath }}"
      MOUNT_DATASETS="{{ $root.Values.storage.datasets.mountPath }}"
      MOUNT_MEDIA="{{ $root.Values.storage.mediaFiles.mountPath }}"
      MOUNT_WEIGHTS="{{ $root.Values.storage.weights.mountPath }}"
      mkdir -p "$MOUNT_MODELS" "$MOUNT_DATASETS" "$MOUNT_MEDIA" "$MOUNT_WEIGHTS"
      sync_into() {
        src="$1"
        dest="$2"
        if [ -z "$src" ] || [ "$src" = "unknown" ]; then return 0; fi
        if [ ! -e "$src" ]; then echo "init-data: skip missing source (mount host paths into the pod if needed): $src"; return 0; fi
        mkdir -p "$dest"
        if [ -d "$src" ]; then cp -a "$src"/. "$dest"/; else cp -a "$src" "$dest"/; fi
      }
{{- range $sz := ($model.sizes | default list) }}
{{- if and (hasKey $sz "path") $sz.path (ne $sz.path "unknown") }}
      sync_into {{ $sz.path | quote }} "$MOUNT_WEIGHTS/{{ $model.name }}/{{ $sz.name }}"
{{- end }}
{{- end }}
{{- range $ds := ($model.datasets | default list) }}
{{- if and (hasKey $ds "path") $ds.path (ne $ds.path "unknown") }}
      sync_into {{ $ds.path | quote }} "$MOUNT_DATASETS/{{ $ds.name }}"
{{- end }}
{{- end }}
      echo "init-data: sync done for MODEL_ID=${MODEL_ID}"
{{ if $root.Values.initContainers.extraShell }}{{ $root.Values.initContainers.extraShell | nindent 6 }}{{ end }}
  env:
    - name: MODEL_ID
      value: {{ $model.name | quote }}
    - name: MODELS_MOUNT
      value: {{ $root.Values.storage.models.mountPath | quote }}
    - name: DATASETS_MOUNT
      value: {{ $root.Values.storage.datasets.mountPath | quote }}
    - name: MEDIA_MOUNT
      value: {{ $root.Values.storage.mediaFiles.mountPath | quote }}
    - name: WEIGHTS_MOUNT
      value: {{ $root.Values.storage.weights.mountPath | quote }}
  volumeMounts:
    - name: models
      mountPath: {{ $root.Values.storage.models.mountPath | quote }}
    - name: datasets
      mountPath: {{ $root.Values.storage.datasets.mountPath | quote }}
    - name: mediaFiles
      mountPath: {{ $root.Values.storage.mediaFiles.mountPath | quote }}
    - name: weights
      mountPath: {{ $root.Values.storage.weights.mountPath | quote }}
{{- range $hp := ($root.Values.initContainers.hostPathVolumes | default list) }}
    - name: {{ $hp.name }}
      mountPath: {{ $hp.mountPath | quote }}
{{- end }}
{{- end }}
{{- end }}
