pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = 'your-account-id.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPOSITORY = 'flask-app-repo'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Akshata-Waikar/Amazon_ECR.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('flask-app') { // ✅ Corrected folder name
                    sh 'docker build -t flask-app .'
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh 'aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY'
                }
            }
        }

        stage('Tag & Push Image') {
            steps {
                script {
                    sh """
                        docker tag flask-app:latest $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
                        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
                    """
                }
            }
        }

        stage('Deploy to Live Server') {
            steps {
                sh 'echo "Deploy logic goes here..."'
            }
        }
    }
}
