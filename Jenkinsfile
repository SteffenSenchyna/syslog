#!/usr/bin/env groovy

pipeline {
  environment {
    HELM_TAG = "1.0.0"
    BUILD_TAG = "0.${currentBuild.number}"
    GIT_COMMIT = sh(returnStdout: true, script: 'git rev-parse HEAD').trim().substring(0, 6)
    USER="ssenchyna"
    SERVICE = env.JOB_NAME.substring(0, env.JOB_NAME.lastIndexOf('/'))
    NETBOXTOKEN=""
    NETBOXURL=""
    DISCORDURL=""
    AWS_ACCESS_KEY=""
    AWS_SECRET_KEY=""
    AWS_DEFAULT_REGION=""
    AWS_S3_BUCKET_NAME=""
    NETWORKAPIURL=""
    MONGOURL=""
  }

  agent any

  stages {   
    stage('Build For Unit Testing') {
      steps {
          sh 'pip install -r requirements.txt'
        }
      }

    stage ('Unit Testing'){
      steps {
        sh 'python3 -m unittest discover -s . -p "*_test.py"'
        }
      }
 
    stage("Docker login") {
      steps {
        sh """
          ## Login to Docker Repo ##
          echo ${env.DOCKER_PASS} | docker login -u $USER --password-stdin
          echo ${env.DOCKER_PASS} | helm registry login registry-1.docker.io -u $USER --password-stdin 
        """
      }
    }

    stage("Build Docker/Helm") {
        steps {
            sh """
            docker build -t ${env.DOCKER_REPO}/$SERVICE:$BUILD_TAG .
            docker push ${env.DOCKER_REPO}/$SERVICE:$BUILD_TAG
            sed -i 's/version:.*/version: $HELM_TAG/' ./helm-chart/Chart.yaml
            sed -i 's/appVersion:.*/appVersion: $BUILD_TAG/' ./helm-chart/Chart.yaml
            helm package ./helm-chart
            """
        }
    }
    stage("Push Docker/Helm") {
        steps {
            sh """
            docker push ${env.DOCKER_REPO}/$SERVICE:$BUILD_TAG
            helm push "$SERVICE-$HELM_TAG".tgz oci://registry-1.docker.io/$USER
            """
        }
    }    
  }
}