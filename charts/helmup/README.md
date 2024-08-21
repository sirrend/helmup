# helmup

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.1.0](https://img.shields.io/badge/AppVersion-1.1.0-informational?style=flat-square)

Official Sirrend helmup application

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| Sirrend | <business@sirrend.com> | <https://www.sirrend.io/> |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| engine.affinity | object | `{}` |  |
| engine.autoscaling.enabled | bool | `false` |  |
| engine.autoscaling.maxReplicas | int | `10` | Max number of pods to run |
| engine.autoscaling.minReplicas | int | `1` | Min number of pods to run |
| engine.autoscaling.targetCPUUtilizationPercentage | int | `80` | The threshold of CPU utilization to scale up upom  |
| engine.fullnameOverride | string | `""` |  |
| engine.image.pullPolicy | string | `"Always"` | imagePullPolicy - Highly recommended to leave this as Always |
| engine.image.repository | string | `"sirrend/helmup-engine"` | Repository for the helmup-engine image |
| engine.image.tag | string | `"0.1.13"` | The helmup-engine image tag to use |
| engine.imagePullSecrets | list | `[]` | A list of image pull secret names to use |
| engine.ingress.annotations | object | `{}` |  |
| engine.ingress.className | string | `""` | From Kubernetes 1.18+ this field is supported in case your ingress controller supports it. When set, you do not need to add the ingress class as annotation. |
| engine.ingress.enabled | bool | `false` | Enables an ingress object for the application |
| engine.ingress.hosts[0].host | string | `"chart-example.local"` |  |
| engine.ingress.hosts[0].paths[0].path | string | `"/"` |  |
| engine.ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` |  |
| engine.ingress.tls | list | `[]` |  |
| engine.livenessProbe.enabled | bool | `true` |  |
| engine.livenessProbe.failureThreshold | int | `3` |  |
| engine.livenessProbe.initialDelaySeconds | int | `15` |  |
| engine.livenessProbe.path | string | `"/healthcheck"` | Please do not change this |
| engine.livenessProbe.periodSeconds | int | `300` |  |
| engine.livenessProbe.port | int | `8090` |  |
| engine.livenessProbe.timeoutSeconds | int | `5` |  |
| engine.nameOverride | string | `"engine"` |  |
| engine.nodeSelector | object | `{}` |  |
| engine.podAnnotations | object | `{}` | Extra annotations for the engine pod |
| engine.podLabels | object | `{}` |  |
| engine.podSecurityContext | object | `{}` | Defines the podSecurityContext for the engine pod |
| engine.readinessProbe.enabled | bool | `false` |  |
| engine.readinessProbe.failureThreshold | int | `3` |  |
| engine.readinessProbe.initialDelaySeconds | int | `20` |  |
| engine.readinessProbe.path | string | `"/healthcheck"` | Please do not change this |
| engine.readinessProbe.periodSeconds | int | `10` |  |
| engine.readinessProbe.port | int | `8090` |  |
| engine.readinessProbe.timeoutSeconds | int | `5` |  |
| engine.replicaCount | int | `1` | Number of engine pods to run |
| engine.resources | object | `{}` | A resources block for the engine pod |
| engine.securityContext | object | `{}` | The container securityContext for the controller container |
| engine.service.port | int | `80` | The port to run the dashboard engine on |
| engine.service.type | string | `"ClusterIP"` | The type of the engine service |
| engine.serviceAccount.annotations | object | `{}` | Extra annotations for the service account that will be created |
| engine.serviceAccount.automount | bool | `true` | If true, the service account will be mounted automatically |
| engine.serviceAccount.create | bool | `true` | If true, a service account will be created for the controller. If set to false, uses default serviceAccount |
| engine.serviceAccount.name | string | `""` | The name of an existing service account to use for the controller |
| engine.startupProbe.enabled | bool | `true` |  |
| engine.startupProbe.failureThreshold | int | `3` |  |
| engine.startupProbe.initialDelaySeconds | int | `10` |  |
| engine.startupProbe.path | string | `"/healthcheck"` | Please do not change this |
| engine.startupProbe.periodSeconds | int | `10` |  |
| engine.startupProbe.port | int | `8090` |  |
| engine.startupProbe.timeoutSeconds | int | `5` |  |
| engine.tolerations | list | `[]` |  |
| engine.volumeMounts | list | `[]` | Extra volumes for the engine pod |
| engine.volumes | list | `[]` | Extra volume mounts for the engine container |
| global.appConfig.github.CUSTOMER_NAME | string | `"sirrend"` | Required: Github account / project name |
| global.appConfig.github.GIT_BRANCH | string | `"main"` | Required: Github branch name to scrape |
| global.appConfig.github.GIT_REPOSITORY_NAME | string | `"kuba_test"` | Required: Github repo name |
| global.appConfig.github.GIT_REPOSITORY_URL | string | `"https://github.com/sirrend/kuba_test.git"` | Required: Github repository URL |
| global.appConfig.jira.enabled | bool | `true` | Required: Whether to enable jira notifications / tickets creation |
| global.appConfig.jira.project_key | string | `"SI"` | The jira project key |
| global.appConfig.jira.server_url | string | `"https://sirrend.atlassian.net/"` | The jira server URL |
| global.appConfig.jira.username | string | `"yuvalpress@gmail.com"` | Jira username |
| global.appConfig.notifications.enabled | bool | `true` | Required: Whether or not to send notification via channels (slack or teams - as configured in the notifications section) |
| global.appConfig.notifications.type | string | `"slack"` | Valid options are ["slack", "teams", "None"] |
| global.appConfig.reformat_helm_templates | bool | `true` | Whether or not to improve the helm manifest using AI capabilities. Recommended! |
| global.appConfig.target_kube_version | string | `"1.30.0"` |  |
| global.appConfig.upgrade_majors | string | `"disabled"` | Whether or not to upgrade major chart's versions |
| global.externalSecret.backendType | string | `"secretsManager"` | Specify the secretStoreRef, e.g., secretsManager for AWS Secrets Manager |
| global.externalSecret.enabled | bool | `true` | Required: Support for external secrets operator: Enables/Disables externalSecret to be imported to the namespace. Conflicts with "secretNameOverride" |
| global.externalSecret.refreshInterval | string | `"30h"` | Speficy the refresh interval for the secret |
| global.externalSecret.secretKeyGithub | string | `"sirrend-github-token"` | The secret name to pull from SecretStore for the Github token |
| global.externalSecret.secretKeyJira | string | `"sirrend-jira-token"` | The secret name to pull from SecretStore for the Jira token |
| global.externalSecret.secretKeyNotificationsWebhookUrl | string | `"sirrend-slack-webhook-secret"` | The secret name to pull from SecretStore for the notifications channel (slack/teams) webhhok url |
| global.externalSecret.secretKeyOpenAI | string | `"chatgpt-token"` | The secret name to pull from SecretStore for the openAI chatgpt token |
| global.externalSecret.secretStoreRef | object | `{"kind":"ClusterSecretStore","name":"aws-secrets-manager"}` | Specify the secretStoreRef |
| global.externalSecret.secretTemplate | object | `{"annotations":{},"data":{},"labels":{},"type":"Opaque"}` | externalSecret template |
| global.externalSecret.secretVersion | string | `""` | Optional |
| global.secretNameOverride | string | `""` | If using a self-defined secret, specify its name |
| notifications.affinity | object | `{}` |  |
| notifications.enabled | bool | `true` |  |
| notifications.fullnameOverride | string | `""` |  |
| notifications.image.pullPolicy | string | `"Always"` | imagePullPolicy - Highly recommended to leave this as Always |
| notifications.image.repository | string | `"sirrend/helmup-notifications-service"` | Repository for the helmup-notifications-service image |
| notifications.image.tag | string | `"0.1.3"` | The helmup-github-scraper image tag to use |
| notifications.imagePullSecrets | list | `[]` | A list of image pull secret names to use |
| notifications.livenessProbe.enabled | bool | `true` |  |
| notifications.livenessProbe.failureThreshold | int | `3` |  |
| notifications.livenessProbe.initialDelaySeconds | int | `15` |  |
| notifications.livenessProbe.path | string | `"/health"` | Please do not change this |
| notifications.livenessProbe.periodSeconds | int | `300` |  |
| notifications.livenessProbe.port | int | `9000` |  |
| notifications.livenessProbe.timeoutSeconds | int | `5` |  |
| notifications.nameOverride | string | `"notifications-service"` |  |
| notifications.nodeSelector | object | `{}` |  |
| notifications.podAnnotations | object | `{}` | Extra annotations for the notifications pod |
| notifications.podLabels | object | `{}` |  |
| notifications.podSecurityContext | object | `{}` | Defines the podSecurityContext for the notifications pod |
| notifications.readinessProbe.enabled | bool | `false` |  |
| notifications.readinessProbe.failureThreshold | int | `3` |  |
| notifications.readinessProbe.initialDelaySeconds | int | `20` |  |
| notifications.readinessProbe.path | string | `"/health"` | Please do not change this |
| notifications.readinessProbe.periodSeconds | int | `30` |  |
| notifications.readinessProbe.port | int | `9000` |  |
| notifications.readinessProbe.timeoutSeconds | int | `5` |  |
| notifications.replicaCount | int | `1` | Number of engine pods to run |
| notifications.resources | object | `{}` | A resources block for the notifications pod |
| notifications.securityContext | object | `{}` | The container securityContext for the controller container |
| notifications.service.port | int | `80` | The port to run the dashboard engine on |
| notifications.service.type | string | `"ClusterIP"` | The type of the engine service |
| notifications.serviceAccount.annotations | object | `{}` | Extra annotations for the service account that will be created |
| notifications.serviceAccount.automount | bool | `true` | If true, the service account will be mounted automatically |
| notifications.serviceAccount.create | bool | `true` | If true, a service account will be created for the controller. If set to false, uses default serviceAccount |
| notifications.serviceAccount.name | string | `""` | The name of an existing service account to use for the controller |
| notifications.startupProbe.enabled | bool | `false` |  |
| notifications.startupProbe.failureThreshold | int | `3` |  |
| notifications.startupProbe.initialDelaySeconds | int | `30` |  |
| notifications.startupProbe.path | string | `"/health"` | Please do not change this |
| notifications.startupProbe.periodSeconds | int | `10` |  |
| notifications.startupProbe.port | int | `9000` |  |
| notifications.startupProbe.timeoutSeconds | int | `5` |  |
| notifications.tolerations | list | `[]` |  |
| notifications.volumeMounts | list | `[]` | Extra volumes for the notifications pod |
| notifications.volumes | list | `[]` | Extra volume mounts for the notifications container |
| scraper.affinity | object | `{}` |  |
| scraper.cronJobExpression | string | `"0 0 * * *"` | Required: the cronJob expressions to scrape the git repo |
| scraper.failedJobsHistoryLimit | int | `1` | Required: failed job history limit |
| scraper.fullnameOverride | string | `""` |  |
| scraper.image.pullPolicy | string | `"Always"` | imagePullPolicy - Highly recommended to leave this as Always |
| scraper.image.repository | string | `"sirrend/helmup-github-scraper"` | Repository for the helmup-github-scraper image |
| scraper.image.tag | string | `"0.1.4"` | The helmup-github-scraper image tag to use |
| scraper.imagePullSecrets | list | `[]` | A list of image pull secret names to use |
| scraper.nameOverride | string | `"github-scraper"` |  |
| scraper.nodeSelector | object | `{}` |  |
| scraper.podAnnotations | object | `{}` | Extra annotations for the scraper pod |
| scraper.podLabels | object | `{}` |  |
| scraper.podSecurityContext | object | `{}` | Defines the podSecurityContext for the scraper pod |
| scraper.replicaCount | int | `1` | Number of engine pods to run |
| scraper.resources | object | `{}` | A resources block for the scraper pod |
| scraper.securityContext | object | `{}` | The container securityContext for the scraper container |
| scraper.serviceAccount.annotations | object | `{}` | Extra annotations for the service account that will be created |
| scraper.serviceAccount.automount | bool | `true` | If true, the service account will be mounted automatically |
| scraper.serviceAccount.create | bool | `true` | If true, a service account will be created for the controller. If set to false, uses default serviceAccount |
| scraper.serviceAccount.name | string | `""` | The name of an existing service account to use for the controller |
| scraper.successfulJobsHistoryLimit | int | `3` | Required: successful job history limit |
| scraper.tolerations | list | `[]` |  |
| scraper.volumeMounts | list | `[]` | Extra volumes for the scraper pod |
| scraper.volumes | list | `[]` | Extra volume mounts for the scraper container |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.14.2](https://github.com/norwoodj/helm-docs/releases/v1.14.2)
