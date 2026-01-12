# Jenkins Task
## 1. Deploy jenkins on a server baremetal way (not using docker)
### From the documents: 
### 1. install java:
```
sudo apt update
sudo apt install fontconfig openjdk-21-jre
java -version
 ```
### 2. install jenkins
```
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins
 ```
### 3. start the jenkins service
```
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins

Loaded: loaded (/lib/systemd/system/jenkins.service; enabled; vendor preset: enabled)
Active: active (running) since Tue 2018-11-13 16:19:01 +03; 4min 57s ago
 ```

## 2. Build a pipeline that builds container image and pushes it to private dokcer registry
### 1. Add credentials
Get your Dockerhub and Github Token and put it in jenkins credentials.
Use Pipeline syntax to generate the git script to use it in Pipeline

### 2. Building the pipline
```
node {
    def app
    stage('Fetch') {
        git branch: 'main', credentialsId: '3802b290-b232-4369-b32e-35fbcbe2bc5e', url: 'https://github.com/mosakrm0/jenkins-test'
        }
    stage('Build'){
        app = docker.build('mosakrmov01/task1')
    }
    stage('Push'){
        withDockerRegistry(credentialsId: 'dockerhub') {
        sh '''docker push mosakrmov01/task1 '''
            }     
    }
}
```

## 3. Build a pipeline that deploys the application to your server.
### 1. Run the deploy pipeline
```
node {
    stage('run'){
        withDockerRegistry(credentialsId: 'dockerhub') {
        sh '''docker run -d mosakrmov01/task1 '''
            }     
    }
}
```

## 4.  Build a cronjob pipeline that runs docker system prune when ever we have more than 10 dangling images,

### 1. In Triggers Put Build Periodically  ` @daily `
### 2. Run the cronjob pipeline
```
node {
    stage('check'){
        sh '''
        if ((docker images -f "dangling=true" -q | wc -l) > 10); then
            docker image prune
        fi
        '''
            }     
}
```

## 5. Edit the Build pipeline to make developer be able to choose the build branch using a dropdown menu and choose a custom image tag and default to the sha256 commit hash if not tag was specified.

```
node {
    def app
}
pipeline {
    agent any
    parameters {
        choice(name: 'Branch', choices: ['main', 'dev', 'test'], description: 'Choose a Branch')
        string(name: 'Tag', defaultValue: '', description: 'Specify the image tag.')
    }
    stages {
        stage('Fetch') {
            steps{
                git branch: "${params.Branch}", credentialsId: '3802b290-b232-4369-b32e-35fbcbe2bc5e', url: 'https://github.com/mosakrm0/jenkins-test'
                script{
                    env.CommitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                }
            }
        }
        stage('Build'){
            steps{
                script{
                    env.ImageTag = params.Tag?: env.CommitHash
                    app = docker.build("mosakrmov01/task1:${ImageTag}")   
                }
            }
        }
        stage('Push'){
            steps{
                script{
                    docker.withRegistry('', 'dockerhub'){
                    sh '''docker push mosakrmov01/task1 '''
                    }
                }
            }
        }
    }
}
```

<img width="1570" height="311" alt="image" src="https://github.com/user-attachments/assets/d08973f2-8e93-4fc7-9d8a-13caa591c280" />
<img width="1865" height="650" alt="image" src="https://github.com/user-attachments/assets/d0d054ae-6561-42bc-9c01-f4f94abb979c" />

