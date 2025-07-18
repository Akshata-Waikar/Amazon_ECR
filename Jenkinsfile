pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '265980493709'                  // Replace with your AWS Account ID
        AWS_REGION = 'ap-northeast-2'                    // Replace with your AWS region
        IMAGE_NAME = 'flask-app'
        REPO_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}"
        LIVE_SERVER = 'ec2-user@15.164.232.143'   // Replace with your EC2 public IP
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Akshata-Waikar/Python_through_jenkins.git'  // Use your actual repo
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
                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin $REPO_URI
                    """
                }
            }
        }

        stage('Tag & Push to ECR') {
            steps {
                script {
                    sh """
                    docker tag ${IMAGE_NAME}:latest ${REPO_URI}:latest
                    docker push ${REPO_URI}:latest
                    """
                }
            }
        }

        stage('Deploy to Live Server') {
            steps {
                sshagent(credentials: ['live-server-ssh']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $LIVE_SERVER '
                        docker pull $REPO_URI:latest &&
                        docker stop flask-container || true &&
                        docker rm flask-container || true &&
                        docker run -d -p 5000:5000 --name flask-container $REPO_URI:latest
                    '
                    """
                }
            }
        }

        stage('Trigger Lambda') {
            steps {
                script {
                    sh '''
                    aws lambda invoke \
                      --function-name notifyAfterPush \
                      --payload '{"image":"flask-app"}' \
                      output.json
                    '''
                }
            }
        }
    }
}
