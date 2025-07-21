# 🚀 Automated Flask Application Deployment to Amazon ECR and EC2 Using Jenkins Pipeline

## 📌 Objective

The objective of this project is to **automate the end-to-end deployment** of a Flask web application using a Jenkins CI/CD pipeline, ensuring:

- ✅ Automatic Docker image creation from application code  
- ✅ Seamless image push to **Amazon ECR**  
- ✅ Remote deployment to an **EC2 instance using SSH and Docker**  
- ✅ Repeatable, consistent deployments with minimal manual steps  
- ✅ Streamlined DevOps workflow for faster and more reliable application delivery  

This project showcases best practices in **containerization, AWS integration**, and **CI/CD automation**.

---

## 📖 Introduction

In modern DevOps practices, manual deployment is slow and error-prone. This project demonstrates how to automate Flask app deployment using a Jenkins pipeline:

- Jenkins builds a Docker image of the Flask app  
- The image is pushed to Amazon **Elastic Container Registry (ECR)**  
- Jenkins connects via SSH to an EC2 instance  
- It pulls and runs the image as a container  

This setup ensures rapid, consistent, and automated deployments with reduced risk of manual errors.

---

## 🛠️ Technology Stack

| Tool         | Purpose                                           |
|--------------|---------------------------------------------------|
| **Jenkins**  | CI/CD automation server                           |
| **Docker**   | Containerizes the Flask app                       |
| **Amazon ECR** | Stores Docker images in the cloud              |
| **EC2**      | Hosts Jenkins and/or Flask app                    |
| **GitHub**   | Source code repository                            |
| **AWS CLI**  | Manages AWS resources through scripts             |

---

## 🧱 Implementation Steps

### 🔹 Step 1: Launch EC2 Instance
- Launch Amazon Linux 2 or Ubuntu
- Open ports: **22 (SSH), 8080 (Jenkins), 80 (App)**
- Connect:  
  `ssh -i <key.pem> ec2-user@<EC2_PUBLIC_IP>`

### 🔹 Step 2: Install Docker

-  sudo yum update -y
-  sudo amazon-linux-extras install docker -y
-  sudo service docker start
-  sudo usermod -aG docker ec2-user  


### 🔹 Step 3: Run Jenkins Inside Docker

-  docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock jenkins/jenkins:lts

### 🔹 Step 4: Access Jenkins
Visit: http://<EC2_PUBLIC_IP>:8080

Get password:
 -  docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword

### 🔹 Step 5: Setup Jenkins
-  Install Suggested Plugins
-  Create Admin User

### 🔹 Step 6: Add Credentials in Jenkins
Go to: Manage Jenkins → Credentials → Global → Add Credentials
Add the following:
-  AWS Access Key (as Secret Text)
-  AWS Secret Key (as Secret Text)
-  GitHub PAT
-  EC2 Private Key (as SSH private key)

### 🔹 Step 7: Create an ECR Repository

### 🔹 Step 8: Configure Jenkins Pipeline
Add your Jenkinsfile (Declarative syntax)
-  Use stages:
-  Clone Repo
-  Build Docker Image
-  Login to ECR
-  Push Image
-  Deploy via SSH

### 🔹 Step 9: Prepare EC2 Target Server
-  Install Docker & AWS CLI
-  Open port 80
-  Allow SSH from Jenkins host or 0.0.0.0/0 for testing

### 🔹 Step 10: Run the Jenkins Job

Trigger build

Jenkins will:
-  Build image
-  Push to ECR
-  Connect to EC2 via SSH
-  Run the Flask app

### 🔹 Step 11: Verify Deployment
Visit:
http://<EC2_PUBLIC_IP>
Expected output:
"Hello from Docker!"


✅ Conclusion

This project demonstrates:
-  Jenkins in Docker builds and pushes the Flask image to ECR
-  Jenkins connects to an EC2 instance via SSH
-  It pulls the latest image and restarts the container

This solution ensures:
-  Fully automated, repeatable deployment
-  Seamless Jenkins + AWS + Docker integration
-  A robust foundation for advanced DevOps practices

