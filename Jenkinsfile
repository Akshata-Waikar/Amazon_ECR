pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '265980493709'
        AWS_REGION = 'ap-northeast-2'
        IMAGE_NAME = 'flask-app-repo'
        REPO_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}"
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Akshata-Waikar/flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}")
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh """
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REPO_URI
                    """
                }
            }
        }

        stage('Tag & Push to ECR') {
            steps {
                script {
                    def image = docker.image("${IMAGE_NAME}")
                    image.tag("latest")
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
