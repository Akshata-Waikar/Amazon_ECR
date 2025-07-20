pipeline {
    agent any

    environment {
        AWS_REGION     = 'ap-northeast-2'
        APP_NAME       = 'flask-app'
        ECR_REPO       = "265980493709.dkr.ecr.ap-northeast-2.amazonaws.com/${APP_NAME}"
        IMAGE_TAG      = 'latest'
        LIVE_SERVER_IP = '43.200.180.166'  // Replace this with your EC2 public IP
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
                    if (fileExists('flask-app/Dockerfile')) {
                        sh "docker build -t ${APP_NAME} ./flask-app"
                    } else {
                        echo "⚠️ 'flask-app' directory not found — building from root directory (Jenkins is resourceful like that!)"
                        sh "docker build -t ${APP_NAME} ."
                    }
                }
            }
        }

        stage('Login to ECR') {
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                        aws configure set default.region $AWS_REGION

                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO
                    '''
                }
            }
        }

        stage('Tag & Push Image') {
            steps {
                sh '''
                    docker tag flask-app:latest $ECR_REPO:$IMAGE_TAG
                    docker push $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to Live Server') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'live-server-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no -i $SSH_KEY ec2-user@$LIVE_SERVER_IP '
                            echo "🤖 Connected to EC2."

                            AWS_REGION="ap-northeast-2"
                            ECR_REPO="265980493709.dkr.ecr.ap-northeast-2.amazonaws.com/flask-app"
                            IMAGE_TAG="latest"

                            echo "🔐 Logging into ECR..."
                            aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO

                            echo "📥 Pulling image..."
                            docker pull $ECR_REPO:$IMAGE_TAG

                            echo "🧼 Cleaning old container..."
                            docker stop flask-container || true
                            docker rm flask-container || true

                            echo "🚀 Starting new container..."
                            docker run -d --name flask-container -p 80:5000 $ECR_REPO:$IMAGE_TAG
                        '
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful! Your Flask app should now be live. If it isn’t, blame Jenkins. 😉"
        }
        failure {
            echo "❌ Deployment failed. Panic mildly, sip some coffee, then check Jenkins logs like a true DevOps detective."
        }
    }
}
