pipeline {
    agent {
        docker {
            image 'python:3.9'
            args '-v /var/jenkins_home/workspace/laab6:/workspace'
        }
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/Kr0nstadt/AquariusTesting.git'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'pip install locust'
            }
        }
        
        stage('Load Testing') {
            steps {
                sh 'locust --headless -u 5 -r 1 --run-time 30s --host=https://jsonplaceholder.typicode.com -f locustfile.py'
            }
        }
    }
}