# Storage Manager Helm Installation Guide

> Please make sure the Kubernetes cluster, kubectl and helm (version 3.x) tools ready before you start.

## Install application

1. Update `config.yaml` to reflect your cluster

```yaml
mongodb:
  scheme: mongodb
  host: localhost
  port: 27017
  username: mdbadmin
  password: password
  database: admin
  options:
    retryWrites: true
```

2. Create Kubernetes secret from `config.yaml`

```bash
# The secret name storage-manager-config CANNOT be changed
kubectl create secret -n NAMESPACE generic storage-manager-config --from-file=config.yaml=config.yaml
```

3. Update `storage-manager/values.yaml` file

```yaml
# For example, use Nginx ingress to expose HTTPS service

ingress:
  enabled: true
  annotations:
    kubernetes.io/ingress.class: nginx
    kubernetes.io/tls-acme: "true"
  hosts:
    - host: storage-manager.actini.wang
      paths:
        - /
  tls:
   - secretName: storage-manager-actini-wang-tls
     hosts:
       - storage-manager.actini.wang

# For more configurations, please refer [Helm | Values Files](https://helm.sh/docs/chart_template_guide/values_files/)
```

4. Install application with Helm

```bash
helm upgrade --install -n NAMESPACE storage-manager storage-manager/
```

5. Check the pod running status

```bash
kubectl get pods -n NAMESPACE -l app.kubernetes.io/name=storage-manager
```