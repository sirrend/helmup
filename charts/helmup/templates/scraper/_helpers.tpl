{{/*
Expand the name of the chart.
*/}}
{{- define "helmup-github-scraper.name" -}}
{{- default .Chart.Name .Values.scraper.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "helmup-github-scraper.fullname" -}}
{{- if .Values.scraper.fullnameOverride }}
{{- .Values.scraper.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.scraper.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "helmup-github-scraper.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "helmup-github-scraper.labels" -}}
helm.sh/chart: {{ include "helmup-github-scraper.chart" . }}
{{ include "helmup-github-scraper.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "helmup-github-scraper.selectorLabels" -}}
app.kubernetes.io/name: {{ include "helmup-github-scraper.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "helmup-github-scraper.serviceAccountName" -}}
{{- if .Values.scraper.serviceAccount.create }}
{{- default (include "helmup-github-scraper.fullname" .) .Values.scraper.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.scraper.serviceAccount.name }}
{{- end }}
{{- end }}
