pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-northeast-2'
        ECR_REPO = '265980493709.dkr.ecr.ap-northeast-2.amazonaws.com/flask-app'
        IMAGE_TAG = 'latest'
        LIVE_SERVER = 'ec2-user@15.164.232.143'  // Replace with your EC2 public IP
    }

    stages {
        stage('Clone Repo') {
            steps {
                git credentialsId: 'github-pat', url: 'https://github.com/Akshata-Waikar/Amazon_ECR', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t flask-app .'
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh 'aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO'
                }
            }
        }

        stage('Tag & Push to ECR') {
            steps {
                script {
                    sh '''
                        docker tag flask-app:latest $ECR_REPO:$IMAGE_TAG
                        docker push $ECR_REPO:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy to Live Server') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'live-server-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        ssh -i $SSH_KEY -o StrictHostKeyChecking=no $LIVE_SERVER '
                            docker pull $ECR_REPO:$IMAGE_TAG &&
                            docker stop flask-container || true &&
                            docker rm flask-container || true &&
                            docker run -d --name flask-container -p 80:5000 $ECR_REPO:$IMAGE_TAG
                        '
                    '''
                }
            }
        }

        stage('Trigger Lambda') {
            steps {
                script {
                    sh '''
                        aws lambda invoke \
                        --function-name my-deploy-notifier \
                        --region $AWS_REGION \
                        --payload '{}' \
                        response.json
                    '''
                }
            }
        }
    }
}
