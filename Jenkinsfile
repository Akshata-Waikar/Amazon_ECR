pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-northeast-2'
        ECR_REPO = '265980493709.dkr.ecr.ap-northeast-2.amazonaws.com/flask-app'
        IMAGE_TAG = 'latest'
        SSH_PRIVATE_KEY = credentials('live-server-key')  // Jenkins credential ID
        LIVE_SERVER_IP = '3.37.129.19' // <== REPLACED WITH ACTUAL IP
    }

    stages {
        stage('Clone Repo') {
            steps {
                git credentialsId: 'github-pat', url: 'https://github.com/Akshata-Waikar/Amazon_ECR', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('flask_app') {
                    sh 'docker build -t flask-app .'
                }
            }
        }

        stage('Login to ECR') {
            steps {
                sh "aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO"
            }
        }

        stage('Tag & Push Image') {
            steps {
                sh """
                    docker tag flask-app:latest $ECR_REPO:$IMAGE_TAG
                    docker push $ECR_REPO:$IMAGE_TAG
                """
            }
        }

        stage('Deploy to Live Server') {
            steps {
                sh """
                    ssh -o StrictHostKeyChecking=no -i $SSH_PRIVATE_KEY ec2-user@$LIVE_SERVER_IP << EOF
                    docker pull $ECR_REPO:$IMAGE_TAG
                    docker stop flask-container || true
                    docker rm flask-container || true
                    docker run -d --name flask-container -p 80:5000 $ECR_REPO:$IMAGE_TAG
                    EOF
                """
            }
        }
    }
}

