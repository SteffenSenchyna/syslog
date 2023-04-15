#!/bin/bash
source .env
# Create the charts directory
mkdir -p charts

# Create the Kubernetes Secret YAML file
cat <<EOF > charts/${PWD##*/}-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ${PWD##*/}-secret
type: Opaque
data:
EOF

while read -r line || [ -n "$line" ]; do
  if [ -n "$line" ]; then
    key=$(echo $line | cut -d'=' -f1)
    value=$(echo $line | cut -d'=' -f2)
    encoded=$(echo -n $value | base64)
    echo "  $key: $encoded" >> charts/${PWD##*/}-secret.yaml
  fi
done < .env

# Create the Kubernetes ConfigMap YAML file
cat <<EOF > charts/${PWD##*/}-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${PWD##*/}-config
data:
EOF

while read -r line || [ -n "$line" ]; do
  if [ -n "$line" ]; then
    key=$(echo $line | cut -d'=' -f1)
    value=$(echo $line | cut -d'=' -f2)
    echo "  $key: $value" >> charts/${PWD##*/}-config.yaml
  fi
done < .env

# Create the Kubernetes Service YAML file
cat <<EOF > charts/${PWD##*/}-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ${PWD##*/}
spec:
  selector:
    app: ${PWD##*/}
  ports:
EOF

while read -r line || [ -n "$line" ]; do
    if [[ "$line" == *"EXPOSE"* ]]; then
        port=$(echo $line | awk '{print $2}' | cut -d'/' -f1)
        protocol=$(echo $line | awk '{print $2}' | cut -d'/' -f2)
        cat <<EOF >> charts/${PWD##*/}-service.yaml
    - protocol: $protocol
      port: $port
      targetPort: $port
EOF
    fi
done < Dockerfile

# Create the Kubernetes Deployment YAML file
cat <<EOF > charts/${PWD##*/}-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${PWD##*/}-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${PWD##*/}
  template:
    metadata:
      labels:
        app: ${PWD##*/}
    spec:
      containers:
        - name: ${PWD##*/}
          image: ssenchyna/${PWD##*/}:latest
          ports:
EOF

while read -r line || [ -n "$line" ]; do
    if [[ "$line" == *"EXPOSE"* ]]; then
        port=$(echo $line | awk '{print $2}' | cut -d'/' -f1)
        cat <<EOF >> charts/${PWD##*/}-deployment.yaml
            - containerPort: $port
EOF
    fi
done < Dockerfile

cat <<EOF >> charts/${PWD##*/}-deployment.yaml
          envFrom:
            - configMapRef:
                name: ${PWD##*/}-configmap
            - secretRef:
                name: ${PWD##*/}-secret
EOF
