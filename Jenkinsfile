pipeline {
  agent any

  environment {
      DOCKER_IMAGE = 'rain210/llm-api'
      DOCKER_TAG = 'latest'
  }

  stages {
      stage('Checkout') {
          steps {
              git branch: 'main', url: 'https://github.com/rain2108/LLM-API.git'
          }
      }

      stage('Build Docker Image') {
          steps {
              sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG'
          }
      }

      stage('Push Docker Image') {
          steps {
              withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                  sh 'echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin'
                  sh 'docker push $DOCKER_IMAGE:$DOCKER_TAG'
              }
          }
      }
      stage('Deploy') {
          steps {
              sh 'docker-compose down'
              sh 'docker-compose up -d'
          }
      }
  }

  post {
      always {
          sh 'docker-compose down'
      }
  }
}

