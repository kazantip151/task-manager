pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kazantip151/task-manager.git'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t task-manager:latest.'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run --rm task-manager:latest python -m unitest discover'
            }
        }
        stage('Push') {
            steps {
                sh 'docker tag task-manager:latest karboneyted/task-manager:latest'
                sh 'docker push karboneyted/task-manager:latest'
            }
        }
    }
}