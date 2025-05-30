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
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
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
            environment {
                NGROK_AUTHTOKEN = credentials('NGROK_AUTHTOKEN')         
                GROQ_API_KEY = credentials('groq_api_key')
                GROUNDX_API_KEY = credentials('groundx_api_key')
                BUCKET_ID = credentials('BUCKET_ID')  
                SOURCE_URL = 'https://www.docker.com/'
            }
            steps {
                script {
                    // Write the .env file dynamically
                    writeFile file: '.env', text: """
                        NGROK_AUTHTOKEN=${env.NGROK_AUTHTOKEN}
                        groq_api_key=${env.GROQ_API_KEY}
                        groundx_api_key=${env.GROUNDX_API_KEY}
                        BUCKET_ID=${env.BUCKET_ID}
                        SOURCE_URL=${env.SOURCE_URL}
                    """.stripIndent()

                    sh 'docker compose down'
                    sh 'docker compose up -d'
                }
            }
        }
    }

    post {
        always {
            sh 'docker compose down || true'
        }
    }
}

