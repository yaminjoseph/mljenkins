# Set Virtual Environment
conda create -n jenkins-env python=3.10
conda activate jenkins-env
pip install -r scr/requirements.txt

# Run Package 
pip install src/.
python
import prediction_model
from prediction_model.training_pipeline import perform_training
perform_training()
clear

# Run FastAPI
python main.py

# Test FastAPI (json)
{
  "Gender": "Male",
  "Married": "No",
  "Dependents": "2",
  "Education": "Graduate",
  "Self_Employed": "No",
  "ApplicantIncome": 5849,
  "CoapplicantIncome": 0,
  "LoanAmount": 1000,
  "Loan_Amount_Term": 1,
  "Credit_History": "1.0",
  "Property_Area": "Rural"
}

# Docker
docker build -t yaminjoseph/cicd:latest .
docker images
docker push yaminjoseph/cicd
docker run -d -it --name modelv1 -p 8005:8005 yaminjoseph/cicd:latest bash
docker ps

# Docker Testing
docker exec modelv1 python prediction_model/training_pipeline.py
docker exec modelv1 pytest -v --junitxml TestResults.xml --cache-clear
docker cp modelv1:/code/src/TestResults.xml .

# Docker FastAPI
docker exec -d -w /code modelv1 python main.py
docker exec -d -w /code modelv1 uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8005

_____

#### AWS (EC2)
Launch Ubuntu Server with Port 8080 & 8005: 
- ubuntu
- t2_medium
- 30gb

Select EC2 Instance > Security > Select Security Group > Edit Inbound Rules > Add Rule:
- all tcp > anywhere-ipc4
- all tcp > anywhere-ipc4

Select EC2 Instance > Networking > Public IPv4 address Copy > add ":8080" > test it

#### GCP (Cloud Compute)
Launch Ubuntu Server with Port 8080 & 8005: 

Select Cloud Compute Engine > Create Instance > Protocols and ports > Specified protocols and ports > tcp:8080, tcp:8005
Select Instance > Copy External IP > Add ":8080"

____

# Install Jenkins on Ubuntu:

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins

# Install Java on Ubuntu:

sudo apt update
sudo apt install fontconfig openjdk-17-jre
java -version

# Enable Jenkins on Ubuntu:
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
sudo cat /var/lib/jenkins/secrets/initialAdminPassword


# Install Docker on Ubuntu:
https://docs.docker.com/engine/install/ubuntu/

sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Validation of Docker Installation on Ubunto:
sudo docker run hellow-world

# Add Ubunto Permissions (avoid using sudo)
sudo usermod -a -G docker jenkins
sudo usermod -a -G docker $USER
restart ec2/gcp instance
docker ps

# GitHub 
Create a Repository & Push Files

# Generate Github Access Token
Github > Settings > Developer Setting > Generate Personal Access Tokes > Token Classic

# Jenkins Setup
Select Instance EC2 > Copy External IP > Add ":8080" > Copy Path
Select Instance GCP > Copy External IP > Add ":8080" > Copy Path

sudo cat /var/lib/jenkins/secrets/initialAdminPassword ### Jenkis Passwords

Select Instance EC2 > Copy External IP > Add ":8080" > Paste Jenkins Password
Select Instance GCP > Copy External IP > Add ":8080" > Paste Jenkins Password

Jenkins: Select Pluggins Intall > Add Junit + Github + Email Extension Template

# Jenkins Webhooks Setup
Manage Jenkins > Credentials > (global) > add credential > secret text > paste github password 
Github Repository Setting > Webhooks > Add Webhook
- Payload URL: http://18.116.34.65:8080/github-webhook/
- Content Type: application/json
- Just the push event

Manage Jenkins > Systems > Add github Server > Assign the Credential > Test Credential > Check Manage Hooks
Create New Item > Configure > Selecy Git > Input Repository URL > Branch to Build> */main > Select GitHub hook trigger for GITScm polling

