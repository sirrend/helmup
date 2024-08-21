{{/*
    Return the secret name for the notifications service.
    If `.Values.global.secretNameOverride` is not empty, use it.
    Otherwise, use the default secret name.
*/}}
{{- define "helmup-service.secret" -}}
{{- if .Values.global.secretNameOverride }}
{{- .Values.global.secretNameOverride -}}
{{- else -}}
"helmup-secret"
{{- end -}}
{{- end -}}