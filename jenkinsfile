pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = 'your_account_id'
        AWS_REGION = 'ap-northeast-2'
        IMAGE_NAME = 'flask-app-repo'
        REPO_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/yourusername/your-flask-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}")
                }
            }
        }

        stage('Login to Amazon ECR') {
            steps {
                script {
                    sh """
                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin $REPO_URI
                    """
                }
            }
        }

        stage('Tag & Push Image') {
            steps {
                script {
                    docker.image("${IMAGE_NAME}").tag("latest")
                    sh "docker tag ${IMAGE_NAME}:latest $REPO_URI:latest"
                    sh "docker push $REPO_URI:latest"
                }
            }
        }

        stage('Trigger Lambda') {
            steps {
                script {
                    sh '''
                    aws lambda invoke \
                    --function-name notifyAfterPush \
                    --payload '{"image":"flask-app-repo"}' \
                    output.json
                    '''
                }
            }
        }
    }
}
